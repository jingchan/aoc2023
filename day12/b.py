import math
import os

PATH = os.path.dirname(__file__)
# IN_FILE = PATH + "/1.txt"
IN_FILE = PATH + "/2.txt"
print(IN_FILE)

with open(IN_FILE, "r") as f:
    total = 0
    # line = f.readline()
    grid = []
    for line in f.readlines():
        grid.append([x for x in line][:-1])
    rows = len(grid)
    cols = len(grid[0])

    print(total)
