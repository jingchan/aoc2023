import re

digit = re.compile(r"\d")
word = re.compile(r"one|two|three|four|five|six|seven|eight|nine")
rword = re.compile("one|two|three|four|five|six|seven|eight|nine"[::-1])


def word_to_digit(word):
    if word == "one":
        return 1
    elif word == "two":
        return 2
    elif word == "three":
        return 3
    elif word == "four":
        return 4
    elif word == "five":
        return 5
    elif word == "six":
        return 6
    elif word == "seven":
        return 7
    elif word == "eight":
        return 8
    elif word == "nine":
        return 9
    else:
        return 0


BIG = 999999
with open("day1/a2.txt", "r") as f:
    sum = 0
    for line in f:
        # position of first digit
        first_digit = (
            int(digit.findall(line)[0]) if len(digit.findall(line)) > 0 else -1
        )
        first_digit_pos = (
            line.find(digit.findall(line)[0]) if len(digit.findall(line)) > 0 else BIG
        )
        first_word = (
            word_to_digit(word.findall(line)[0])
            if len(word.findall(line)) > 0
            else "str"
        )
        first_word_pos = (
            line.find(word.findall(line)[0]) if len(word.findall(line)) > 0 else BIG
        )
        first = first_digit if first_digit_pos < first_word_pos else first_word

        line = line[::-1]
        last_digit = int(digit.findall(line)[0]) if len(digit.findall(line)) > 0 else -1
        last_digit_pos = (
            line.find(digit.findall(line)[0]) if len(digit.findall(line)) > 0 else BIG
        )
        last_word = (
            word_to_digit(rword.findall(line)[0][::-1])
            if len(rword.findall(line)) > 0
            else "str"
        )
        last_word_pos = (
            line.find(rword.findall(line)[0]) if len(rword.findall(line)) > 0 else BIG
        )
        last = last_digit if last_digit_pos < last_word_pos else last_word

        sum += first * 10 + last

    print(sum)
