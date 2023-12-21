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
        print(wfn, procs)
    print(wf)

    for line in lines[i:]:
        line = line.strip()
        print(line)
        line = line[1:-1].split(',')
        cur = {}
        for cs in line:
            cs = cs.split('=')
            cur[cs[0]] = int(cs[1])

        ptr = 'in'
        while True:
            print(ptr)
            if ptr == 'A':
                total += cur['x']
                total += cur['m']
                total += cur['a']
                total += cur['s']
                break
            if ptr == 'R':
                break

            cwf = wf[ptr]

            for proc in cwf:
                if proc[1] == '<':
                    if cur[proc[0]] < proc[2]:
                        ptr = proc[3]
                        break
                elif proc[1] == '>':
                    if cur[proc[0]] > proc[2]:
                        ptr = proc[3]
                        break
                else:
                    ptr = proc[3]
                    break
    print(total)

    # print((count1, count2))
    # print(min(count1, count2))

    # print(max(scores))
