import math
import os
import re

PATH = os.path.dirname(__file__)
# IN_FILE = PATH + '/1.txt'
IN_FILE = PATH + '/2.txt'
# IN_FILE = PATH + '/3.txt'

dirs = [
    (1, 0),
    (0, 1),
    (-1, 0),
    (0, -1),
]

with open(IN_FILE, 'r') as f:
    # line = f.readline()
    input = []
    total = 0
    ht = 0
    lt = 0
    m = {}
    for line in f.readlines():
        line = line.strip()
        sec = line.split(' -> ')
        tar = sec[1].split(', ')

        if sec[0] == 'broadcaster':
            m[sec[0]] = ['b', tar]
        elif sec[0][0] == '%':
            m[sec[0][1:]] = ['%', tar, False]
        else:
            m[sec[0][1:]] = ['&', tar, {}]

    for k, v in m.items():
        if v[0] == '&':
            for kj, mj in m.items():
                if k in mj[1]:
                    v[2][kj] = False

    print(m)
    for i in range(0, 1000):
        q = [(False, 'broadcaster', 'sender')]
        lt += 1

        while len(q) > 0:
            sig, next, sender = q.pop(0)
            if next not in m:
                continue
            nm = m[next]
            if nm[0] == 'b':
                for n in nm[1]:
                    q.append((False, n, next))
                    lt += 1
            elif nm[0] == '%':
                if not sig:
                    if not nm[2]:  # low
                        nm[2] = True
                        for n in nm[1]:
                            q.append((True, n, next))
                            ht += 1
                    else:  # high
                        nm[2] = False
                        for n in nm[1]:
                            q.append((False, n, next))
                            lt += 1
            else:
                nm[2][sender] = sig

                allhigh = True
                for prevsig in nm[2].values():
                    if prevsig is False:
                        allhigh = False
                        break
                if allhigh:
                    for n in nm[1]:
                        q.append((False, n, next))
                        lt += 1
                else:
                    for n in nm[1]:
                        q.append((True, n, next))
                        ht += 1

    print(ht, lt)
    print(ht * lt)
