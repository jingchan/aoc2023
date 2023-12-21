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
    width = len(grid[0])
    height = len(grid)
    locs = 0
    plocs = 0
    pplocs = 0
    ppplocs = 0
    pdelt = 0
    ppdelt = 0
    # if (x, y) in cache:
    # return cache[(x, y)]
    q = [(x, y, 0, 0, 0)]
    tiles = {}

    while len(q) > 0:
        prev_i = i
        x, y, i, tx, ty = q.pop(0)

        if i > prev_i:
            visiteds = [v for v in tiles.values()]
            locs = sum([len(v) for v in visiteds])
            print(
                'step',
                i,
                ':',
                locs,
                '\tdelta:',
                locs - plocs,
                '\tdelta2:',
                (locs - plocs) - ppdelt,
            )
            ppdelt = pdelt
            pdelt = locs - plocs
            plocs = locs

        if (tx, ty) not in tiles:
            tiles[(tx, ty)] = {}
        visited = tiles[(tx, ty)]
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
            ntx = tx
            nty = ty
            if nx < 0 or ny < 0 or nx >= len(grid[0]) or ny >= len(grid):
                if nx < 0:
                    ntx = tx - 1
                if ny < 0:
                    nty = ty - 1
                if nx >= width:
                    ntx = tx + 1
                if ny >= height:
                    nty = ty + 1
                nx = (nx + width) % width
                ny = (ny + height) % height
                q.append((nx, ny, i + 1, ntx, nty))
                continue
            if grid[ny][nx] == '.':
                q.append((nx, ny, i + 1, ntx, nty))
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
                # print(x, y)
                # exit()
                solve(x, y, grid, 0, 6400000, visited)

    total = 0
    print(visited)
    print(len(visited))
