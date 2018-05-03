# Файл создает словарь из данного текста, который впоследствии обрабатывается в generate.py
# Автор: Толмачев Петр Константинович
# Версия №4


import re
import argparse
import json
import os
import collections


def remap_keys(mapping):
     return [{'key':k, 'value': v} for k, v in mapping.iteritems()]


"""
Отпарсим аргументы терминала.
Вводить в ввиде:
python --input-dir <путь до директории> --model <путь к файлу, куда сохранять словарь> '--lc'
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
    """
    Переведем данные тексты в удобный для нас формат:
    """
    if namespace.dir is not None:
        for top, dirs, files in os.walk(namespace.dir):
            for nm in files:
                path = str(os.path.join(top, nm))
                with open(path, 'r', encoding='utf-8') as workFile:
                    while True:
                        line = workFile.readline()
                        if namespace.lc is not None:
                            line = line.lower()
                        if len(line) == 0:
                            break
                        f = re.sub('\d+', '', line)
                        result = re.findall('\w+', f)
                        myMap.update(zip(result[:-1], result[1:]))
                workFile.close()
    else:
        print('Введите текст и закончите символом\
         конца файла(специальная комбинация клавиш)')
        while True:
            s = input()
            if namespace.lc is not None:
                s = s.lower()
            if len(s) == 0:
                break
            f = re.sub('\d+', '', s)
            result = re.findall('\w+', f)
            myMap.update(zip(result[:-1], result[1:]))

    """
    Запишем в файл полученный словарь:
    """
    with open(namespace.model, 'tw', encoding='utf-8') as json_file:
        json.dump(list(myMap), json_file)
    json_file.close()
