import math
import os
import re
import pickle
from itertools import combinations

PATH = os.path.dirname(__file__)

TEST = True
# TEST = False

IN_FILE = PATH + '/2.txt'
if TEST:
    IN_FILE = PATH + '/1.txt'

DIRS = [(-1, 0, '^'), (1, 0, 'v'), (0, -1, '<'), (0, 1, '>')]


def vecmul(p1, m):
    return (p1[0] * m, p1[1] * m, p1[2] * m)


def norm(p1):
    return math.sqrt(p1[0] ** 2 + p1[1] ** 2 + p1[2] ** 2)


def vecadd(p1, v1):
    return (p1[0] + v1[0], p1[1] + v1[1], p1[2] + v1[2])


def normalized(p1):
    norm = math.sqrt(p1[0] ** 2 + p1[1] ** 2 + p1[2] ** 2)
    return (p1[0] / norm, p1[1] / norm, p1[2] / norm)


# |a||b|cos(theta) = a dot b
def dotproduct(p1, p2):
    return p1[0] * p2[0] + p1[1] * p2[1] + p1[2] * p2[2]


def vecsub(p1, p2):
    return (p1[0] - p2[0], p1[1] - p2[1], p1[2] - p2[2])


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


# Given a list of points give a number that represents how non linear they are.
#
# If this is equal to 0, then points are linear.
def nonlinearity(points):
    total = 0
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            for k in range(j + 1, len(points)):
                v1 = vecsub(points[j], points[i])
                v2 = vecsub(points[k], points[i])
                v1 = normalized(v1)
                v2 = normalized(v2)
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
    # USE_THEATA_PHI = True
    USE_THEATA_PHI = False
    # TEST_SLICE = st[:100]
    TEST_SLICE = st
    # Use x,y,z
    minarea = math.inf
    center = (-0.9327765579626527, 3.0832784107538593)
    zoomScale = 1
    # center = (1.9664709829294493, 6.033390073442831)
    hail = [(p, v) for p, v in st]
    axissteps = 50
    axisrange = 50
    offset = (0, 0, 0)
    cvel = (0, 0, 0)
    for iteri in range(axissteps):
        for iterj in range(axissteps):
            for iterk in range(axissteps):
                x = (
                    math.floor(cvel[0])
                    + (iteri / axissteps - 0.5) * axisrange
                    + offset[0]
                )
                y = (
                    math.floor(cvel[1])
                    + (iterj / axissteps - 0.5) * axisrange
                    + offset[1]
                )
                z = (
                    math.floor(cvel[2])
                    + (iterk / axissteps - 0.5) * axisrange
                    + offset[2]
                )
                if x == 0 or y == 0 or z == 0:
                    continue
                x = -3
                y = 1
                z = 2

                fdir = (x, y, z)
                # fdir = normalized(vecsub((21, 14, 12), (24, 13, 10)))
                projected = []
                for it, (p, v) in enumerate(TEST_SLICE):
                    dotval = dotproduct(fdir, p)
                    pp = vecsub(p, vecmul(fdir, dotval))
                    dotval = dotproduct(fdir, v)
                    pv = vecsub(v, vecmul(fdir, dotval))
                    # print('projected on guess', p, v, pp, pv)

                    # print('projected on guess',p1, v1, p2, v2)
                    zup = (0, 0, 1)
                    dotval = dotproduct(zup, pp)
                    pp = vecsub(pp, vecmul(zup, dotval))
                    dotval = dotproduct(zup, pv)
                    pv = vecsub(pv, vecmul(zup, dotval))
                    projected.append((pp, pv))
                    # print('projected on guess', p, v, pp, pv)

                    # print('projected on guess',p1, v1, p2, v2)

                intersections = []
                nonintersectcount = 0
                for s, (p1, v1) in enumerate(projected):
                    for t, (p2, v2) in enumerate(projected):
                        if t <= s:
                            continue

                        doesintersect, intersection = lineintersection(
                            p1, v1, p2, v2
                        )
                        # if intersection[0] < 0.01 or intersection[1] < 0.01:
                        #     continue
                        # if intersection[0] > 1000000000000000000:
                        #     nonintersectcount += 1
                        #     continue
                        # if intersection[1] > 1000000000000000000:
                        #     nonintersectcount += 1
                        #     continue

                        if not doesintersect:
                            nonintersectcount += 1
                            continue
                            # print('nointersection', p1, v1, p2, v2)
                            # raise Exception()
                        else:
                            intersections.append(intersection)
                # if len(intersections) <= 3:
                #     continue
                # if len(intersections) < len(TEST_SLICE):
                #     continue
                if nonintersectcount > len(intersections) / 2:
                    # print(
                    #     'nonintersections',
                    #     nonintersectcount,
                    #     'intersections',
                    #     len(intersections),
                    # )
                    pass
                    # continue
                mins = (
                    min([x[0] for x in intersections]),
                    min([x[1] for x in intersections]),
                )
                maxs = (
                    max([x[0] for x in intersections]),
                    max([x[1] for x in intersections]),
                )
                # area = (maxs[1] - mins[1]) * (maxs[0] - mins[0])
                area = (maxs[1] - mins[1]) + (maxs[0] - mins[0])
                if area < minarea:
                    print('MINAREA', minarea, mins, maxs)
                    print(
                        'nonintersections',
                        nonintersectcount,
                        'intersections',
                        len(intersections),
                    )
                    print(intersections)
                    print('guesseddir', fdir)

                    minarea = area
                    intavg = (
                        sum([x[0] for x in intersections]) / len(intersections),
                        sum([x[1] for x in intersections]) / len(intersections),
                    )
                    print('intavg', intavg)
                    projt = [
                        (
                            i,
                            (
                                ((intavg[0] - p[0]) / v[0]),
                                ((intavg[1] - p[1]) / v[1]),
                            ),
                        )
                        for i, (p, v) in enumerate(projected)
                        if v[0] != 0 and v[1] != 0
                    ]
                    # print('projt', projt)
                    projt = [(i, (t[0] + t[1]) / 2) for i, t in projt]
                    linehail = [
                        (vecadd(hail[i][0], vecmul(hail[i][1], t)), t)
                        for i, t in projt
                    ]
                    # print('linehail', linehail)
                    diffs = [
                        (
                            vecsub(linehail[i][0], linehail[i + 1][0]),
                            linehail[i][1] - linehail[i + 1][1],
                        )
                        for i in range(len(linehail) - 1)
                    ]
                    avgvel = (
                        sum(dp[0] / dt for dp, dt in diffs) / len(diffs),
                        sum(dp[1] / dt for dp, dt in diffs) / len(diffs),
                        sum(dp[2] / dt for dp, dt in diffs) / len(diffs),
                    )

                    computedvels = [vecmul(dp, 1 / dt) for dp, dt in diffs]
                    # print('computedvels', computedvels)

                    start = [vecsub(p, vecmul(avgvel, t)) for p, t in linehail]
                    avgstart = (
                        sum(p[0] for p in start) / len(start),
                        sum(p[1] for p in start) / len(start),
                        sum(p[2] for p in start) / len(start),
                    )
                    # print('start', start)
                    print('avgvel:', avgvel)
                    print('avgstart:', avgstart)
                    print(
                        'sumavgstart:',
                        avgstart[0] + avgstart[1] + avgstart[2],
                    )

                    print(
                        'MINAREA',
                        minarea,
                        'Best xyz:',
                        f'({x}, {y}, {z}), ({iteri}, {iterj}, {iterk})',
                    )
                    # print(
                    #     'testanswer', normalized(vecsub((21, 14, 12), (24, 13, 10)))
                    # )
