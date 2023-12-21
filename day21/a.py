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


def solve(x, y, grid, i, steps, visited, cache={}):
    # if (x, y) in cache:
    # return cache[(x, y)]
    q = [(x, y, 0)]

    while len(q) > 0:
        x, y, i = q.pop(0)
        if (x, y) in visited:
            continue
        if i == steps:
            if (x, y) not in visited:
                visited[(x, y)] = []
            visited[(x, y)].append(i)
            continue
        if (steps - i) % 2 == 0:
            if (x, y) not in visited:
                visited[(x, y)] = []
            visited[(x, y)].append(i)

        for d in dirs:
            nx = x + d[0]
            ny = y + d[1]
            if nx < 0 or ny < 0 or nx >= len(grid[0]) or ny >= len(grid):
                continue
            if grid[ny][nx] == '.':
                q.append((nx, ny, i + 1))
                # cache[(x, y)] = True


with open(IN_FILE, 'r') as f:
    # line = f.readline()
    input = []
    total = 0
    ht = 0
    lt = 0
    grid = []
    visited = {}
    for line in f.readlines():
        line = line.strip()
        grid.append(list(line))
        # visited.append([] * len(line))
    print(len(grid), len(grid[0]))
    for y, row in enumerate(grid):
        for x, c in enumerate(row):
            if c == 'S':
                print(x, y)
                exit()
                solve(x, y, grid, 0, 64, visited)

    total = 0
    print(visited)
    print(len(visited))
