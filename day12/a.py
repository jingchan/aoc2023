import math
import os

PATH = os.path.dirname(__file__)
# IN_FILE = PATH + "/1.txt"
IN_FILE = PATH + "/2.txt"
print(IN_FILE)


def solve(arr, lb, start=0, ans=None, cache=None, skip=False):
    if start == 0:
        if ans is None:
            ans = []
        if cache is None:
            cache = {}
        print(arr)
    if (start, len(lb), skip) in cache:
        # print(cache)

        print('cachehit', (start, len(lb),skip))
        return cache[(start, len(lb),skip)]

    if len(lb) == 0:
        # print(ans)
        for x in arr[start:]:
            if x == "#":
                print('cachehit', (start, len(lb),skip))
                cache[(start, len(lb), skip)] = 0
                return 0
        # for i in range(len(arr)):
        #     inanswer=False
        #     for a in ans:
        #         if i >= a[0] and i < a[0]+a[1]:
        #             inanswer=True
        #             print("#", end="")
        #     if not inanswer:
        #         if arr[i] == "#":
        #             cache[(start, len(lb),skip)] = 0
        #             return 0
        #         print(".", end="")
        print('cacheset', (start, len(lb),skip))
        cache[(start, len(lb),skip)] = 1
        return 1

    if start >= len(arr):
        return 0
    acc = 0
    if arr[start] == "." or arr[start] == "?":
        acc += solve(arr, lb, start+1, ans, cache)

    if arr[start] == "#" or arr[start] == "?":
        # if start==0 or arr[start-1] == "." or arr[start-1] == "?":
        if not skip:
            cont = True
            for i in range(lb[0]):
                if start+i >= len(arr) or arr[start+i] == ".":
                    cont = False
                    break
            if cont:
                # if start+lb[0] >= len(arr) or arr[start+lb[0]] == "." or arr[start+lb[0]] == "?":
                acc += solve(arr, lb[1:], start+lb[0], ans+[(start, lb[0])], cache, True)
    print('cacheset', (start, len(lb),skip))
    cache[(start, len(lb),skip)] = acc
    return acc



with open(IN_FILE, "r") as f:
    total = 0
    # line = f.readline()
    for line in f.readlines():
        line = line.strip()
        arr, vals = line.split(" ")

        lb = [int(x) for x in vals.split(",")]

        narr = arr + "?" + arr + "?"+ arr + "?"+ arr + "?" + arr
        nlb = lb*5
        print (narr)
        print (nlb)

        score = solve(narr, nlb)
        total+= score
        print(score)
        print('------------------------')

    print(total)


# ???.### 1,1,3
# .??..??...?##. 1,1,3
# ?#?#?#?#?#?#?#? 1,3,1,6
# ????.#...#... 4,1,1
# ????.######..#####. 1,6,5
# ?###???????? 3,2,1
# 101116732


# 4964259839627
