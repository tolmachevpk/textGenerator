import re
import argparse
import json
import os
import collections


def upgrade(selfmap, iterable):  # заполнение словаря
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
            selfmap[j] = collections.Counter()
            j = i
    return selfmap


# отпарсим аргументы терминала
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
namespace = parser.parse_args()

if __name__ == '__main__':
    myMap = dict()
    if namespace.dir is not None:
        for top, dirs, files in os.walk(namespace.dir):
            for nm in files:
                path = str(os.path.join(top, nm))
                workFile = open(path, 'r', encoding='utf-8')
                line = str
                if namespace.lc is not None:
                    line = workFile.readline().lower()
                else:
                    line = workFile.readline()
                while line:
                    f = re.sub('\d+', '', line)
                    upgrade(myMap, f)
                    if namespace.lc is not None:
                        line = workFile.readline().lower()
                    else:
                        line = workFile.readline()
                workFile.close()
    else:
        print('Введите текст и закончите его пустой строкой')
        s = str
        while s != '':
            if namespace.lc is not None:
                s = input().lower()
            else:
                s = input().read()
            f = re.sub('\d+', '', s)
            upgrade(myMap, f)

    json.dump(myMap, open(namespace.model, 'tw', encoding='utf-8'))
