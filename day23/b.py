import math
import os
import re
import pickle
from itertools import combinations

PATH = os.path.dirname(__file__)
IN_FILE = PATH + '/1.txt'
# IN_FILE = PATH + '/2.txt'

DIRS = [(-1, 0, '^'), (1, 0, 'v'), (0, -1, '<'), (0, 1, '>')]


def solve(grid, x=1, y=0, dist=0, visited={}):
    maxdist = dist
    if x == len(grid) - 1:
        return dist
    for d in DIRS:
        nx = x + d[0]
        ny = y + d[1]
        if nx < 0:
            continue
        if grid[x + d[0]][y + d[1]] in ['#']:
            # if grid[x + d[0]][y + d[1]] not in ['.', d[2]]:
            continue
        if (x + d[0], y + d[1]) not in visited or visited[(nx, ny)] == False:
            visited[(x + d[0], y + d[1])] = True
            maxdist = max(
                maxdist, solve(grid, x + d[0], y + d[1], dist + 1, visited)
            )

            visited[(x + d[0], y + d[1])] = False
    print(x, y, maxdist)
    return maxdist


with open(IN_FILE, 'r') as f:
    # line = f.readline()
    grid = []
    for line in f.readlines():
        line = line.strip()
        grid.append(list(line))

    print(solve(grid))
