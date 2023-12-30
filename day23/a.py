import math
import os
import re
import pickle
from itertools import combinations

PATH = os.path.dirname(__file__)
# IN_FILE = PATH + '/1.txt'
IN_FILE = PATH + '/2.txt'

DIRS = [(-1, 0, '^'), (1, 0, 'v'), (0, -1, '<'), (0, 1, '>')]


def solve3(adj, end, cur=(0, 1), path=set(), dist=0):
    path.add(cur)
    maxd = -1
    if cur == end:
        return dist
    for s, e in adj:
        if s == cur:
            if e not in path:
                maxd = max(
                    maxd, solve3(adj, end, e, path.copy(), dist + adj[(s, e)])
                )
    return maxd


def solve2(grid, intersections, dists, x=0, y=1, last=None, dist=0):
    q = [(x, y, dist, last, {(0, 1)})]
    while len(q) > 0:
        x, y, dist, last, path = q.pop(0)

        if (x, y) in intersections:
            if last is not None:
                if (last, (x, y)) not in dists:
                    dists[(last, (x, y))] = dist
                    dists[((x, y), last)] = dist
                else:
                    dists[(last, (x, y))] = max(dist, dists[(last, (x, y))])
                    dists[((x, y), last)] = max(dist, dists[(last, (x, y))])
                    continue
            last = (x, y)
            dist = 0
        for d in DIRS:
            nx = x + d[0]
            ny = y + d[1]
            if nx < 0 or nx >= len(grid):
                continue
            if grid[x + d[0]][y + d[1]] in ['#']:
                continue
            if (x + d[0], y + d[1]) == last:
                continue
            if (x + d[0], y + d[1]) not in path:
                # visited.add((x + d[0], y + d[1]))
                q.append(
                    (
                        x + d[0],
                        y + d[1],
                        dist + 1,
                        last,
                        path | {(x + d[0], y + d[1])},
                    ),
                )
                # solve2(
                #     grid,
                #     intersections,
                #     dists,
                #     x + d[0],
                #     y + d[1],
                #     last,
                #     dist + 1,
                #     visited.union({(x + d[0], y + d[1])}),
                # )


def solve(grid, x=1, y=0, dist=0, visited={}):
    intersections = set()

    q = [(x, y, dist)]
    while len(q) > 0:
        x, y, dist = q.pop(0)
        isintersection = False
        num = 0
        for d in DIRS:
            nx = x + d[0]
            ny = y + d[1]
            if nx < 0 or nx >= len(grid):
                continue
            if grid[x + d[0]][y + d[1]] in ['#']:
                # if grid[x + d[0]][y + d[1]] not in ['.', d[2]]:
                continue
            num += 1
        if num > 2:
            intersections.add((x, y))
            isintersection = True
        for d in DIRS:
            nx = x + d[0]
            ny = y + d[1]
            if nx < 0 or nx >= len(grid):
                continue
            if grid[x + d[0]][y + d[1]] in ['#']:
                # if grid[x + d[0]][y + d[1]] not in ['.', d[2]]:
                continue
            if (x + d[0], y + d[1]) not in visited:
                visited[(x + d[0], y + d[1])] = True
                if isintersection:
                    q.append((x + d[0], y + d[1], 1))
                else:
                    q.append((x + d[0], y + d[1], dist + 1))
    return intersections


with open(IN_FILE, 'r') as f:
    # line = f.readline()
    grid = []
    for line in f.readlines():
        line = line.strip()
        grid.append(list(line))

    intersections = solve(grid)
    intersections.add((0, 1))
    intersections.add((len(grid) - 1, len(grid[0]) - 2))

    print(intersections)
    dists = {}
    solve2(grid, intersections, dists)
    print('dists')
    print(dists)

    print(solve3(dists, ((len(grid) - 1, len(grid[0]) - 2))))

    # for i in intersections:
    #     for j in intersections:
    #         if (i, j) not in dists:
    #             dists[(i, j)] = -math.inf

    # for k in intersections:
    #     for i in intersections:
    #         for j in intersections:
    #             if dists[(i, j)] < dists[(i, k)] + dists[(k, j)]:
    #                 dists[(i, j)] = dists[(i, k)] + dists[(k, j)]

    # print(dists)

    # print(dists[((0, 1), (len(grid) - 1, len(grid[0]) - 2))])
