import math
import os

PATH = os.path.dirname(__file__)
# IN_FILE = PATH + "/1.txt"
IN_FILE = PATH + "/2.txt"
print(IN_FILE)

with open(IN_FILE, "r") as f:
    total = 0
    # line = f.readline()
    grid = []
    er = []
    ec = []
    map = []
    for line in f.readlines():
        grid.append([x for x in line][:-1])
    rows = len(grid)
    cols = len(grid[0])

    for i in range(rows):
        for j in range(cols):
            if grid[i][j] != '.':
                # map[grid[i][j]] = (i,j)
                map.append((i,j))

    for i in range(rows):
        empty = True
        for j in range(cols):
            if grid[i][j] != '.':
                empty = False
        if empty:
            er.append(i)
    for i in range(cols):
        empty = True
        for j in range(rows):
            if grid[j][i] != '.':
                empty = False
        if empty:
            ec.append(i)

    print(map)
    for i, g1p in enumerate(map):
        for j, g2p in enumerate(map):
            if not i<j:
                continue
    # for g1i, g1p in map.items():
    #     for g2i, g2p in map.items():
            total += max(g2p[0], g1p[0]) - min(g2p[0], g1p[0])
            total += max(g2p[1], g1p[1]) - min(g2p[1], g1p[1])
            total += sum([999999 for i in er if i > min(g1p[0], g2p[0]) and i < max(g1p[0], g2p[0])])
            total += sum([999999 for i in ec if i > min(g1p[1], g2p[1]) and i < max(g1p[1], g2p[1])])






    print(total)
