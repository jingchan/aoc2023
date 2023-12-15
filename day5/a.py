from functools import reduce

import os

PATH = os.path.dirname(__file__)
# IN_FILE = PATH + "/1.txt"
IN_FILE = PATH + "/2.txt"
print(IN_FILE)


with open(IN_FILE, "r") as f:
    total = 0
    seeds = [int(s) for s in f.readline().split()[1:]]

    converted = []
    for line in f.readlines():
        if line[0].isalpha():
            print(seeds)
            continue
        if line == "\n":
            print(converted)
            for i in range(len(seeds)):
                sum = 0
                for c in converted:
                    sum += c[i]
                if sum == 0:
                    sum += seeds[i]
                seeds[i] = sum
            converted = []
            continue
        seedmap = [int(n) for n in line.split()]
        delta = seedmap[0] - seedmap[1]
        # seedmap[1] + seedmap[2]
        convert = []
        for s in seeds:
            if s >= seedmap[1] and s < seedmap[1] + seedmap[2]:
                convert.append(s + delta)
            else:
                convert.append(0)
        converted.append(convert)

        line = line.strip()

    for i in range(len(seeds)):
        sum = 0
        for c in converted:
            sum += c[i]
        if sum == 0:
            sum += seeds[i]
        seeds[i] = sum
    converted = []
    print(seeds)
    print(min(seeds))
# seeds: 79 14 55 13

# seed-to-soil map:
# 50 98 2
# 52 50 48

# soil-to-fertilizer map:
# 0 15 37
# 37 52 2
# 39 0 15

# fertilizer-to-water map:
# 49 53 8
# 0 11 42
# 42 0 7
# 57 7 4

# water-to-light map:
# 88 18 7
# 18 25 70

# light-to-temperature map:
# 45 77 23
# 81 45 19
# 68 64 13

# temperature-to-humidity map:
# 0 69 1
# 1 0 69

# humidity-to-location map:
# 60 56 37
# 56 93 4
