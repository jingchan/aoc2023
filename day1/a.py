

with open('day1/in2.txt', 'r') as f:
    sum = 0
    for line in f:
        digits = [int(d) for d in line if d.isdigit()]
        first = digits[0]
        last = digits[-1]
        sum += first*10 + last

    print(sum)
