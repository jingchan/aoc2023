import math
import os

PATH = os.path.dirname(__file__)
# IN_FILE = PATH + "/1.txt"
IN_FILE = PATH + "/2.txt"
print(IN_FILE)

# O....#....
# O.OO#....#
# .....##...
# OO.#O....O
# .O.....O#.
# O.#..O.#.#
# ..O..#O..O
# .......O..
# #....###..
# #OO..#....
# 1000000000 cycles
def weight(grid):
    total = 0
    stops = [0 for x in grid[0]]
    it = [0 for x in grid[0]]
    for y, row in enumerate(grid):
        for i,c in enumerate(row):
            if c == 'O':
                score = len(grid) - (stops[i]+it[i])
                it[i] += 1
                # print(y, i, score)
                total += score
            if c == '#':
                stops[i] = y + 1
                it[i] = 0
    return total

with open(IN_FILE, "r") as f:
    total = 0
    # line = f.readline()
    grid = []
    for line in f.readlines():
        line = line.strip()
        line = [x for x in line]
        grid.append(line)

    stops = [0 for x in grid[0]]
    it = [0 for x in grid[0]]
    rocks = set()
    rprev = []
    rcyc = []
    for y, row in enumerate(grid):
        for i, c in enumerate(row):
            if c == 'O':
                rocks.add((i, y))
                grid[y][i] = '.'
    rprev.append({r for r in rocks})

    print("numorcks",len(rocks))

    def move(x, y, d, rocks):
        # Turn direction number into delta vector
        if d == 0:
            d = [0, -1]
        elif d == 1:
            d = [-1, 0]
        elif d == 2:
            d = [0, 1]
        elif d == 3:
            d = [1, 0]

        # Move until hit a wall, rock, or edge.
        while True:
            nx = x+d[0]
            ny = y+d[1]
            if nx < 0 or ny < 0 or nx >= len(grid[0]) or ny >= len(grid):
                break
            if grid[ny][nx] == '#':
                break
            if (nx, ny) in rocks:
                break
            x = nx
            y = ny

        # Return new position
        return (x,y)

    jumped = False
    i = 0
    while i < 1000000000:
        dir = 0
        nrocks = set()
        for y in range(len(grid)):
            for x in range(len(grid[0])):
                if (x, y) in rocks:
                    nrocks.add(move(x, y, dir, rocks.union(nrocks)))
                    rocks.remove((x, y))
        dir = 1
        rocks = nrocks
        nrocks = set()
        for x in range(len(grid[0])):
            for y in range(len(grid)):
                if (x, y) in rocks:
                    nrocks.add(move(x, y, dir, rocks.union(nrocks)))
                    rocks.remove((x, y))
        dir = 2
        rocks = nrocks
        nrocks = set()
        for y in range(len(grid)):
            for x in range(len(grid[0])):
                ny = len(grid)-y-1
                if (x, ny) in rocks:
                    nrocks.add(move(x, ny, dir, rocks.union(nrocks)))
                    rocks.remove((x, ny))
        dir = 3
        rocks = nrocks
        nrocks = set()
        for x in range(len(grid[0])):
            for y in range(len(grid)):
                nx = len(grid[0])-x-1
                if (nx, y) in rocks:
                    nrocks.add(move(nx, y, dir, rocks.union(nrocks)))
                    rocks.remove((nx, y))
        i+= 1

        rocks = nrocks
        print('nrocks', i, len(rocks))
        # print({r for r in rocks})

        if {r for r in rocks} in rprev:
            # index of item in list
            cycle = i - rprev.index({r for r in rocks})
            print('cycle', i)
            # cycle = i
            # increase i by cycles whiel still elss than 1000000000
            while i+1000*cycle < 1000000000-10:
                i += 1000*cycle
            while i+cycle < 1000000000-10:
                i += cycle
            print('i now', i)

        rprev.append({r for r in rocks})

    for r in rocks:
        grid[r[1]][r[0]] = 'O'

    # for row in grid:
    #     print(row)

    # print(weight(grid))
    print(len(grid))

    total = 0
    for r in rocks:
        total += len(grid) - r[1]

        # Placeholder


    print(total)
# 95274
# 95267
273
