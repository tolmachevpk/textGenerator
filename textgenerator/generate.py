import json
import random
import sys
import os
import argparse


#отпарсим аргументы терминала
parser = argparse.ArgumentParser(description='generate')
parser.add_argument('--model', default=None, help='Путь к файлу, из которого загружается модель')
parser.add_argument('--seed', default=None, help='Начальное слово')
parser.add_argument('--length', default=-1, help='Длина генерируемой последовательности')
parser.add_argument('--output', default=None, help='Файл, в который следует выводить результат')
namespace = parser.parse_args()

if namespace.model == None:
    print('Путь к файлу, из которого загружается модель, не указан')
    sys.exit()
if not os.path.exists(namespace.model):
    print('Путь к файлу, из которого загружается модель, указан неверно')
    sys.exit()
if int(namespace.length) < 0:
    print('Длина генерируемой последовательности либо не указана, либо не корректна')
    sys.exit()

dictogr = dict()
dictogr = json.load(open(namespace.model, 'r')) #скачаем словарь

#сгенерируем текст
result = list()
if namespace.seed == None:
    l = random.choice(list(dictogr.keys()))
    while l == '':
        l = random.choice(list(dictogr.keys()))
    result.append(l)
else:
    result.append(namespace.seed)
for i in range(int(namespace.length) - 1):
    l = random.choice(list(dictogr[result[i]].keys()))
    result.append(l)

#выведем результат
if namespace.output == None:
    for i in result:
        print(i, end=' ')
else:
    file = open(namespace.output, 'w')
    file.write(result)
    file.close()
