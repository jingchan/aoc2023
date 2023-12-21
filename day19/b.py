import copy
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


def ints(i, j, inclusive=False):
    if not inclusive:
        return (
            (i[0] <= j[0] and i[1] >= j[0])
            or (i[0] <= j[1] and i[1] >= j[1])
            or (j[0] <= i[0] and j[1] >= i[0])
            or (j[0] <= i[1] and j[1] >= i[1])
        )
    else:
        return (
            (i[0] <= j[0] and i[1] >= j[0])
            or (i[0] <= j[1] and i[1] >= j[1])
            or (j[0] <= i[0] and j[1] >= i[0])
            or (j[0] <= i[1] and j[1] >= i[1])
            or (j[0] == i[1] + 1)
            or (i[0] == j[1] + 1)
        )


def union(rangelist):
    ret = []
    while len(rangelist) > 0:
        r = rangelist.pop(0)
        collected = []
        for i in range(len(rangelist)):
            if ints(r, rangelist[i], True):
                collected.append(rangelist[i])
                r = (
                    min(r[0], rangelist[i][0]),
                    max(r[1], rangelist[i][1]),
                )
        for c in collected:
            rangelist.remove(c)
        ret.append(r)
    return sort(ret)


def sort(rl):
    return sorted(rl, key=lambda x: x[0])


# def intersect(r1, r2):
#     r1 = union(r1)
#     r2 = union(r2)

#     ret = []
#     q = r1
#     while len(q) > 0:
#         nr = q.pop(0)
#         for i in range(len(r2)):
#             if ints(nr, r2[i]):
#                 ret.append(
#                     (
#                         max(nr[0], r2[i][0]),
#                         min(nr[1], r2[i][1]),
#                     )
#                 )
#     return ret


# def cut(op, num, rl):
#     ret = []
#     if op == '<':
#         for r in rl:
#             if num < r[0]:
#                 ret.append(r)
#             elif num < r[1]:
#                 ret.append((num, r[1]))
#     elif op == '>':
#         for r in rl:
#             if num > r[1]:
#                 ret.append(r)
#             elif num > r[0]:
#                 ret.append((r[0], num))
#     return ret


def solve(wf, cur='in', range=None):
    if range is None:
        range = {
            'x': (1, 4000),
            'a': (1, 4000),
            'm': (1, 4000),
            's': (1, 4000),
        }
    ret = []
    if cur == 'A':
        return [range]
    elif cur == 'R':
        return []

    for l, c, n, go in wf[cur]:
        if c == '<':
            nr = dict(range)
            nr[l] = (nr[l][0], n - 1)
            if not nr[l][0] > nr[l][1]:
                ret.extend(solve(wf, go, nr))
            range[l] = (n, range[l][1])
            if range[l][0] > range[l][1]:
                break
        elif c == '>':
            nr = dict(range)
            nr[l] = (n + 1, nr[l][1])
            if not nr[l][0] > nr[l][1]:
                ret.extend(solve(wf, go, nr))
            range[l] = (range[l][0], n)
            if range[l][0] > range[l][1]:
                break
        else:
            ret.extend(solve(wf, go, range))
    return ret


with open(IN_FILE, 'r') as f:
    # line = f.readline()
    input = []
    scores = []
    total = 0
    wf = {}
    i = 0
    lines = [l for l in f.readlines()]
    for line in lines:
        i += 1
        line = line.strip()
        if line == '':
            print('break')
            break

        wfn = line.split('{')[0]
        pcs = line.split('{')[1][:-1].split(',')
        procs = []
        for p in pcs:
            if ':' in p:
                p = p.split(':')
                if '<' in p[0]:
                    char = p[0].split('<')[0]
                    num = p[0].split('<')[1]
                    procs.append((char, '<', int(num), p[1]))
                else:
                    char = p[0].split('>')[0]
                    num = p[0].split('>')[1]
                    procs.append((char, '>', int(num), p[1]))
            else:
                procs.append((p, '=', 0, p))
        wf[wfn] = procs

    for line in lines[i:]:
        line = line.strip()
        print(line)
        line = line[1:-1].split(',')
        cur = {}
        for cs in line:
            cs = cs.split('=')
            cur[cs[0]] = int(cs[1])

    # soln = solve(wf, 'in')
    soln = solve(wf)
    print('soln', soln)

    total = 0
    for s in soln:
        total += math.prod([e - s + 1 for s, e in s.values()])

    # for k in ['x', 'a', 'm', 's']:
    # print(union([s[k] for s in soln]))
    # unioned = union([s[k] for s in soln])
    # total *= sum([s[k][1] - s[k][0] + 1 for s in soln])

    print('soln', soln)
    print('total', total)
#     # print([s[k] for s in soln])
#     for s in soln:
#         print(math.prod([e - s + 1 for s, e in s.values()]))

#     print('soln', soln)
#     print('total', total)
# 167409079868000
# 256000000000000
# 167409079868000
# 15353877894096
# 41307205860410
# 86528864213351
# 157308576137020800
