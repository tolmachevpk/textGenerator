"""Файл генерирует текст с помощью созданного словаря в train.py

Автор: Толмачев Петр Константинович

Версия №7
"""


import json
import random
import sys
import argparse


"""Отпарсим аргументы терминала.

Использование:
>>> python --model <путь к файлу, куда сохранять словарь>
    '--seed <начальное слово>'
    '-- length <число - длина генерируемого текста>'
    '--output <файл, в который записываем результат>'

Подробнее описано в help.
"""
parser = argparse.ArgumentParser(description='generate')
parser.add_argument(
    '--model',
    default=None,
    help='Путь к файлу, из которого загружается модель'
)
parser.add_argument(
    '--seed',
    default=None,
    help='Начальное слово'
)
parser.add_argument(
    '--length',
    default=-1,
    help='Длина генерируемой последовательности'
)
parser.add_argument(
    '--output',
    default=None,
    help='Файл, в который следует выводить результат'
)


if __name__ == '__main__':
    namespace = parser.parse_args()
    if int(namespace.length) < 0:
        raise ValueError('Введенное число некорректно')

    # скачаем словарь и переведем в удобный для работы вид (словарь словарей)
    with open(namespace.model, 'r') as dictogram:
        thing = json.load(dictogram)
    dictogram.close()
    dictogr = dict()
    for key, value in thing:
        if key not in dictogr:
            dictogr[key] = dict()
            dictogr[key][value] = 1
        if value in dictogr[key]:
            dictogr[key][value] += 1
        else:
            dictogr[key][value] = 1
    lastWord = thing[len(thing) - 1][1]

    # Начнем генерацию текста
    result = list()
    if namespace.seed is None:
        l = random.choice(list(dictogr.keys()))
        result.append(l)
    else:
        result.append(namespace.seed)
    if namespace.seed not in dictogr.keys() and lastWord != namespace.seed:
        raise SystemError
    for i in range(int(namespace.length) - 1):
        try:
            l = random.choice(list(dictogr[result[i]].keys()))
        except:
            break
        result.append(l)

    # Выведем результат
    if namespace.output is None:
        for i in result:
            sys.stdout.write(i)
            sys.stdout.write(' ')
    else:
        with open(namespace.output, 'a', encoding='utf-8') as file:
            for i in result:
                file.write(i)
                file.write(' ')
        file.close()
