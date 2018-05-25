"""Файл создает словарь из данного текста,
который впоследствии обрабатывается в generate.py

Автор: Толмачев Петр Константинович

Версия №11
"""


import re
import argparse
import json
import sys
import os
import collections


def parse_line(line):
    """Функция парсит полученную строку, удаляет все лишнее, возвращает list()."""
    f = re.sub('\d+', '', line)
    result = re.findall('\w+', f)
    return result


def bigram_to_json(my_list):
    """Функция переводит в удобный для работы формат и записывает в json файл."""
    dictogr = dict()
    for key, value in my_list:
        if key not in dictogr:
            dictogr[key] = dict()
            dictogr[key][value] = 1
        elif value in dictogr[key]:
            dictogr[key][value] += 1
        else:
            dictogr[key][value] = 1
        if value not in dictogr:
            dictogr[value] = dict()

    # Запишем результат в файл
    with open(namespace.model, 'tw', encoding='utf-8') as json_file:
        json.dump(dictogr, json_file)


def gen_file(dir):
    """Функция возвращает все файлы из директории"""
    if dir is None:
        print('Введите текст и закончите символом '
              'конца файла(специальная комбинация клавиш)')
        return sys.stdin
    else:
        for top, dirs, files in os.walk(namespace.dir):
            for nm in files:
                path = str(os.path.join(top, nm))
                # Обработаем данный файл
                with open(path, 'r', encoding='utf-8') as workFile:
                    yield workFile



parser = argparse.ArgumentParser(description='train')
parser.add_argument(
    '--input-dir',
    default=None,
    help='Путь к директории, из которой берутся тексты',
    dest='dir'
)
parser.add_argument(
    '--model',
    default=None,
    help='Путь к файлу, в который следует загрузить модель'
)
parser.add_argument(
    '--lc',
    default=None,
    help='Приведение текстов к lowercase', nargs='*'
)

if __name__ == '__main__':
    namespace = parser.parse_args()
    my_map = collections.Counter()

    # Проверим все директории на наличие читаемых файлов, если указан путь
    for file in gen_file(namespace.dir):
        for line in file:
            if namespace.lc is not None:
                line = line.lower()
            my_map.update(
                zip(parse_line(line)[:-1], parse_line(line)[1:])
            )

    bigram_to_json(my_map)
