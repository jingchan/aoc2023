import math
import os

PATH = os.path.dirname(__file__)
# IN_FILE = PATH + "/1.txt"
IN_FILE = PATH + "/2.txt"
print(IN_FILE)

# #.##..##.
# ..#.##.#.
# ##......#
# ##......#
# ..#.##.#.
# ..##..##.
# #.#.##.#.

# #...##..#
# #....#..#
# ..##..###
# #####.##.
# #####.##.
# ..##..###
# #....#..#
def solve(lines):
    score = 0
    # print array one per line
    for i in range(len(lines)):
        print(lines[i])
    print()
    for i in range(len(lines)-1):
        ans = True
        diff = 0
        for j in range(1, len(lines)-i):
            if(i-j+1) < 0:
                print(i, j)
                break

            if lines[i-j+1] != lines[i+j]:
                for k in range(len(lines[0])):
                    if lines[i-j+1][k] != lines[i+j][k]:
                        diff +=1
            if diff > 1:
                break
        if diff == 1:
            score = (i+1)*100
            print('score:', score, i)
            return score

    transpose = []
    for i in range(len(lines)):
        for j in range(len(lines[0])):
            if len(transpose) <= j:
                transpose.append("")
            transpose[j] += lines[i][j]

    lines = transpose
    print('transpose')
    for i in range(len(lines)):
        print(lines[i])
    print()

    for i in range(len(lines)-1):
        ans = True
        diff = 0
        for j in range(1, len(lines)-i):
            if(i-j+1) < 0:
                print(i, j)
                break

            if lines[i-j+1] != lines[i+j]:
                for k in range(len(lines[0])):
                    if lines[i-j+1][k] != lines[i+j][k]:
                        diff +=1
            if diff > 1:
                break
        if diff == 1:
            score = (i+1)
            print('score:', score, i)
            return score
    raise Exception("no answer")

with open(IN_FILE, "r") as f:
    # line = f.readline()

    total = 0
    lines = []
    for line in f.readlines():
        line = line.strip()
        if not line == "":
            lines.append(line)
        else:
            total += solve(lines)
            lines = []

    total += solve(lines)

    print(total)


# ???.### 1,1,3
# .??..??...?##. 1,1,3
# ?#?#?#?#?#?#?#? 1,3,1,6
# ????.#...#... 4,1,1
# ????.######..#####. 1,6,5
# ?###???????? 3,2,1
# 101116732


# 4964259839627
