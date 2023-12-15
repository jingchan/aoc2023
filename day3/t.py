import re
import os

PATH = os.path.dirname(__file__)
IN_FILE = PATH + "/1.txt"
# IN_FILE = PATH + "/2.txt"
print(IN_FILE)
matcher = re.compile(r"^(\d)+(?=\D|$)")

with open(IN_FILE, "r") as f:
    score = 0
    grid = []
    for line in f:
        grid.append(line[:-1])

    for i in range(0, len(grid)):
        for j in range(0, len(grid[0])):
            if grid[i][j] != "." and not grid[i][j].isdigit():
                for off in range(-1, 2):
                    k = 0
                    while k < len(grid[0]):
                        if i + off < 0 or i + off >= len(grid):
                            k += 1
                            continue
                        m = matcher.match(grid[i + off][k:])
                        if m:
                            print("Num:", m.group(0))
                            ln = len(m.group(0))
                            print("k:", k)
                            print("ln:", ln)
                            print("j:", j)
                            print(k <= j + 1)
                            print(k + ln)
                            print(j - 1)
                            print(k + ln >= j - 1)
                            if k <= j + 1 and k + ln >= j - 1:
                                num = m.group(0)
                                print("match:", num)
                                score += int(num)
                                print(ln)
                                print(grid[i + off])
                                new_str = (
                                    grid[i + off][:k]
                                    + "*" * ln
                                    + grid[i + off][k + ln :]
                                )
                                print(new_str)
                                grid[i + off] = new_str
                                # grid[i + off] = (
                                #     grid[i + off][: (k - 1)]
                                #     + "*" * ln
                                #     + grid[i + off][: (k + ln)]
                                # )
                                # print(grid[i + off])
                            k += len(m.group(0))
                            break
                        else:
                            k += 1
    print(score)
