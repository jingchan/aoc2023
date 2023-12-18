import math
import time
import os

PATH = os.path.dirname(__file__)
# IN_FILE = PATH + "/1.txt"
IN_FILE = PATH + "/2.txt"

print(IN_FILE)


def solve(x, y, dx, dy, grid, visited):
    next = [(x, y, dx, dy)]

    while len(next)>0:
        # print(next)
        x, y, dx, dy = next.pop(0)
        if x < 0 or y < 0 or x >= len(grid[0]) or y >= len(grid):
            continue
        if (x, y, dx, dy) in visited:
            continue

        visited.add((x, y, dx, dy))

        if grid[y][x] == '.':
            next.append((x+dx, y+dy, dx, dy))
        elif grid[y][x] == '/':
            next.append((x-dy, y-dx, -dy, -dx))
        elif grid[y][x] == '\\':
            next.append((x+dy, y+dx, dy, dx))
        elif grid[y][x] == '|':
            # print("s")
            if dx == 0:
                # print("s1")
                next.append((x+dx, y+dy, dx, dy))
            else:
                # print("s2")
                next.append((x-dy, y-dx, -dy, -dx))
                # print(next)
                next.append((x+dy, y+dx, dy, dx))
                # print(next)
        elif grid[y][x] == '-':
            if dy == 0:
                next.append((x+dx, y+dy, dx, dy))
            else:
                next.append((x-dy, y-dx, -dy, -dx))
                next.append((x+dy, y+dx, dy, dx))


with open(IN_FILE, "r") as f:
    total = 0
    # line = f.readline()
    grid = []
    for line in f.readlines():
        line = line.strip()
        grid.append(line)

    for i,g in enumerate(grid[0]):
        visited = set()
        solve(i, 0, 0, 1, grid, visited)
        visited2 = set()
        for k in visited:
            visited2.add((k[0], k[1]))
        # print(len(visited2))
        total = max(total, len(visited2))
        visited = set()

        solve(i, len(grid)-1-i, 0, -1, grid, visited)
        visited2 = set()
        for k in visited:
            visited2.add((k[0], k[1]))
        # print(len(visited2))
        total = max(total, len(visited2))
    for i,g in enumerate(grid):
        visited = set()
        solve(0, i, 1, 0, grid, visited)
        visited2 = set()
        for k in visited:
            visited2.add((k[0], k[1]))
        # print(len(visited2))
        total = max(total, len(visited2))
        visited = set()

        solve(len(grid[0])-1, i, -1, 0, grid, visited)
        visited2 = {(x,y) for (x,y,dx,dy) in visited}
        # visited2 = set()
        # for k in visited:
        #     visited2.add((k[0], k[1]))
        # print(len(visited2))
        total = max(total, len(visited2))

    # print(count)
    print(total)
# rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7
