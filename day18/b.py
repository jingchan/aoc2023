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

    # shoelace formula
    area = 0
    for i in range(len(points) - 2):
        area += getarea(points[0], points[i + 1], points[i + 2])

    # pick's theorem
    i = area - b / 2 + 1
    print(i + b)

    # print(total)

    # print((maxx-minx+1)*(maxy-miny+1) -outtotal)

    # 952408144115
    # 952408144115.0
    # 952407629995
    #  952407629995

    # 1863245620090
# 952408144115
# 952408144115


#  0,0 ------------ 461k,0
#   |               461k,56k --------------------- 818k, 56k
#   |                   497k,356k --- 609k,356k        |
#  0,500k - 5k,500k          |            |            |
#              |             |            |        818k,919k ------- 1.1m,919k                                               818k,919k         1.1m,919k
#           5k,1.1m --- 497k,1.1m     609k,1.1m -------------------- 1.1m,1.1m
#
#
#

# (461937+1)*56407
# 26,056,536,766
# print((1186328-461937)*56407) #=40860723137
# 40860723137- 40859998746
# # 44644467493502
# (1186328-818608)
