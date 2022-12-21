
class Result:
    error = "混管异常"
    fine = "阴性"
    pending = "未完成"


class Status:
    error = "检测试管不足，未能采样"
    complete = "核酸结果已出"
    pending = "采样完成，等待结果"
    queueing = "排队中"
    waiting = "未排队"


class Person:
    def __init__(self, id_: int, name: str, positive: bool, tel: str, province: str, city: str,
                 state: int = Status.waiting, queue_time: float = None, queueing_time_cost: float = None, checked: bool = False,
                 check_time: float = None, check_org: str = None, check_res: str = Result.pending):
        self.id_ = id_
        self.name = name
        self.positive = positive
        self.tel = tel
        self.province = province
        self.city = city
        self.state = state
        self.queue_time = queue_time
        self.queueing_time_cost = queueing_time_cost
        self.checked = checked
        self.check_time = check_time
        self.check_org = check_org
        self.check_res = check_res
        self.strf_queue_time = None
        self.strf_check_time = None

    def is_positive(self):
        return self.positive
