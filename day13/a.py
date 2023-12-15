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
    print(lines)
    for i in range(len(lines)-1):
        ans = True
        for j in range(1, len(lines)-i):
            print('chek', i, j, i-j)
            if(i-j+1) < 0:
                print(i, j)
                break

            print('ind', i-j+1, i+j)
            if lines[i-j+1] != lines[i+j]:

                print('---')
                print(lines[i-j+1])
                print(lines[i+j])
                ans = False
                break
            else:
                print('===')
                print(lines[i-j+1])
                print(lines[i+j])
        if ans:
            score += (i+1)*100
            print('score:', score)
            break

    transpose = []
    for i in range(len(lines)):
        for j in range(len(lines[0])):
            if len(transpose) <= j:
                transpose.append("")
            transpose[j] += lines[i][j]
    print('trans', transpose)

    lines = transpose
    for i in range(len(lines)-1):
        ans = True
        for j in range(1, len(lines)-i):
            print('chek', i, j, i-j)
            if(i-j+1) < 0:
                print(i, j)
                break

            print('ind', i-j+1, i+j)
            if lines[i-j+1] != lines[i+j]:
                print('---')
                print(lines[i-j+1])
                print(lines[i+j])
                ans = False
                break
        if ans:
            score += i+1
            print('score:', score)
            break
    return score


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
