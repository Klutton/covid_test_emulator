import _io
import csv
import random
from quote import get_name
import person
import covid_test_point

tel_csv_pos = ''
time_cost_range = []
capacity_range = []
nums = []
mix: int


def rand_positive(pos):
    val = random.uniform(0, 1)
    if val > pos:
        return False
    else:
        return True


def get_tel(reader:list):
    rand = random.randint(0, len(reader)-1)
    nums.append(rand)
    prefix = reader[rand][1]
    province = reader[rand][2]
    city = reader[rand][3]
    tel = prefix + f"{str(random.randint(0, 9999)):0>4}"
    return tel, province, city


class GeneratePerson:

    def __init__(self, positive_possibility: float, generate_number: int = 100):
        self.positive_possibility = positive_possibility
        self.generate_number = generate_number

    def generate(self):
        ret = []
        with open(fr"{tel_csv_pos}", 'r', encoding='utf-8') as f:
            reader = list(csv.reader(f))
            for i in range(1, self.generate_number + 1):
                id_ = i
                name = get_name.random_chinese_name()
                positive = rand_positive(self.positive_possibility)
                tel, province, city = get_tel(reader)
                while tel in nums:
                    tel, province, city = get_tel(reader)
                nums.append(tel)
                ret.append(person.Person(id_, name, positive, tel, province, city))

        return ret


class GeneratePoint:

    def __init__(self, generate_number: int = 10):
        self.generate_number = generate_number

    def generate(self):
        ret = []

        for i in range(1, self.generate_number + 1):
            id_ = i
            name = f'Covid-19 test point #{str(i)}'
            time_index = random.uniform(time_cost_range[0], time_cost_range[1])
            time_cost = [time_index - 3, time_index + 3]
            capacity = random.randint(capacity_range[0], capacity_range[1])
            ret.append(covid_test_point.Point(id_, name, time_cost, capacity, mix))
            print(f"生成{name},试管数量{capacity}")

        return ret
