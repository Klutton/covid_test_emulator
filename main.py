import random
import generator
import io_manage
import json
import time
from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput
from pycallgraph import Config
import person

interval: float
restart: bool = True
start_point: int
_person_queue: list
_point_queue: list
full = False


def setup():
    with open('config.json', 'r') as f:
        conf = json.loads(f.read())
        generator.time_cost_range = conf['point']['time_cost_range']
        generator.capacity_range = conf['point']['capacity_range']
        generator.mix = conf['point']['mixed_sample_amount']
        generator.tel_csv_pos = conf['telnum_directory']
        io_manage.people_directory = conf['people_directory']
        io_manage.point_directory = conf['point_directory']
        global interval, restart, start_point
        interval = conf['person']['interval']
        restart = conf['restart']

    return (conf['person']['positive_possibility'], conf['person']['generate_number']), conf['point']['generate_number']


def check_full():
    cnt = 0
    for point in _point_queue:
        if point.full:
            cnt += 1
    if cnt == len(_point_queue):
        global full
        full = True
        print("***所有核酸点试管均耗尽")
        return True
    else:
        return False


def wait_end(index: int):
    ret = 0
    while ret != len(_point_queue):
        ret = 0
        for queue in _point_queue:
            ret += queue.clear()
            io_manage.point_write(_point_queue)
            io_manage.person_write(_person_queue, index)


def start_queueing():
    try:
        for point in _point_queue:
            point.check_queue_long()
        t = time.time()
        index = start_point
        while index < len(_person_queue):
            time.sleep(0.5)

            if time.time() - t >= interval:
                t = time.time()
                while True:
                    rand = random.randint(0, len(_point_queue) - 1)
                    if _point_queue[rand].in_queue(_person_queue[index]) or check_full():
                        io_manage.person_write(_person_queue, index)
                        break

                for point in _point_queue:
                    point.test()
                    io_manage.point_write(_point_queue)

                if full:
                    while index < len(_person_queue):
                        _person_queue[index].state = person.Status.error
                        index += 1

                    wait_end(index)
                    io_manage.point_write(_point_queue)
                    io_manage.person_write(_person_queue, index)
                    print("测试试管耗尽，未排队者未能核酸，模拟结束")
                    return

                index += 1

        print(f"\n***所有人均已进入核酸队伍，共{len(_person_queue)}人")
        wait_end(index)

        print("\n模拟结束！")

    except Exception as e:
        print(f"程序中断，资料已保存\n{e}")


def main():
    # 获取生成参数
    global _person_queue, _point_queue, start_point
    person_gen, point_gen = setup()
    print("初始化完成")
    if restart:
        _person_queue = generator.GeneratePerson(person_gen[0], person_gen[1]).generate()
        _point_queue = generator.GeneratePoint(point_gen).generate()
        start_point = 0
        print("随机数据已经生成")
        start_queueing()
    else:
        try:
            print("等待数据载入，请不要终止程序")
            _person_queue, _point_queue, start_point = io_manage.read()
            print("数据已经载入")
        except Exception as e:
            print(f"尝试启动restart功能启动\n{e}")

        start_queueing()


if __name__ == '__main__':
    config = Config()
    graphviz = GraphvizOutput()
    graphviz.output_file = 'graph.png'

    with PyCallGraph(output=graphviz, config=config):
        main()
