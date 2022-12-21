import csv
import person
import pickle

people_directory = ''
point_directory = ''


def person_write(_list: list, index: int):
    with open(fr"{people_directory}/参加核酸人员.csv", 'w') as f:
        head = ['id', '姓名', '是否为阳性', '电话号码', '省', '市', '排队状态', '排队时间', '排队用时',
                '完成采样', '采样完成时间', '核酸检测地点', '核酸检测结果']
        data = []
        for individual in _list:
            data.append({
                'id': individual.id_, '姓名': individual.name, '是否为阳性': individual.positive, '电话号码': individual.tel,
                '省': individual.province, '市': individual.city,
                '排队状态': individual.state, '排队时间': individual.strf_queue_time, '排队用时': individual.queueing_time_cost,
                '完成采样': individual.checked, '采样完成时间': individual.strf_check_time, '核酸检测地点': individual.check_org,
                '核酸检测结果': individual.check_res
            })

        writer = csv.DictWriter(f, head)
        writer.writeheader()
        writer.writerows(data)

    with open(fr"{people_directory}/people.dat", 'wb') as f:
        pickle.dump(_list, f)

    with open(fr"{people_directory}/index.dat", 'wb') as f:
        pickle.dump(index, f)


def point_write(_list: list):
    with open(fr"{people_directory}/point_data.dat", 'wb') as f:
        pickle.dump(_list, f)


def read():
    with open(f"{people_directory}/people.dat", 'rb') as f:
        people = pickle.load(f)
    with open(f"{point_directory}/point_data.dat", 'rb') as f:
        point = pickle.load(f)
    with open(fr"{people_directory}/index.dat", 'rb') as f:
        index = pickle.load(f)
    return people, point, index
