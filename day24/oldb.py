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


def veceq(v1, v2):
    return (v1[0] / v2[0] == v1[1] / v2[1] == v1[2] / v2[2]) or (
        v1[0] / v2[0] == v1[1] / v2[1] == v1[2] / v2[2]
    )


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

    # dist = 10000000000000000000000
    # mini, minj = 0, 0
    # for i, (p, v) in enumerate(st):
    #     for j, (p2, v2) in enumerate(st):
    #         if i >= j:
    #             continue
    #         if norm(diff(p, p2)) < dist:
    #             dist = norm(diff(p, p2))
    #             mini, minj = i, j
    #             print(dist, i, j)

    # print(mini, minj)
    # 120947065836941, 305
    # 519294682629929, -125)
    # print(
    #     sorted([(p[0], v[0]) for p, v in st if v[0] < 0], key=lambda x: -x[0])[
    #         0
    #     ]
    # )
    # print(
    #     sorted([(p[0], v[0]) for p, v in st if v[0] > 0], key=lambda x: x[0])[0]
    # )
    # thstep = 10000
    # phstep = 10000
    # mincross = 100000000000000
    # minp = (0, 0, 0)
    # for i in range(thstep):
    #     for j in range(phstep):
    #             x = math.sin(i / thstep * 2 * math.pi) * math.cos(
    #                 j / phstep * 2 * math.pi
    #             )
    #             y = math.cos(i / thstep * 2 * math.pi) * math.cos(
    #                 j / phstep * 2 * math.pi
    #             )
    #             z = math.sin(j / phstep * 2 * math.pi)
    #             p0 = normalized((x, y, z))

    #             match = True
    #             for k, (p, v) in enumerate(st):
    #                 p1 = normalized(p)
    #                 p2 = normalized(addvec(p, v))

    #                 if norm(crossproduct(p0, p1)) > norm(crossproduct(p0, p2)):
    #                     # count += 0
    #                     match = False
    #                     break
    #             if match:
    #                 print(p0)

    mincross = 100000000000000
    minp = (0, 0, 0)
    answers = []

    center = (364, 456, -830)
    chklen = 50
    time = 180925542072
    minval = math.inf

    CALCULATE_V0 = True
    minv = (math.inf, math.inf, math.inf)
    maxv = (-math.inf, -math.inf, -math.inf)
    minvn = (math.inf, math.inf, math.inf)
    maxvn = (-math.inf, -math.inf, -math.inf)
    if CALCULATE_V0:
        # for i in range(center[0] - chklen, center[0] + chklen):
        #     for j in range(center[1] - chklen, center[1] + chklen):
        #         for k in range(center[2] - chklen, center[2] + chklen):
        # for i in range(300, 400):
        #     for j in range(410, 540):
        #         for k in range(-1000, -730):
        for i in range(-1000, 1000):
            for j in range(-1000, 1000):
                for k in range(-1000, 1000):
                    if i == 0 and j == 0 and k == 0:
                        continue
                    p0 = normalized((i, j, k))

                    match = True
                    for _, (p, v) in enumerate(st):
                        p1 = normalized(p)
                        p2 = normalized(addvec(p, v))

                        if norm(crossproduct(p0, p1)) < norm(
                            crossproduct(p0, p2)
                        ):
                            # count += 0
                            match = False
                            break
                    if match:
                        print(p0, ':', i, j, k)
                        answers.append((i, j, k))
                        minv = (
                            min(minv[0], i),
                            min(minv[1], j),
                            min(minv[2], k),
                        )
                        maxv = (
                            max(maxv[0], i),
                            max(maxv[1], j),
                            max(maxv[2], k),
                        )
                        minvn = (
                            min(minvn[0], p0[0]),
                            min(minvn[1], p0[1]),
                            min(minvn[2], p0[2]),
                        )
                        maxvn = (
                            max(minvn[0], p0[0]),
                            max(minvn[1], p0[1]),
                            max(minvn[2], p0[2]),
                        )
        print(minv, maxv)
        print(minvn, maxvn)
    else:
        minvn = (0.32525747314895087, 0.44097360082933035, -0.8233140703616396)
        maxvn = (0.35545900335367153, 0.4525643451219678, -0.8178229701219811)

    print(answers)

    exit()
    print('normalized 1', normalized((336, 467, -824)))
    print('normalized 2', normalized((13, 17, -31)))
    print('normalized 3', normalized((286, 374, -683)))
    # 2.0967452990863777e-10 182483464836 (344, 451, -825)
    # 2.0961924145253275e-10 182483464835 (313, 412, -754)
    # 2.0956343019414014e-10 182483464835 (305, 403, -738)
    # 2.095095113022194e-10 182483464871 (374, 496, -909)
    # 2.0945601524914592e-10 182483465074 (365, 486, -891)
    # 2.094014980944664e-10 182483465277 (354, 473, -868)
    # 2.0940125133005194e-10 182483465470 (301, 402, -738)

    # last = (13, 17, -31)
    # last = (286, 374, -683)
    # last = (344, 451, -825)
    # last = (313, 412, -754)
    # last = (305, 403, -738)
    # last = (374, 496, -909)
    # last = (365, 486, -891)
    last = (301, 402, -738)
    lastn = normalized(last)
    rel = 0.001
    minvn = (
        0.3451057175812343 * (1 - rel),
        0.4512920922216141 * (1 - rel),
        -0.8229444034629433 * (1 + rel),
    )
    maxvn = (
        0.3451057175812343 * (1 + rel),
        0.4512920922216141 * (1 + rel),
        -0.8229444034629433 * (1 - rel),
    )
    print('minvn', minvn)
    print('maxvn', maxvn)
    answers = []

    # for i in range(1, 4400):
    #     for j in range(1, 6000):
    #         lastnormdiff = 0
    #         for k in range(-1, -10000, -1):
    multiplier = 10000
    band = 100
    for i in range(
        math.floor(multiplier * lastn[0]) - band,
        math.floor(multiplier * lastn[0]) + band,
    ):
        for j in range(
            math.floor(multiplier * lastn[1]) - band,
            math.floor(multiplier * lastn[1]) + band,
        ):
            for k in range(
                math.floor(multiplier * lastn[2]) - band,
                math.floor(multiplier * lastn[2]) + band,
            ):
                nv = normalized((i, j, k))
                cos = dotproduct(nv, normalized(last))
                # print(diff(nv, normalized(last)))
                if cos < 0.9999999:
                    continue

                alreadyhas = False
                for a in answers:
                    if veceq((i, j, k), a):
                        alreadyhas = True

                if not alreadyhas:
                    answers.append((i, j, k))
                    # adiff = norm(
                    #     diff(normalized((i, j, k)), normalized(last))
                    # )
                    print((i, j, k), 'cos:', cos)

    print(answers)
    print(len(answers))

    fastest = sorted(
        [(i, norm(v)) for i, (p, v) in enumerate(st)], key=lambda x: -x[1]
    )[0]
    # fastest = sorted(
    #     [(i, norm(v)) for i, (p, v) in enumerate(st)], key=lambda x: x[1]
    # )[0]
    print('fastest', fastest)
    # 209564909278430435852 182483464640 (13, 17, -31)
    # answers = [(130, 170, -310)]
    pf, vf = st[fastest[0]]
    print(pf, vf)
    # 2097791397 33221807643 (336, 467, -824)
    # -420261568 33221807644 (336, 467, -824)
    minval = math.inf
    for i in range(182483464834, 182483465630, 1):
        # for i in range(182483465080, 182483466075, 1):
        p1 = addvec(pf, mult(vf, i))
        for v1 in answers:
            p2 = addvec(p1, v1)
            valtotal = 0
            for _, (p3, v3) in enumerate(st):
                valtotal += abs(coplanar_value(p1, p2, p3, addvec(p3, v3)))
            if valtotal < minval:
                minval = valtotal
                print(minval, i, v1)
    exit()

    center = (330, 437, -781)
    chklen = 50
    time = 180925542072
    minval = math.inf
    for i in range(center[0] - chklen, center[0] + chklen):
        for j in range(center[1] - chklen, center[1] + chklen):
            for k in range(center[2] - chklen, center[2] + chklen):
                p1 = addvec(pf, mult(vf, time))
                p2 = addvec(p1, (i, j, k))
                valtotal = 0
                for _, (p3, v3) in enumerate(st):
                    valtotal += abs(coplanar_value(p1, p2, p3, addvec(p3, v3)))
                if valtotal < minval:
                    minval = valtotal
                    print(minval, (i, j, k))
                    # print(minval, (i, j, k), v1)

    # for v0 in answers:
    #     count = 0
    #     for _, (p, v) in enumerate(st):
    #         for _, (p2, v2) in enumerate(st):
    #             if (dotproduct(normalized(v0), normalized(v))) > 0:
    #                 count += 1

    # mindiff = 100000000
    # for i in range(1, 100000):
    #     diff = 0
    #     diff += abs(round(i * 0.3364991373284372) - i * 0.3364991373284372)
    #     diff += abs(
    #         round(
    #             i * 0.4649920009718842,
    #         )
    #         - i * 0.4649920009718842
    #     )
    #     diff += abs(round(i * -0.8188716441600483) - i * -0.8188716441600483)
    #     if diff < mindiff:
    #         mindiff = diff
    #         print(
    #             i * 0.3364991373284372,
    #             i * 0.4649920009718842,
    #             i * -0.8188716441600483,
    #         )

    # i*0.4649920009718842, i*-0.8188716441600483)
    # print(i*0.3364991373284372, i*0.4649920009718842, i*-0.8188716441600483)
    # (0.3347279807895764, 0.4650007280335906, -0.8195922777849751)
    # (0.33380350870446335, 0.46248961865133287, -0.8213881970276502)
    # (0.3364991373284372, 0.4649920009718842, -0.8188716441600483)
    # (-0.3419906002147191, -0.45968568344034055, 0.8195922777849748)
    # (-0.34437742446510883, -0.46047283241916914, 0.8181497174250237)
    # (-0.35470409146930276, -0.45256606962110013, 0.8181497174250237)
    # (0.35706625590215857, 0.44741728543805265, -0.8199521093254524)
    # (-0.3675904596486923, -0.4381393667825546, 0.820311617161823)

    # for i, (p, v) in enumerate(st):
    #     for j, (p2, v2) in enumerate(st):
    #         if i >= j:
    #             continue
    #         if norm(diff(p, p2)) == dist:
    #             print(p, v, p2, v2)
    # maxcount = 0
    # for i in range(-100, 100):
    #     for j in range(-100, 100):
    #         for k in range(-100, 100):
    #             v0 = (i, j, k)
    #             # print(v0)
    #             count = 0
    #             for _, (p, v) in enumerate(st):
    #                 if (dotproduct(normalized(v0), normalized(v))) > 0:
    #                     count += 1
    #             if count > maxcount:
    #                 maxcount = count
    #                 print(v0, count)
    #             # print('>0', count)
    #             # print('<0', len(st) - count)

    # p1, v1 = st[56]
    # p3, v3 = st[85]

    # for i in range(1, 1000000):
    #     if i % 1000 == 0:
    #         print('checking i:', i)
    #     for j in range(1, i):
    #         p2 = addvec(p1, mult(v1, i))
    #         p4 = addvec(p3, mult(v3, j))
    #         if coplanar(p1, p2, p3, p4):
    #             # pass
    #             print(p1, p2, p3, p4, i, j)
    # else:
    # print(p1, p2, p3, p4, i, j)
    # cols += 1
    # break

    # for i, (p, v) in enumerate(st):
    #     for j, (p2, v2) in enumerate(st):
    #         if i == j:
    #             continue
    #         if i > j:
    #             continue

    #         for k, (p3, v3) in enumerate(st):
    #             if k == i or k == j:
    #                 continue
    #             if coplanar(p, p2, p3, addvec(p3, v3)):
    #                 cols += 1
    #                 break

    #         cols += 1
    # print(cols)


# 31098.547424316406 182483464630 (13, 17, -31)
# 31097.431816101074 182483464630 (94, 123, -224)
# 31097.233772277832 182483464630 (107, 140, -255)
# 31095.994270324707 182483464630 (168, 220, -401)
# 31095.331199645996 182483464630 (171, 224, -408)
# 31095.255783081055 182483464630 (287, 376, -685)
# 31095.17251586914 182483464630 (300, 393, -716)
# 31095.06056213379 182483464632 (171, 224, -408)
# 31095.005752563477 182483464632 (287, 376, -685)
# 31094.932586669922 182483464635 (287, 376, -685)
# 31094.9220123291 182483464637 (300, 393, -716)
# 31094.792251586914 182483464643 (287, 376, -685)
# 31094.73651123047 182483464680 (287, 376, -685)
# 31094.55972290039 182483464781 (287, 376, -685)
