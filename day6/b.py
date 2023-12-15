import math
from functools import reduce

import os

PATH = os.path.dirname(__file__)
# IN_FILE = PATH + "/1.txt"
IN_FILE = PATH + "/2.txt"
print(IN_FILE)


with open(IN_FILE, "r") as f:
    times = []
    distances = []
    line = f.readline()
    times = ""
    for a in line.split()[1:]:
        times += a
    t = int(times)
    print("time", times)
    line = f.readline()
    d = ""
    for a in line.split()[1:]:
        d += a
    d = int(d)
    print(d)

    i1 = (t + math.sqrt(t**2 - 4 * d)) / 2
    i2 = (t - math.sqrt(t**2 - 4 * d)) / 2
    print(i1, i2)
    print(math.ceil(i1) - math.ceil(i2))


# i * (T - i) > D
# i^2 - Ti + D < 0
# i = (T + sqrt(T^2 - 4D)) / 2
# i = (T - sqrt(T^2 - 4D)) / 2
