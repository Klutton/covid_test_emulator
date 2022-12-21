#!/usr/bin/env python
# -*- coding: utf-8 -*-
#author:gorgiaxx

import csv
import getopt
import sys
import random

def get_rand():
    try:
        with open(location_file,'r') as c:
            reader = csv.reader(c)
            rand = random.randint(1,327666)
            return

# 获取当前城市的所有号码前缀
def get_number(citys,types):
    try:
        with open(location_file, 'r') as csvfile:
            reader = csv.reader(csvfile)
            number_prefix_arr = []
            if len(types):
                for line in reader:
                    if line[3] in citys and line[4] in types:
                        number_prefix_arr.append(line[1])
            else:
                for line in reader:
                    if line[3] in citys:
                        number_prefix_arr.append(line[1])
            csvfile.close()
            if len(number_prefix_arr):
                print('总共生成{0}条记录,预计占用空间{1:.3f}MB'.format(len(number_prefix_arr) * 10000, len(number_prefix_arr) * 10000 * 12 / 1024 / 1024))
            else:   sys.exit(0)
            return number_prefix_arr
    except Exception as e:
        print(e)

# 写手机号到文件
def gen_number(number_prefix_arr, output_file):
    try:
        with open(output_file, 'w') as f:
            for i in number_prefix_arr:
                for n in range(0,10000):
                    f.writelines(i + "{:0>4d}".format(n) + '\n')
        print("生成成功，文件：", output_file)
    except Exception as e:
        print(e)

def usage():
    print("Usage:python gen_phonenumber.py -c 厦门 [-t 中国联通,中国电信] ~/xiamen.txt");

if __name__ == '__main__':
    print('+' + '-' * 40 + '+')
    print('\t  根据区域生成手机号列表')
    print('+' + '-' * 40 + '+')
    location_file = 'phonelocation.csv'

    if len(sys.argv) < 3:
        usage()
    try:
        options,args = getopt.getopt(sys.argv[1:],"c:t:o")
        citys = ''
        types = ''
        output_file = ''
        for opt,arg in options:
            if opt == '-c':
                citys = arg.split(',')
            elif opt == '-t':
                types = arg.split(',')
        output_file = args[0]
        gen_number(get_number(citys, types),output_file)

    except Exception as e:
        print(e)
        usage()
