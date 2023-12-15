import math
import os

PATH = os.path.dirname(__file__)
# IN_FILE = PATH + "/1.txt"
IN_FILE = PATH + "/2.txt"
# IN_FILE = PATH + "/3.txt"
print(IN_FILE)


with open(IN_FILE, "r") as f:
    total = 0
    m = f.readline()
    line = f.readline()
    d = dict()
    cur = []
    for line in f.readlines():
        line = line.split()
        pos = line[0]
        l = line[2][1:4]
        r = line[3][0:3]
        d[pos] = (l, r)
        if pos[2] == "A":
            cur.append(pos)
    steps = 0
    print(cur)
    num_z = len([x for x in d if x[2] == "Z"])
    first_z = [dict() for x in cur]
    second_z = [dict() for x in cur]
    all_z = [dict() for x in cur]
    print(first_z)
    print(first_z[0].keys())
    print([x for x in first_z if len(x.keys()) == 0])
    # while (len([x for x in first_z if len(x.keys()) == 0]) > 0) or (
    #     len([x for x in second_z if len(x.keys()) == 0]) > 0
    # ):
    for it in range(100000):
        new_cur = []
        for c in cur:
            if m[steps % (len(m) - 1)] == "L":
                new_c = d[c][0]
            else:
                new_c = d[c][1]
            new_cur.append(new_c)
        cur = new_cur
        steps += 1
        # print(cur)
        for i in range(len(cur)):
            if cur[i][2] == "Z":
                if all_z[i].get(cur[i]) is None:
                    all_z[i][cur[i]] = [steps]
                else:
                    all_z[i][cur[i]].append(steps)
                    # is_uniq = True
                    # for x in all_z[i][cur[i]]:
                    #     if steps % x == 0:
                    #         is_uniq = False
                    # if is_uniq:
                    #     all_z[i][cur[i]].append(steps)
                    # all_z[i][cur[i]].append(steps - max(all_z[i][cur[i]]))

                if first_z[i].get(cur[i]) is None:
                    first_z[i][cur[i]] = steps
                elif second_z[i].get(cur[i]) is None:
                    second_z[i][cur[i]] = steps
                    # second_z[i][cur[i]] = steps - first_z[i][cur[i]]

                print(all_z)
    print()
    print(all_z)

    # print(first_z) print(second_z)
    p = 1
    for x in first_z:
        x = list(x.values())[0]
        if p % x != 0:
            p *= x
    max_i = math.sqrt(max([x for x in first_z[0].values()]))
    factors = [[] for x in cur]
    for i in range(2, int(max_i)):
        for j in range(len(first_z)):
            if list(first_z[j].values())[0] % i == 0:
                factors[j].append(i)
                factors[j].append(list(first_z[j].values())[0] / i)
                continue
        if p % i == 0:
            p /= i

    print(p)
    prod = 1
    maxim = 0
    print([x for x in factors])
    for v in [x[0] for x in factors]:
        prod *= v
        maxim = max(maxim, v)
    print(prod * 277)

    print("product", prod)


# # a mod b
# x = a % b
