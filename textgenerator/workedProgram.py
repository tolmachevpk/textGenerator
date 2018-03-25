# coding: utf-8
import random
import re
import os
import argparse


class Dictogram():
    def __init__(self):
        self.map = dict() #создание словаря

    def upgrade(self, iterable): #заполнение словаря
        j = 'END'
        result = re.findall('\w+', iterable)
        for i in result:
            if j in self.map:
                if i in self.map[j]:
                    self.map[j][i] += 1
                else:
                    self.map[j][i] = 1
                j = i
            else:
                self.map[j] = dict({i: 1})
                j = i

    def make_random_start(self): #генерация начала предложения
        return random.choice(list(self.map.keys()))

    def make_random_sentence(self, start, n): #генерация предложения до количества n слов
        n -= 1
        l = list()
        l.append(start)
        for i in range(n):
            g = list(self.map[l[i]].keys())
            a = random.choice(g)
            l.append(a)
        return l


parser = argparse.ArgumentParser()
parser.add_argument('input_dir', type=str, help='Input path to directory')
parser.add_argument('length', type=int, help='Write length of sentence')
args = parser.parse_args()
if args.input_dir != None:
    for top, dirs, files in os.walk(args.input_dir):
        for nm in files:
            path = str(os.path.join(top, nm))
            file = open(path, 'r', encoding='cp1251')
            s = file.read().lower()
            f = re.sub('\d+', '', s)
            a = Dictogram()
            a.upgrade(f)
else:
    s = input().lower()
    f = re.sub('\d+', '', s)
    a = Dictogram()
    a.upgrade(f)
start = a.make_random_start()
result = a.make_random_sentence(start, args.length)
for i in result:
    print(i, end=' ')


def documentations():
    """
    Алгоритм генерации предложения:
        1. Приведение всех букв к нижнему регистру
        2. Удаление цифр и всех остальных символов, не считая букв
        3. Заведение всех слов в специальный словарь с учетом количества их вхождений\
         в первоначальное предложение
        4. Генерация начала предложения
        5. Генерация оставшихся слов до нужно количества слов в предложении
        6. Вывод предложения

    :return:
    Сгенерированная строка
    """
