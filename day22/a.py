import math
import os
import re
import pickle
from itertools import combinations

PATH = os.path.dirname(__file__)
# IN_FILE = PATH + '/1.txt'
IN_FILE = PATH + '/2.txt'

# 1,0,1~1,2,1
# 0,0,2~2,0,2
# 0,2,3~2,2,3
# 0,0,4~0,2,4
# 2,0,5~2,2,5
# 0,1,6~2,1,6
# 1,1,8~1,1,9


def solve(bricks, sup, dets, cache):
    # print('dets', dets)
    dets = frozenset(dets)
    if dets in cache:
        return cache[dets]
    # print(dets)

    ret = set(dets)

    for c in cache:
        if c.issubset(dets):
            ret = ret.union(cache[c])

    for k, v in sup.items():
        if k in dets:
            continue
        if k in ret:
            continue
        if v.issubset(ret):
            ret.add(k)

            ret = ret.union(
                solve(
                    bricks,
                    sup,
                    dets
                    | {
                        k,
                    },
                    cache,
                )
            )
    # print('ret', ret)
    cache[dets] = ret
    return ret


# SAVE_DATA = True
SAVE_DATA = False

with open(IN_FILE, 'r') as f:
    # line = f.readline()
    input = []
    total = 0
    ht = 0
    lt = 0
    grid = []
    visited = {}
    bricks = []
    bricks2 = []
    sup = {}
    if SAVE_DATA:
        for line in f.readlines():
            line = line.strip()
            a, b, c = line.split('~')[0].split(',')
            d, e, f = line.split('~')[1].split(',')
            a, b, c, d, e, f = int(a), int(b), int(c), int(d), int(e), int(f)
            dist = d - a + e - b + f - c
            points = []
            for i in range(dist + 1):
                if dist == 0:
                    points.append([a, b, c])
                    continue
                points.append(
                    [
                        (d - a) / dist * i + a,
                        (e - b) / dist * i + b,
                        (f - c) / dist * i + c,
                    ]
                )
            bricks.append(points)
        for b in bricks:
            maxp = [b[0][0], b[0][1], b[0][2]]
            minp = [b[0][0], b[0][1], b[0][2]]
            for p in b:
                px, py, pz = p
                maxp[0] = max(maxp[0], px)
                maxp[1] = max(maxp[1], py)
                maxp[2] = max(maxp[2], pz)
                minp[0] = min(minp[0], px)
                minp[1] = min(minp[1], py)
                minp[2] = min(minp[2], pz)

            bricks2.append((minp, maxp))
        bricks = sorted(bricks, key=lambda x: min([p[2] for p in x]))
        while len(sup) < len(bricks):
            print('suppeorted', len(sup))
            for bi, b in enumerate(bricks):
                if bi not in sup:
                    sups = set()
                    for px, py, pz in b:
                        for bi2, b2 in enumerate(bricks):
                            # if bricks2[bi2][1][2] < bricks2[bi][0][2] - 1:
                            #     continue
                            if bi2 == bi:
                                continue
                            if pz - 1 == 0:
                                sups.add(-1)
                                continue

                            for px2, py2, pz2 in b2:
                                if (
                                    (px == px2)
                                    and (py == py2)
                                    and (pz == pz2 + 1)
                                ):
                                    sups.add(bi2)
                    if len(sups) == 0:
                        for i in range(len(bricks[bi])):
                            bricks[bi][i][2] -= 1
                        rem = []
                        for k, v in sup.items():
                            if bi in v:
                                rem.append(k)
                        for r in rem:
                            del sup[r]
                    else:
                        sup[bi] = sups

    if SAVE_DATA:
        pass
        # with open('bricks.pkl', 'wb') as file:
        #     pickle.dump(bricks, file)
        # with open('sup.pkl', 'wb') as file:
        #     pickle.dump(sup, file)
    else:
        with open('bricks.pkl', 'rb') as file:
            bricks = pickle.load(file)
        with open('sup.pkl', 'rb') as file:
            sup = pickle.load(file)

    ans = {}
    count = 0
    onlysup = set()
    print('aweiofjaa')
    print(sup)
    for i in sup:
        if len(sup[i]) == 1:
            if sup[i] != -1:
                onlysup = onlysup.union(sup[i])

    print(set(range(len(bricks))) - onlysup)
    print(len(set(range(len(bricks))) - onlysup))

    print('onlysup', onlysup)

    sortedsup = sorted(onlysup, key=lambda x: -min([p[2] for p in bricks[x]]))
    # print(sortedsup)
    # exit()
    print('num ', len(onlysup))
    total = 0
    cache = {}
    for i, s in enumerate(sortedsup):
        print('solving', i, s)
        if s == -1:
            continue
        add = (
            len(
                solve(
                    bricks,
                    sup,
                    {
                        s,
                    },
                    cache,
                )
            )
            - 1
        )
        print(s, add)

        total += add
    print(total)

    # print(bricks)
    # print(sup)
    # print(count)

# 21691
# 21691 L
# 9241 L
