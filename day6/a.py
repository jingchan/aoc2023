from functools import reduce

import os

PATH = os.path.dirname(__file__)
# IN_FILE = PATH + "/1.txt"
IN_FILE = PATH + "/2.txt"
print(IN_FILE)


with open(IN_FILE, "r") as f:
    total = 1
    times = []
    distances = []
    line = f.readline()
    times = [int(a) for a in line.split()[1:]]
    line = f.readline()
    distances = [int(a) for a in line.split()[1:]]

    for i in range(len(times)):
        count = 0
        for j in range(times[i]):
            print(j, times[i] - j)
            # print(j * (i - j))
            if j * (times[i] - j) > distances[i]:
                count += 1

        total *= count

    print(total)
# Time:      7  15   30
# Distance:  9  40  200
