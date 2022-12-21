import time
import random

import person


class Point:

    def __init__(self, id_: int, name: str, time_cost: list, capacity: int, mix: int, checked_people: int = 0):
        self.id_ = id_
        self.name = name
        self.time_cost = time_cost
        self.capacity = capacity
        self.mix = mix
        self.people_capacity = capacity * mix
        self.checked_people = checked_people
        self.complete_num = 0
        print(f"核酸点：{self.name} 人流量状态：空闲")

        self.start_time: float = -1
        self.current_cost_time: float
        self._queue = []
        self._pending = []
        self.full = False
        self.lack = False
        self.stop = False

    def new_cost_time(self):
        self.current_cost_time = random.uniform(self.time_cost[0], self.time_cost[1])
        self.start_time = time.time()

    def clear(self):
        if len(self._queue) == 0 and len(self._pending) == 0:
            if not self.stop:
                print(f"{self.name}全部核酸采样完成，采样数量：{self.complete_num}")
                self.stop = True
            return 1
        elif len(self._pending) < self.mix and len(self._queue) == 0:
            self.check_ten_samples(True)
            return 0
        else:
            self.test()
            return 0

    def test(self):
        if self.start_time == -1:
            return
        if time.time() - self.current_cost_time > self.start_time and len(self._queue) != 0:
            self.out_queue()
            self.new_cost_time()

    def in_queue(self, individual: person.Person):
        if self.check_queue_long('in'):
            if self.start_time == -1:
                self.new_cost_time()
            self.complete_num += 1
            # 计数器
            individual.queue_time = time.time()
            individual.state = person.Status.queueing
            self._queue.append(individual)
            t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(individual.queue_time))
            individual.strf_queue_time = t
            # print广播
            print(
                f"\n+++开始排队 {individual.name} id{str(individual.id_)}\n{individual.tel} {individual.province}"
                f"\n监测点为：{self.name}，时间：{t}\n排在第{len(self._queue)}个")
            return True
        else:
            return False

    def out_queue(self):

        t_now = time.time()
        individual: person.Person = self._queue.pop(0)
        t = time.strftime("%M:%S", time.localtime(t_now - individual.queue_time))
        individual.queueing_time_cost = t
        individual.state = person.Status.pending
        individual.checked = True
        individual.check_time = time.time()
        individual.strf_check_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(individual.check_time))
        individual.check_org = self.name

        # print广播
        print(f"\n---采样完成 {individual.name} id{str(individual.id_)}\n监测点为：{self.name}，用时：{t}\n")
        self._pending.append(individual)
        # 检查是否满十个样本
        self.check_ten_samples()
        self.check_queue_long('out')

    def check_queue_long(self, _type: str = ''):
        fix = 0
        if _type == 'in':
            fix = -1
        elif _type == 'out':
            fix = 1
        # 检查本核酸点人流量情况
        if self.complete_num == self.people_capacity:
            if not self.full:
                print(f'{self.name}试管耗尽！')
                self.full = True
            return False
        else:
            # 在此处设置人数剩余20的提醒
            if self.people_capacity - self.complete_num - 1 <= 50 and not self.lack:
                print(f"\n核酸点：{self.name} 采样管即将耗尽！（数量小于五根）\n")
                self.lack = True

            l = len(self._queue)  # 目前人数
            lp = l + fix  # 先前人数
            if l == 9 and lp == 10:
                print(f"\n核酸点：{self.name} 人流量状态：空闲\n")
            elif (l == 11 and lp == 10) or (l == 40 and lp == 41):
                print(f"\n核酸点：{self.name} 人流量状态：拥挤\n")
            elif l == 40 and lp == 39:
                print(f"\n核酸点：{self.name} 人流量状态：饱和\n")

            return True

    def check_ten_samples(self, stop: bool = False):
        # 等待积累十人
        if len(self._pending) == self.mix or stop:
            # 判断其中是否有阳性
            for i in range(0,len(self._pending)):
                if self._pending[i].positive:
                    self.test_complete_broadcast(person.Result.error)
                    return

            self.test_complete_broadcast(person.Result.fine)

    def test_complete_broadcast(self, result: str):
        completed = ''

        while len(self._pending) > 0:
            p = self._pending.pop(0)
            p.check_res = result
            p.state = person.Status.complete
            completed += " " + str(p.id_)
        print(f'\n核酸点：{self.name} 检测结果已出\nid:{completed}\n结果为{result}\n')
