"""Файл генерирует текст с помощью созданного словаря в train.py

Автор: Толмачев Петр Константинович

Версия №11
"""


import json
import random
import sys
import argparse



def output_text(file, result):
    """Функция отвечает за вывод текста в файл или консоль."""
    for i in result:
        file.write(i)
        file.write(' ')


def output(result):
    """Функция проверяет, куда нужно выводить файл, и выводит туда."""
    if namespace.output is None:
        console = sys.stdout
        output_text(console, result)
    else:
        with open(namespace.output, 'a', encoding='utf-8') as file:
            output_text(file, result)


def generation(dictogr):
    """Функция генерирует текст нужной длины."""
    result = list()
    if namespace.seed is None:
        l = random.choice(list(dictogr.keys()))
        result.append(l)
    else:
        result.append(namespace.seed)
    if namespace.seed not in dictogr.keys():
        raise SystemError
    for i in range(int(namespace.length) - 1):
        help_val = list(dictogr[result[i]].keys())
        if len(help_val) > 0:
            l = random.choice(help_val)
        if len(help_val) == 0:
            break
        result.append(l)
    return result


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
        dictogr = json.load(dictogram)

    # Начнем генерацию текста
    result = generation(dictogr)

    # Выведем результат
    output(result)
