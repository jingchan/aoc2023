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
                print(y, i, score)
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
        grid.append(line)

    stops = [0 for x in grid[0]]
    it = [0 for x in grid[0]]
    for y, row in enumerate(grid):
        for i,c in enumerate(row):
            if c == 'O':
                score = len(grid) - (stops[i]+it[i])
                it[i] += 1
                print(y, i, score)
                total += score
            if c == '#':
                stops[i] = y + 1
                it[i] = 0

    print(weight(grid))
