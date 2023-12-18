import math
import os
import re

PATH = os.path.dirname(__file__)
IN_FILE = PATH + '/1.txt'
# IN_FILE = PATH + "/2.txt"

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
        l = int(hex[2:-2], 16)
        d = int(hex[-2])
        print(hex, d)
        input.append((d, l, hex))
        # input.append((di[d], int(l), hex))


    cur = (0, 0)
    grid1[cur] = True
    grid2[cur] = True
    tg = set()
    dg = {}
    xstop = set()
    ystop = set()
    pathsize = 0
    for i in range(len(input)):
        (d, l, hex) = input[(i)%len(input)]
        (ld, ll, lhex) = input[((i-1)+len(input))%len(input)]
        xstop.add(cur[0])
        ystop.add(cur[1])
        tg.add(cur)
        print('p',cur)
        cur = (cur[0] + dirs[d][0]*l, cur[1] + dirs[d][1]*l)
        pathsize += l

    xs = sorted(xstop)
    ys = sorted(ystop)
    print('sortedx', xs)
    print('sortedy', ys)

    minx = min(x for (x,y) in tg)
    miny = min(y for (x,y) in tg)

    maxx = max(x for (x,y) in tg)
    maxy = max(y for (x,y) in tg)

    cury = miny
    last_width = 0
    last_ranges = set()
    total =0
    for yi in range(len(ys)):
        cury = ys[yi]
        cxs = sorted([x for (x,y) in tg if y <= cury])

        i=0
        keep=[]
        while i < len(cxs):
            if i+1 < len(cxs) and cxs[i]==cxs[i+1]:
                i+=2
            else:
                keep.append(cxs[i])
                i+=1
        cxs = keep


        in_ranges = set()
        width=0
        # print('cxslen', len(cxs))
        for i, x in enumerate(cxs):
            if i%2 == 0:
                if cxs[i+1] - x > 0:
                    in_ranges.add((x, cxs[i+1]))
                    width += cxs[i+1] - x + 1
                    # print('addwidth', cxs[i+1] - x + 1)
        # print('width', width)
        if yi < len(ys)-1:
            total +=(ys[yi+1]-ys[yi])*width
        # else:
        #     total += width

        # edge stuff
        # print('last', last_width)
        # print('curwidth', width)
        # print(width-last_width)
        # if yi>0:
        #     total -= width-last_width

        print("last",last_ranges)
        print("inrange",in_ranges)
        remaining = last_ranges
        for lrs, lre in in_ranges:
            next = []
            for rs, re in remaining:
                if rs >= lrs and rs <= lre:
                    rs = lre+1
                if re <= lre and re >= lrs:
                    re = lrs-1
                if rs <= re:
                    next.append((rs, re))
            remaining = next
        ending_ranges = remaining
        print([(rs,re) for rs, re in ending_ranges])
        print([re-rs+1 for rs, re in ending_ranges])
        for i, ending_range1 in enumerate(ending_ranges):
            for j, ending_range2 in enumerate(ending_ranges):
                if i != j:
                    if ((ending_range1[0] >= ending_range2[0] and ending_range1[0] <= ending_range2[1])
                    or (ending_range1[1] <= ending_range2[1] and ending_range1[1] >= ending_range2[0])):
                        raise Exception("overlap")

        end_range_len = sum([re-rs+1 for rs, re in ending_ranges])
        print('ending', end_range_len)

        total += end_range_len




        last_width=width
        last_ranges = in_ranges



            # print(xi, yi, end=' ')
    print(total)


    #  952408144115
    #  952407629995


    # 1863245620090
# 952408144115
# 952408144115


#  0,0 ------------ 461k,0
#   |               461k,56k --------------------- 818k, 56k
#   |                   497k,356k --- 609k,356k        |
#  0,500k - 5k,500k          |            |            |
#              |             |            |        818k,919k ------- 1.1m,919k                                               818k,919k         1.1m,919k
#           5k,1.1m --- 497k,1.1m     609k,1.1m -------------------- 1.1m,1.1m
#
#
#

    # (461937+1)*56407
    # 26,056,536,766


# 44644467493502
