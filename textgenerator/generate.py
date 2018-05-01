# Файл генерирует текст с помощью созданного словаря в train.py
# Автор: Толмачев Петр Константинович
# Версия №4


import json
import random
import sys
import argparse


"""
Отпарсим аргументы терминала.
Вводить в ввиде:
python --model <путь к файлу, куда сохранять словарь> '--seed <начальное слово>'
'-- length <число - длина генерируемого текста>' '--output <файл, в который записываем результат>'
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

    with open(namespace.model, 'r') as dictogram:
        dictogr = json.load(dictogram)  # скачаем словарь
    dictogram.close()

    """
    Сгенерируем сам текст:
    """
    result = list()
    if namespace.seed is None:
        while True:
            l = random.choice(list(dictogr.keys()))
            if l != '':
                break
        result.append(l)
    else:
        result.append(namespace.seed)
    if namespace.seed not in dictogr.keys():
        raise SystemError
    for i in range(int(namespace.length) - 1):
        if len(dictogr[result[i]].keys()) == 1\
                and list(dictogr[result[i]].keys())[0] == 'END':
            break
        else:
            while True:
                l = random.choice(list(dictogr[result[i]].keys()))
                if l != 'END':
                    break
        result.append(l)

    """
    Выведем результат:
    """
    if namespace.output is None:
        for i in result:
            print(i, end=' ')
    else:
        with open(namespace.output, 'a', encoding='utf-8') as file:
            for i in result:
                file.write(i)
                file.write(' ')
        file.close()
