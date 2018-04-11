import json
import random
import sys
import argparse


# отпарсим аргументы терминала
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
namespace = parser.parse_args()


if __name__ == '__main__':
    if int(namespace.length) < 0:
        print('Длина генерируемой последовательности либо не корректна')
        sys.exit()

    dictogr = dict()
    dictogr = json.load(open(namespace.model, 'r'))  # скачаем словарь

    # сгенерируем текст
    result = list()
    if namespace.seed is None:
        l = random.choice(list(dictogr.keys()))
        while l == '':
            l = random.choice(list(dictogr.keys()))
        result.append(l)
    else:
        result.append(namespace.seed)
    if namespace.seed in dictogr.keys():
        pass
    else:
        raise SystemError
    for i in range(int(namespace.length) - 1):
        l = random.choice(list(dictogr[result[i]].keys()))
        result.append(l)

    # выведем результат
    if namespace.output is None:
        for i in result:
            print(i, end=' ')
    else:
        file = open(namespace.output, 'a', encoding='utf-8')
        for i in result:
            file.write(i)
            file.write(' ')
        file.close()
