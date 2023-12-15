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

        num_copies = sum([1 for n in copy if n > 0])
        copy = [max(0, n - 1) for n in copy if n > 0]
        if match > 0:
            score = pow(2, match - 1)
            for c in range(0, num_copies + 1):
                copy.append(match)

        total += num_copies + 1
    print("total", total)
