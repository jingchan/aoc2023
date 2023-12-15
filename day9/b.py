import math
import os

PATH = os.path.dirname(__file__)
# IN_FILE = PATH + "/1.txt"
IN_FILE = PATH + "/2.txt"
print(IN_FILE)


def diff(x):
    print(x)
    if all(i == 0 for i in x):
        return 0
    delta = x[0]-x[1]

    y= [0]* (len(x)-1)
    for i in range(len(x)-1):
        y[i]=x[i+1]-x[i]

    next_d = diff(y)
    print(x[0], x[0]-next_d)
    return x[0]-next_d

with open(IN_FILE, "r") as f:
    total =0
    # line = f.readline()
    for line in f.readlines():
        line = line.split()
        x = [int(i) for i in line]

        print(diff(x))
        total += diff(x)





    print(total)
