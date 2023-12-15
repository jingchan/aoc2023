import os

PATH = os.path.dirname(__file__)
# IN_FILE = PATH + "/1.txt"
IN_FILE = PATH + "/2.txt"
print(IN_FILE)


with open(IN_FILE, "r") as f:
    total = 0
    copy = []
    for line in f.readlines():
        score = 0
        win = []
        nums = []
        for word in line.split("|")[0].strip().split(":")[1].strip().split():
            win.append(int(word))
        for word in line.split("|")[1].strip().split():
            nums.append(int(word))

        # sort each
        win.sort()
        nums.sort()

        # find each value of win in nums
        match = 0
        for w in win:
            if w in nums:
                match += 1
        print("match", match)
        if match > 0:
            total += pow(2, match - 1)

    print("total", total)
