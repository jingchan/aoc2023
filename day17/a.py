import math
import os
import re

PATH = os.path.dirname(__file__)
# IN_FILE = PATH + '/1.txt'
IN_FILE = PATH + "/2.txt"

dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]


def solve(x, y, d, c, grid, heat, ph):
    # print('nextg', x, y, d, c, heat)
    # if (x, y) not in ph:
    #     ph[(x, y)] = heat
    # else:
    #     if ph[(x, y)] < heat:
    #         return
    #     ph[(x, y)] = min(ph[(x, y)], heat)
    q = [(x, y, d, c)]
    heat = 0
    ph[(x, y, d, c)] = 0

    while len(q) > 0:
        x, y, d, c = q.pop(0)
        if (x, y, d, c) in ph:
            heat = ph[(x, y, d, c)]

        nd = d
        nx = x + dirs[nd][0]
        ny = y + dirs[nd][1]
        if nx >= 0 and nx < len(grid[0]) and ny >= 0 and ny < len(grid):
            if c < 3:
                c += 1
                nheat = heat + int(grid[ny][nx])
                if ((nx, ny, nd, c) not in ph) or (ph[(nx, ny, nd, c)] > nheat):
                    ph[(nx, ny, nd, c)] = nheat
                    q.append((nx, ny, nd, c))

                    # solve(nx, ny, nd, c, grid, nheat, ph)

        nd = (d + 1) % 4
        nx = x + dirs[nd][0]
        ny = y + dirs[nd][1]
        nc = 1
        if nx >= 0 and nx < len(grid[0]) and ny >= 0 and ny < len(grid):
            nheat = heat + int(grid[ny][nx])
            if ((nx, ny, nd, nc) not in ph) or (ph[(nx, ny, nd, nc)] > nheat):
                ph[(nx, ny, nd, nc)] = nheat
                q.append((nx, ny, nd, nc))

        nd = ((d - 1) + 4) % 4
        nx = x + dirs[nd][0]
        ny = y + dirs[nd][1]
        nc = 1
        if nx >= 0 and nx < len(grid[0]) and ny >= 0 and ny < len(grid):
            nheat = heat + int(grid[ny][nx])
            if ((nx, ny, nd, nc) not in ph) or (ph[(nx, ny, nd, nc)] > nheat):
                ph[(nx, ny, nd, nc)] = nheat
                q.append((nx, ny, nd, nc))


with open(IN_FILE, 'r') as f:
    # line = f.readline()
    grid = []
    ph = {}
    scores = []
    for line in f.readlines():
        line = line.strip()
        grid.append(line)
    solve(0, 0, 0, 0, grid, 0, ph)
    print(ph)
    minheat = 9999999999
    for k, h in ph.items():
        # print(k, h)
        if k[0] == len(grid[0]) - 1 and k[1] == len(grid) - 1:
            print(k, h)
            minheat = min(minheat, int(h))
    print(minheat)

    # for k, h in ph.items():
    #     # print(k, h)
    #     if k[0] in [11, 12, 13] and k[1] in [11, 12, 13]:
    #         print(k, h)
