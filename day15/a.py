import math
import os

PATH = os.path.dirname(__file__)
IN_FILE = PATH + "/1.txt"
# IN_FILE = PATH + "/2.txt"
print(IN_FILE)


with open(IN_FILE, "r") as f:
    total = 0
    # line = f.readline()
    grid = []
    for line in f.readlines():
        line = line.strip()
        codes = line.split(",")
        for code in codes:
            codeval = 0
            for c in code:
                codeval += ord(c)
                codeval *= 17
                codeval %= 256
            total += codeval

    print(total)
# rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7
