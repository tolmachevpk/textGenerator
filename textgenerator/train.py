import re
import argparse
import json
import os
import sys


def upgrade(selfmap, iterable): #заполнение словаря
    j = ''
    result = re.findall('\w+', iterable)
    for i in result:
        if j in selfmap:
            if i in selfmap[j]:
                selfmap[j][i] += 1
            else:
                selfmap[j][i] = 1
            j = i
        else:
            selfmap[j] = dict({i: 1})
            j = i
    return selfmap


parser = argparse.ArgumentParser(description='train')
parser.add_argument('--input_dir', default=None, help='Путь к директории, из которой берутся тексты')
parser.add_argument('--model', default=None, help='Путь к файлу, в который следует загрузить модель')
parser.add_argument('--lc', default=None, help='Приведение текстов к lowercase', nargs='*')
namespace = parser.parse_args()

if namespace.model == None:
    print('Путь к файлу, в который сохраняется модель, не указан')
    sys.exit()
if not os.path.exists(namespace.model):
    print('Путь к файлу, в который сохраняется модель, указан неверно')
    sys.exit()

myMap = dict()
if namespace.input_dir != None:
    for file in os.listdir(path=namespace.input_dir):
        workFile = open('{}/{}'.format(namespace.input_dir, file))
        line = str
        if namespace.lc != None:
            line = workFile.readline().lower()
        else:
            line = workFile.readline()
        while line:
            f = re.sub('\d+', '', line)
            upgrade(myMap, f)
            if namespace.lc != None:
                line = workFile.readline().lower()
            else:
                line = workFile.readline()
        workFile.close()
else:
    print('Введите текст и закончите его пустой строкой')
    s = str
    while s != '':
        if namespace.lc != None:
            s = input().lower()
        else:
            s = input().read()
        f = re.sub('\d+', '', s)
        upgrade(myMap, f)
json.dump(myMap, open(namespace.model, 'w'))
