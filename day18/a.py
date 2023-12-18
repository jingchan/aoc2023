import math
import os
import re

PATH = os.path.dirname(__file__)
# IN_FILE = PATH + '/1.txt'
IN_FILE = PATH + "/2.txt"

# dirs = {
#   "R": (1, 0),
#   "D": (0, 1),
#   "L": (-1, 0),
#   "U": (0, -1),
# }
dirs = [
  (1, 0),
  (0, 1),
  (-1, 0),
  (0, -1),
]
di = {
  "R": 0,
  "D": 1,
  "L": 2,
  "U": 3,
}
dirlist = ["R", "D", "L", "U"]

grid1 = {}
grid2 = {}

with open(IN_FILE, 'r') as f:
    # line = f.readline()
    input = []
    scores = []
    for line in f.readlines():
        line = line.strip()
        d= line.split(" ")[0]
        l= line.split(" ")[1]
        hex = line.split(" ")[2]
        input.append((di[d], int(l), hex))


    cur = (0, 0)
    grid1[cur] = True
    grid2[cur] = True
    tg = {}
    dg = {}
    for i in range(len(input)+2):
        (d, l, hex) = input[(i)%len(input)]
        (ld, ll, lhex) = input[((i-1)+len(input))%len(input)]

        for j in range(l):
            dg[cur] = d
            if d in [0, 2]:
                tg[cur] = "H"
            else:
                tg[cur] = "V"

            grid1[cur] = True
            grid2[cur] = True
            if j == 0:
                if ((d-ld)+4)%4 == 1:
                    # right
                    tg[cur] = "R"
                    curr = (cur[0] + dirs[(d+1)%4][0], cur[1] + dirs[(d+1)%4][1])
                    grid1[curr] = True
                    curl = (cur[0] + dirs[((d-1)+4)%4][0], cur[1] + dirs[((d-1)+4)%4][1])
                    grid2[curl] = True
                    curl = (cur[0] + dirs[d][0] + dirs[((d-1)+4)%4][0], cur[1] + dirs[d][1]+ dirs[((d-1)+4)%4][1])
                    grid2[curl] = True
                else:
                    # left
                    tg[cur] = "L"
                    curr = (cur[0] + dirs[(d+1)%4][0], cur[1] + dirs[(d+1)%4][1])
                    grid1[curr] = True
                    curr = (cur[0] + dirs[d][0] + dirs[((d+1)+4)%4][0], cur[1] + dirs[d][1]+ dirs[((d+1)+4)%4][1])
                    grid1[curr] = True
                    curl = (cur[0] + dirs[((d-1)+4)%4][0], cur[1] + dirs[((d-1)+4)%4][1])
                    grid2[curl] = True
            cur = (cur[0] + dirs[d][0], cur[1] + dirs[d][1])

    print(grid1)
    print()
    print(grid2)

    grid = [['.' for i in range(20)] for j in range(20)]

    # count1 = 0
    # for k in grid1:
    #     count1 += 1
    #     grid[k[1]+2][k[0]+2] = '#'
    # for r in grid:
    #     for c in r:
    #         print(c, end="")
    #     print()
    # grid = [['.' for i in range(20)] for j in range(20)]
    # count2 = 0
    # for k in grid2:
    #     count2 += 1
    #     grid[k[1]+2][k[0]+2] = '#'
    # for r in grid:
    #     for c in r:
    #         print(c, end="")
    #     print()

    minx = min(x for (x,y) in tg)
    miny = min(y for (x,y) in tg)

    maxx = max(x for (x,y) in tg)
    maxy = max(y for (x,y) in tg)

    # grid = [['.' for i in range(20)] for j in range(20)]
    count = 0
    for i in range(miny, maxy+1):
        acc = 0
        for j in range(minx, maxx+1):
            # if va > 0 or ra > 0 or la > 0:
            #     print(j, i)
            #     grid[i+2][j+2] = '#'
            #     count += 1
            if (j, i) in tg:
                # grid[i+2][j+2] = tg[(j, i)]
                if tg[(j, i)] == "V":
                    acc += 1

                if tg[(j, i)] == "R" and dg[(j, i)] == 1:
                    acc -= 0.5
                if tg[(j, i)] == "R" and dg[(j, i)] == 0:
                    acc += 0.5
                if tg[(j, i)] == "R" and dg[(j, i)] == 2:
                    acc += 0.5
                if tg[(j, i)] == "R" and dg[(j, i)] == 3:
                    acc -= 0.5
                if tg[(j, i)] == "L" and dg[(j, i)] == 1:
                    acc += 0.5
                if tg[(j, i)] == "L" and dg[(j, i)] == 0:
                    acc -= 0.5
                if tg[(j, i)] == "L" and dg[(j, i)] == 2:
                    acc -= 0.5
                if tg[(j, i)] == "L" and dg[(j, i)] == 3:
                    acc += 0.5
            print(acc, end=", ")
            if not acc%2 == 0:
                # print(j, i)
                # grid[i+2][j+2] = '#'
                count += 1
            elif (j, i) in tg:
                # grid[i+2][j+2] = '#'
                count += 1

        print()

    for r in grid:
        for c in r:
            print(c, end="")
        print()
    print(count)






    # print((count1, count2))
    # print(min(count1, count2))










    # print(max(scores))
