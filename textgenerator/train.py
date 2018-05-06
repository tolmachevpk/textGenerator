"""Файл создает словарь из данного текста,
который впоследствии обрабатывается в generate.py

Автор: Толмачев Петр Константинович

Версия №7
"""


import re
import argparse
import json
import sys
import os
import collections


"""Функция парсит полученную строку, удаляет все лишнее, возвращает list()"""
def parse_line(line):
    f = re.sub('\d+', '', line)
    result = re.findall('\w+', f)
    return result


"""Отпарсим аргументы терминала.

Использование:
>>> python --input-dir <путь до директории>
    --model <путь к файлу, куда сохранять словарь> '--lc'

Подробнее описано в help.
"""
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
    myMap = collections.Counter()

    # Проверим все директории на наличие читаемых файлов, если указан путь
    if namespace.dir is not None:
        for top, dirs, files in os.walk(namespace.dir):
            for nm in files:
                path = str(os.path.join(top, nm))
                # Обработаем данный файл
                with open(path, 'r', encoding='utf-8') as workFile:
                    while True:
                        line = workFile.readline()
                        if namespace.lc is not None:
                            line = line.lower()
                        if len(line) == 0:
                            break
                        f = re.sub('\d+', '', line)
                        result = re.findall('\w+', f)
                        myMap.update(
                            zip(parse_line(line)[:-1], parse_line(line)[1:])
                        )
                workFile.close()
    else:
        print('Введите текст и закончите символом\
         конца файла(специальная комбинация клавиш)')
        while True:
            try:
                s = sys.stdin.readline()
            except:
                break
            if namespace.lc is not None:
                s = s.lower()
            myMap.update(
                zip(parse_line(s)[:-1], parse_line(s)[1:])
            )

    # Запишем результат в файл
    with open(namespace.model, 'tw', encoding='utf-8') as json_file:
        json.dump(list(myMap), json_file)
    json_file.close()
