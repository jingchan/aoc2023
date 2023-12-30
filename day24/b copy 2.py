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


def mult(p1, m):
    return (p1[0] * m, p1[1] * m, p1[2] * m)


def diff(p1, p2):
    return (p1[0] - p2[0], p1[1] - p2[1], p1[2] - p2[2])


def norm(p1):
    return math.sqrt(p1[0] ** 2 + p1[1] ** 2 + p1[2] ** 2)


def addvec(p1, v1):
    return (p1[0] + v1[0], p1[1] + v1[1], p1[2] + v1[2])


def normalized(p1):
    norm = math.sqrt(p1[0] ** 2 + p1[1] ** 2 + p1[2] ** 2)
    return (p1[0] / norm, p1[1] / norm, p1[2] / norm)


def dotproduct(p1, p2):
    return p1[0] * p2[0] + p1[1] * p2[1] + p1[2] * p2[2]


def v2sub(p1, p2):
    return (p1[0] - p2[0], p1[1] - p2[1])


def v2cross(p1, p2):
    return p1[0] * p2[1] - p1[1] * p2[0]


def crossproduct(p1, p2):
    return (
        p1[1] * p2[2] - p1[2] * p2[1],
        p1[2] * p2[0] - p1[0] * p2[2],
        p1[0] * p2[1] - p1[1] * p2[0],
    )


def coplanar(p1, p2, p3, p4):
    return (
        dotproduct(crossproduct(diff(p2, p1), diff(p3, p1)), diff(p4, p1)) == 0
    )


def coplanar_value(p1, p2, p3, p4):
    return dotproduct(
        normalized(crossproduct(diff(p2, p1), diff(p3, p1))),
        normalized(diff(p4, p1)),
    )
    # return dotproduct(
    #     normalized(crossproduct(diff(p2, p1), diff(p3, p1))), diff(p4, p1)
    # )


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


def findt(m, b, p, v):
    try:
        a = m
        c = b
        b = -v[1] / v[0] * p[0] - p[1]
        d = v[1] / v[0]
        if a - b == 0:
            if m / d > 0:
                return math.inf
            else:
                return -math.inf
        t = ((d - c) / (a - b) - p[0]) / v[0]

        return t
    except:
        raise Exception(f'm: {m}, b: {b}, p: {p}, v: {v}')
    # if (v[1] - m * v[0]) == 0:
    #     return m / (v[1] / v[0]) * math.inf
    # return (b - p[1] + m * p[0]) / (v[1] - m * v[0])


def veceq(v1, v2):
    return (v1[0] / v2[0] == v1[1] / v2[1] == v1[2] / v2[2]) or (
        v1[0] / v2[0] == v1[1] / v2[1] == v1[2] / v2[2]
    )


def solve(inst):
    fp = inst[0][0]
    fv = inst[0][1]
    bstart = inst[1]
    bend = inst[2]
    bstep = inst[3]
    maxt = -math.inf
    maxcount = 0
    bestm = 0
    bestb = 0
    besti = 0
    for i in range(bstart, bend, bstep):
        for j in range(thstep):
            totalt = 0
            m = math.tan(j / thstep * 2 * math.pi)
            # m = -0.6505993077499973
            # b = 483555514024350 + 10000 * i
            b = -m * (fp[0] + fv[0] * i) + (fp[1] + fv[1] * i)
            # print(b)
            count = 0
            for sti, (p, v) in enumerate(st):
                if p == fp and v == fv:
                    continue
                t = findt(m, b, p, v)
                # print(t)
                if t > 0:
                    count += 1
                else:
                    totalt += t
            if count > maxcount:
                maxcount = count
                maxt = totalt
                bestm = m
                bestb = b
                besti = i
                # print(
                #     f'idx: {k}, m: {bestm}, b: {bestb}, i: {besti}, maxcount: {maxcount}, maxt: {maxt}'
                # )
                # print(f'm: {m}, b: {b}, i: {i}', count)
                # # print('notinc', notinc)
                # print('t', maxt)
            elif count == maxcount and totalt >= maxt:
                maxt = totalt
                bestm = m
                bestb = b
                besti = i
    return (fp.copy(), fv.copy(), bestm, bestb, besti, maxcount, maxt)


# Given a list of points give a number that represents how linear they are.
def nonlinearity(points):
    total = 0
    for i in range(len(points)):
        for j in range(i, len(points)):
            for k in range(j, len(points)):
                v1 = normalized(diff(points[j], points[i]))
                v2 = normalized(diff(points[j], points[i]))
                total += norm(crossproduct(v1, v2))
    return total


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

    print('length:', len(st))

    bstart = 1
    bend = 5
    bstep = 1
    thstep = 300
    lo, high = 483962519523000, 483962519524000
    q = st.copy()
    keep = []
    maxxed = []
    finished = []

    origin = [0, 0, 0]
    velocity = [0, 0, 0]
    xvals = sorted([(p[0], v[0]) for p, v in st])
    for i in range(0, 1000):
        for j in range(0, 1000):
            origin[0] = i - 500
            velocity[0] = j - 500

            mxvals = sorted(
                [
                    (p[0] - origin[0], v[0] - velocity[0], -p[0] / v[0])
                    for p, v in st
                ]
            )
            print(
                f'origin[0]: {origin[0]}, velocity[0]: {velocity[0]} count',
                sum([1 for x, v, t in mxvals if t > 0]),
            )
    # print('\n'.join([str(x) for x in xvals]))
    # print('\n'.join([str(x) for x in mxvals]))
    print('count;', sum([1 for x, v, t in mxvals if t > 0]))
    # b = 483555514024350 + 10000 * i
    # for j in range(thstep):
    #     totalt = 0
    #     notinc = set()
    #     m = math.tan(j / thstep * 2 * math.pi)
    #     # m = -0.6505993077499973
    #     count = 0
    #     for _, (p, v) in enumerate(st):
    #         t = findt(m, b, p, v)
    #         if t > 0:
    #             count += 1
    #         else:
    #             totalt += t
    #             notinc.add((tuple(p), tuple(v), t))
    #     if count > maxcount:
    #         maxcount = count
    #         maxt = totalt
    #         print(f'm: {m}, b: {b}', count)
    #         print('notinc', notinc)
    #         print('t', maxt)
    #     elif count == maxcount and totalt > maxt:
    #         maxt = totalt
    #         print(f'm: {m}, b: {b}', count)
    #         print('notinc', notinc)
    #         print('t', maxt)

    # print(f'{m}:', count)
    # 490757890602892
    # print(f'{m}:', count)
    # 490757890602892


# idx: 4, m: -0.6434683848584611, b: 482073008677409.56, i: 1, maxcount: 297, maxt: -2137884789269.247
