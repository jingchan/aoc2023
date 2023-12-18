import math
import os

PATH = os.path.dirname(__file__)
# IN_FILE = PATH + "/1.txt"
IN_FILE = PATH + "/2.txt"

print(IN_FILE)

def solve(x, y, dx, dy, grid, visited):
    if x < 0 or y < 0 or x >= len(grid[0]) or y >= len(grid):
        return
    if visited.get((x, y, dx, dy)) is not None:
        return
    if grid[y][x] == '.':
        visited[(x, y, dx, dy)] = True
        solve(x+dx, y+dy, dx, dy, grid, visited)
    elif grid[y][x] == '/':
        # if \
        # new_dx = dy
        # new_dy = dx

        # if /
        # new_dx = -dy
        # new_dy = -dx
        visited[(x, y, -dy, -dx)] = True
        solve(x-dy, y-dx, -dy, -dx, grid, visited)
    elif grid[y][x] == '\\':
        visited[(x, y, dy, dx)] = True
        solve(x+dy, y+dx, dy, dx, grid, visited)
    elif grid[y][x] == '|':
        if dx == 0:
            visited[(x, y, dx, dy)] = True
            solve(x+dx, y+dy, dx, dy, grid, visited)
        else:
            visited[(x, y, -dy, -dx)] = True
            solve(x-dy, y-dx, -dy, -dx, grid, visited)
            visited[(x, y, dy, dx)] = True
            solve(x+dy, y+dx, dy, dx, grid, visited)
    elif grid[y][x] == '-':
        if dy == 0:
            visited[(x, y, dx, dy)] = True
            solve(x+dx, y+dy, dx, dy, grid, visited)
        else:
            visited[(x, y, -dy, -dx)] = True
            solve(x-dy, y-dx, -dy, -dx, grid, visited)
            visited[(x, y, dy, dx)] = True
            solve(x+dy, y+dx, dy, dx, grid, visited)


with open(IN_FILE, "r") as f:
    total = 0
    # line = f.readline()
    grid = []
    for line in f.readlines():
        line = line.strip()
        grid.append(line)

    visited = {}
    solve(0, 0, 1, 0, grid, visited)

    visited2 = set()
    for k in visited:
        visited2.add((k[0], k[1]))

    print(len(visited2))

    count =0
    for i,g in enumerate(grid):
        for j,c in enumerate(g):

            if (j, i) in visited2:
                count+=1
            if c == '.':
                if (j, i) in visited2:
                    print('x', end='')
                else:
                    print(c, end='')
            else:
                print(c, end='')
        print()




    print(total)
# rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7
