import math
import os

PATH = os.path.dirname(__file__)
# IN_FILE = PATH + "/1.txt"
IN_FILE = PATH + "/2.txt"
print(IN_FILE)


def pf(d, c, m, len):
    for k in d.keys():
        st = k
        cur = k
        for i in range(len):
            if m[i % len] == "L":
                cur = d[cur][0]
            else:
                cur = d[cur][1]
            if cur == "ZZZ":
                break

        c[st] = (cur, i + 1)


with open(IN_FILE, "r") as f:
    total = 0
    m = f.readline()
    line = f.readline()
    d = dict()
    cur = "AAA"
    for line in f.readlines():
        line = line.split()
        pos = line[0]
        l = line[2][1:4]
        r = line[3][0:3]
        d[pos] = (l, r)
    c = dict()
    pf(d, c, m, len(m) - 1)
    i = 0
    print(cur)
    print(c)
    # print(c[cur], c["MGD"])
    # print(c[cur], c["A"])
    last = cur
    visited = set()
    while c[cur][0] != "ZZZ":
        new_c = dict()
        print("first:", c[cur])
        print("ended:", len([k for k in c.values() if k[0] == "ZZZ"]))
        for k in d.keys():
            end = c[k][0]
            steps = c[k][1]
            if end == "ZZZ":
                new_c[k] = c[k]
                # print("end", k, c[k])
                continue
            new_end = c[end][0]
            new_steps = c[end][1]
            new_c[k] = (new_end, steps + new_steps)
        # if c[cur][0] in visited:
        #     print(c["KHP"])
        #     print("done first:", c[cur])
        #     exit()
        # else:
        # visited.add(c[cur][0])
        c = new_c
        # if new_c[cur][0] == last:
        #     break
        # else:
        #     last = cur
        # c = new_c

        # print(c[cur])

    print("first:", c[cur])
    # print(cur)

    print(i)

# # a mod b
# x = a % b
