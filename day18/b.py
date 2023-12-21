import math
import os
import re

PATH = os.path.dirname(__file__)
# IN_FILE = PATH + '/1.txt'
IN_FILE = PATH + '/2.txt'

dirs = [
    (1, 0),
    (0, 1),
    (-1, 0),
    (0, -1),
]


def p2v(a, b):
    return (b[0] - a[0], b[1] - a[1])


def cross(a, b):
    return a[0] * b[1] - a[1] * b[0]


def getarea(a, b, c):
    return cross(p2v(a, b), p2v(a, c)) / 2


with open(IN_FILE, 'r') as f:
    input = []
    for line in f.readlines():
        line = line.strip()
        hex = line.split(' ')[2]
        l = int(hex[2:-2], 16)
        d = int(hex[-2])
        input.append((d, l))

    cur = (0, 0)
    points = []
    b = 0
    for i in range(len(input)):
        (d, l) = input[(i) % len(input)]
        points.append((cur))
        cur = (cur[0] + dirs[d][0] * l, cur[1] + dirs[d][1] * l)
        b += l

    # def cross(a, b):
    #     return a[0] * b[1] - a[1] * b[0]

    # def getarea(a, b, c):
    #     return cross(p2v(a, b), p2v(a, c)) / 2

    # shoelace formula
    area = 0
    for i in range(len(points) - 2):
        area += getarea(points[0], points[i + 1], points[i + 2])

    # pick's theorem
    i = area - b / 2 + 1
    print(i + b)
