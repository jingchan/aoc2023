from functools import reduce

import os

PATH = os.path.dirname(__file__)
# IN_FILE = PATH + "/1.txt"
IN_FILE = PATH + "/2.txt"
print(IN_FILE)


def remap2(s, sr, r, rr, delta):
    a1 = s
    a2 = s + sr
    b1 = r
    b2 = r + rr
    # disjoint
    if a1 < b1 and a2 <= b1:
        return [(s, sr)], []
    if b1 < a1 and b2 <= a1:
        return [(s, sr)], []

    # contained
    if a1 < b1 and a2 > b2:
        return [(a1, b1 - a1), (b2, a2 - b2)], [(b1 + delta, b2 - b1)]
    if b1 <= a1 and b2 >= a2:
        return [], [(a1 + delta, a2 - a1)]

    # overlap first part
    if b1 <= a1 and b2 > a1:
        return [(b2, a2 - b2)], [(a1 + delta, b2 - a1)]
    # overlap second part
    if a1 < b1 and a2 > b1:
        return [(a1, b1 - a1)], [(b1 + delta, a2 - b1)]

    raise Exception

    # -------- -------------


def remap(s, sr, r, rr, delta):
    if s < r and s + sr - 1 < r:
        return [(s, sr)], []
    if r < s and r + rr - 1 < s:
        return [(s, sr)], []
    if s < r and s + sr - 1 > r:
        if s + sr - 1 > r + rr - 1:
            return [(s, r - s), (r + rr, s + sr - r - rr)], [(r + delta, rr)]
        else:
            return [(s, r - s)], [(r + delta, s + sr - r)]
    if r < s and r + rr - 1 > s:
        if r + rr - 1 > s + sr - 1:
            return [], [(s + delta, sr)]
        else:
            return [(r + rr, s + sr - r - rr)], [(s + delta, r + rr - s)]
    if s == r and s + sr > r + rr:
        return [(r, sr - rr)], [(s + delta, rr)]
    else:
        return [], [(s + delta, sr)]


with open(IN_FILE, "r") as f:
    total = 0
    seeds_tups = [int(s) for s in f.readline().split()[1:]]

    print(seeds_tups)
    seeds = []
    converted = []
    for i in range(0, len(seeds_tups), 2):
        seeds.append((seeds_tups[i], seeds_tups[i + 1]))
    print(seeds)

    for line in f.readlines():
        if line[0].isalpha():
            print(seeds)
            continue
        if line == "\n":
            seeds.extend(converted)
            converted = []
            continue
        seedmap = [int(n) for n in line.split()]
        delta = seedmap[0] - seedmap[1]
        # seedmap[1] + seedmap[2]
        new_seeds = []
        for s in seeds:
            range = s[1]
            new_s, new_c = remap2(s[0], s[1], seedmap[1], seedmap[2], delta)
            # new_s, new_c = remap(s[0], s[1], seedmap[1], seedmap[2], delta)
            if s[1] != sum([s[1] for s in new_s]) + sum([s[1] for s in new_c]):
                raise Exception
            converted.extend(new_c)
            new_seeds.extend(new_s)
        seeds = new_seeds

    seeds.extend(converted)
    converted = []
    print(min([s[0] for s in seeds]))
