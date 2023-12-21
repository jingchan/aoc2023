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


def solve(x, y, grid, i, visited, dist, steps=10000):
    q = [(x, y, i)]

    while len(q) > 0:
        x, y, i = q.pop(0)
        if i > steps:
            break
        if (x, y) in dist:
            continue
        if (x, y) in visited:
            continue
        if i % 2 == 1:
            visited[(x, y)] = i

        dist[(x, y)] = i

        for d in dirs:
            nx = x + d[0]
            ny = y + d[1]
            if nx < 0 or ny < 0 or nx >= len(grid[0]) or ny >= len(grid):
                continue
            if grid[ny][nx] == '.' or grid[ny][nx] == 'S':
                q.append((nx, ny, i + 1))
                # cache[(x, y)] = True
    return visited, dist


# def solve2(grid, steps, spot, d):
#     if spot == 5:
#         if steps > 130:


sg = []
with open(IN_FILE, 'r') as f:
    # line = f.readline()
    input = []
    total = 0
    ht = 0
    lt = 0
    grid = []
    for line in f.readlines():
        line = line.strip()
        grid.append(list(line))
    mid = (0, 0)
    for y, row in enumerate(grid):
        for x, c in enumerate(row):
            if c == 'S':
                mid = (x, y)

    width = len(grid[0])
    height = len(grid)
    print('width, height', width, height)

    sg = [
        [
            solve(0, 0, grid, 0, {}, {})[0],
            solve(0, 65, grid, 0, {}, {})[0],
            solve(0, 130, grid, 0, {}, {})[0],
        ],
        [
            solve(65, 0, grid, 0, {}, {})[0],
            solve(65, 65, grid, 0, {}, {})[0],
            solve(65, 130, grid, 0, {}, {})[0],
        ],
        [
            solve(130, 0, grid, 0, {}, {})[0],
            solve(130, 65, grid, 0, {}, {})[0],
            solve(130, 130, grid, 0, {}, {})[0],
        ],
    ]
    dg = [
        [
            solve(0, 0, grid, 0, {}, {})[1],
            solve(0, 65, grid, 0, {}, {})[1],
            solve(0, 130, grid, 0, {}, {})[1],
        ],
        [
            solve(65, 0, grid, 0, {}, {})[1],
            solve(65, 65, grid, 0, {}, {})[1],
            solve(65, 130, grid, 0, {}, {})[1],
        ],
        [
            solve(130, 0, grid, 0, {}, {})[1],
            solve(130, 65, grid, 0, {}, {})[1],
            solve(130, 130, grid, 0, {}, {})[1],
        ],
    ]

    for r in sg:
        for c in r:
            print(max(c.values()), end=' ')

        print()
    print()
    for r in [0, 65, 130]:
        for c in [0, 65, 130]:
            print(dg[1][1][r, c], end=' ')
        print()

    print()
    for r in [0, 1, 2]:
        for c in [0, 1, 2]:
            print(len(sg[r][c]), end=' ')
        print()

    print(max(sg[2][1].values()))
    print(sg[1][1][0, 129])

    # full coverage steps
    corner = len(sg[0][0])
    side = len(sg[0][1])
    print('cornerside', corner, side)
    steps = 26501365

    # 203854.66153846154
    # 203854 full squares
    halfwidth = (width - 1) / 2
    print(steps / width)
    print((steps + halfwidth) / width)
    # 202300.9923664122

    # print('fullboxes reached', (steps - (width - 1)) / width)
    # print('fullboxes reached', (steps + (width - 1) / 2) / width)
    print(
        'fullboxes reached', (steps - ((width - 1) / 2 + 1) - 195) / width + 1
    )
    fullboxes = math.floor((steps - ((width - 1) / 2 + 1) - 195) / width + 1)

    print('remain steps', steps + halfwidth - fullboxes * width)

    # top 130
    # top right1/left1 = halfwidth

    # Leth of full boxes
    lengths = (steps + halfwidth - (width - 1)) / width
    # print('lengths', lengths)

    # Gauss thing:  Sum between 1 to N: N*(N+1)/2
    n = (202299 * (202299 + 1) / 2) * 4
    print('n', n)
    print('n/4', n / 4)

    extraodds = 4 * ((fullboxes - 1) / 2 + 1)
    halfleft = (n - extraodds) / 2

    total = 0
    total += (halfleft + 1) * 7584  # even
    total += (halfleft + extraodds) * 7613  # odd

    # total += n / 2 * 7584  # eevn
    # total += n / 2 * 7613  # odd
    print('stepstaken', steps - 130)
    total += len(solve(0, 65, grid, 1, {}, {}, 131)[0]) * 1
    total += len(solve(130, 65, grid, 1, {}, {}, 131)[0]) * 1
    total += len(solve(65, 130, grid, 1, {}, {}, 131)[0]) * 1
    total += len(solve(65, 0, grid, 1, {}, {}, 131)[0]) * 1

    total += len(solve(0, 0, grid, 0, {}, {}, 195)[0]) * 202299
    total += len(solve(130, 130, grid, 0, {}, {}, 195)[0]) * 202299
    total += len(solve(0, 130, grid, 0, {}, {}, 195)[0]) * 202299
    total += len(solve(130, 0, grid, 0, {}, {}, 195)[0]) * 202299

    total += len(solve(0, 0, grid, 1, {}, {}, 65)[0]) * 202300
    total += len(solve(130, 130, grid, 1, {}, {}, 65)[0]) * 202300
    total += len(solve(0, 130, grid, 1, {}, {}, 65)[0]) * 202300
    total += len(solve(130, 0, grid, 1, {}, {}, 65)[0]) * 202300
    print(total)

# 202299
# 7584 spots from middle

# 26501365 steps
# 621949377792400 High
# 621944748153030 High
# 621944727930768.0
# 621944694745830 <--
# 621944700620114.0
# 621944700612530 X
# 621943965255900 Low
# 195
