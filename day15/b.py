import math
import os

PATH = os.path.dirname(__file__)
# IN_FILE = PATH + "/1.txt"
IN_FILE = PATH + "/2.txt"
print(IN_FILE)


with open(IN_FILE, "r") as f:
    total = 0
    # line = f.readline()
    grid = []
    box = {}
    for i in range(256):
        box[i] = ({}, [])
    for line in f.readlines():
        line = line.strip()
        codes = line.split(",")
        for code in codes:

            if '=' in code:
                cstr = code.split("=")[0]
                l = code.split("=")[1]

                codeval = 0
                for c in cstr:
                    codeval += ord(c)
                    codeval *= 17
                    codeval %= 256

                if cstr in box[codeval][0]:
                    box[codeval][0][cstr] = l
                else:
                    box[codeval][0][cstr] = l
                    box[codeval][1].append(cstr)
            elif '-' in code:
                cstr = code.split("-")[0]
                codeval = 0
                for c in cstr:
                    codeval += ord(c)
                    codeval *= 17
                    codeval %= 256
                    # // remove from dict
                if cstr in box[codeval][0]:
                    box[codeval][0].pop(cstr)
                    box[codeval][1].remove(cstr)
            else:
                print('err')

            # total += codeval
    for i in range(256):
        bi = i+1
        for slot, l in enumerate(box[i][1]):
            lens = box[i][0][l]
            total += bi * (slot+1) * int(lens)




                # print(ord(c))
        # grid.append(line)

    print(total)
# rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7
