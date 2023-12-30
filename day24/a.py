import math
import os
import re
import pickle
from itertools import combinations

PATH = os.path.dirname(__file__)

TEST = False

IN_FILE = PATH + '/2.txt'
if TEST:
    IN_FILE = PATH + '/1.txt'

DIRS = [(-1, 0, '^'), (1, 0, 'v'), (0, -1, '<'), (0, 1, '>')]


def addvec(p1, v1):
    return (p1[0] + v1[0], p1[1] + v1[1])


def normalized(p1):
    norm = math.sqrt(p1[0] ** 2 + p1[1] ** 2)
    return (p1[0] / norm, p1[1] / norm)


def dotproduct(p1, p2):
    return p1[0] * p2[0] + p1[1] * p2[1]


def timeto(p1, v1, target):
    return (target[0] - p1[0]) / v1[0]


def lineintersection(p1, v1, p2, v2):
    x1 = (p1[0], p1[1])
    x2 = (p1[0] + v1[0], p1[1] + v1[1])
    x3 = (p2[0], p2[1])
    x4 = (p2[0] + v2[0], p2[1] + v2[1])
    if (
        (x1[0] - x2[0]) * (x3[1] - x4[1]) - (x1[1] - x2[1]) * (x3[0] - x4[0])
    ) == 0:
        return False, (0, 0)
    if (
        (x1[0] - x2[0]) * (x3[1] - x4[1]) - (x1[1] - x2[1]) * (x3[0] - x4[0])
    ) == 0:
        return False, (0, 0)
    px = (
        (x1[0] * x2[1] - x1[1] * x2[0]) * (x3[0] - x4[0])
        - (x1[0] - x2[0]) * (x3[0] * x4[1] - x3[1] * x4[0])
    ) / ((x1[0] - x2[0]) * (x3[1] - x4[1]) - (x1[1] - x2[1]) * (x3[0] - x4[0]))
    py = (
        (x1[0] * x2[1] - x1[1] * x2[0]) * (x3[1] - x4[1])
        - (x1[1] - x2[1]) * (x3[0] * x4[1] - x3[1] * x4[0])
    ) / ((x1[0] - x2[0]) * (x3[1] - x4[1]) - (x1[1] - x2[1]) * (x3[0] - x4[0]))
    return True, (px, py)


with open(IN_FILE, 'r') as f:
    # line = f.readline()
    grid = []
    st = []
    for line in f.readlines():
        line = line.strip()
        pos = [int(x) for x in line.split(' @ ')[0].split(', ')]
        vel = [int(x) for x in line.split(' @ ')[1].split(', ')]
        st.append((pos, vel))
        # grid.append(list(line))

    cols = 0
    for i, (p, v) in enumerate(st):
        for j, (p2, v2) in enumerate(st):
            if i == j:
                continue
            if i > j:
                continue
            c = True

            np = addvec(p, v)
            np2 = addvec(p2, v2)

            # if dotproduct(normalized(np), normalized(np2)) > dotproduct(
            #     normalized(p), normalized(p2)
            # ):
            # continue

            didsec, sect = lineintersection(p, v, p2, v2)
            if not didsec:
                continue
            # print(sect)
            if timeto(p, v, sect) < 0:
                continue
            if timeto(p2, v2, sect) < 0:
                continue
            if TEST:
                if not (sect[0] >= 7 and sect[0] <= 27):
                    continue
                if not (sect[1] >= 7 and sect[1] <= 27):
                    continue
            else:
                if not (
                    sect[0] >= 200000000000000 and sect[0] <= 400000000000000
                ):
                    continue
                if not (
                    sect[1] >= 200000000000000 and sect[1] <= 400000000000000
                ):
                    continue
            # print(sect)

            cols += 1
    print(cols)
