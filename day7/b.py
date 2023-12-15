import math
import os

PATH = os.path.dirname(__file__)
# IN_FILE = PATH + "/1.txt"
IN_FILE = PATH + "/2.txt"
print(IN_FILE)


ct = ["J", "2", "3", "4", "5", "6", "7", "8", "9", "T", "Q", "K", "A"]


def kind5(hand):
    counts = dict()
    for card in hand:
        counts[card] = counts.get(card, 0) + 1

    jok = counts.get("d", 0)
    if jok >= 4:
        return True
    for c in counts.values():
        jok = counts.get("d", 0)
        if c == 5 - jok:
            return True


def kind4(hand):
    counts = dict()
    for card in hand:
        counts[card] = counts.get(card, 0) + 1

    jok = counts.get("d", 0)
    counts["d"] = 0
    for c in counts.values():
        if c == 4 - jok:
            return True


def kindfull(hand):
    counts = dict()
    for card in hand:
        counts[card] = counts.get(card, 0) + 1
    jok = counts.get("d", 0)
    counts["d"] = 0
    if 3 in counts.values() and 2 in counts.values():
        return True
    num2 = 0
    for c in counts.values():
        if c == 2:
            num2 += 1
    if num2 == 2 and jok >= 1:
        return True
    return False


def kind3(hand):
    counts = dict()
    for card in hand:
        counts[card] = counts.get(card, 0) + 1
    jok = counts.get("d", 0)
    counts["d"] = 0
    for c in counts.values():
        if c == 3 - jok:
            return True


def kind2p(hand):
    counts = dict()
    for card in hand:
        counts[card] = counts.get(card, 0) + 1
    jok = counts.get("d", 0)
    counts["d"] = 0
    num2 = 0
    for c in counts.values():
        if c == 2:
            num2 += 1
    if num2 == 2:
        return True
    if 2 in counts.values() and jok == 1:
        return True
    return False


def kindpair(hand):
    counts = dict()
    for card in hand:
        counts[card] = counts.get(card, 0) + 1
    jok = counts.get("d", 0)
    counts["d"] = 0
    for c in counts.values():
        if c == 2 - jok:
            return True


def handtype(hand):
    if kind5(hand):
        return 1
    if kind4(hand):
        return 2
    if kindfull(hand):
        return 3
    if kind3(hand):
        return 4
    if kind2p(hand):
        return 5
    if kindpair(hand):
        return 6
    return 7


def card_val(card):
    if card == "T":
        return 10


cmap = {
    "d": "J",
    "e": "2",
    "f": "3",
    "g": "4",
    "h": "5",
    "i": "6",
    "j": "7",
    "k": "8",
    "l": "9",
    "m": "T",
    "o": "Q",
    "p": "K",
    "q": "A",
}


def ph(hand):
    print([cmap.get(c) for c in hand])


with open(IN_FILE, "r") as f:
    total = 0
    h = []
    for line in f.readlines():
        line = line.split()
        line[0]
        # Replace K with A
        line[0] = line[0].replace("J", "d")
        line[0] = line[0].replace("2", "e")
        line[0] = line[0].replace("3", "f")
        line[0] = line[0].replace("4", "g")
        line[0] = line[0].replace("5", "h")
        line[0] = line[0].replace("6", "i")
        line[0] = line[0].replace("7", "j")
        line[0] = line[0].replace("8", "k")
        line[0] = line[0].replace("9", "l")
        line[0] = line[0].replace("T", "m")
        line[0] = line[0].replace("Q", "o")
        line[0] = line[0].replace("K", "p")
        line[0] = line[0].replace("A", "q")

        h.append((line[0], int(line[1]), False))

    rank = len(h)

    for ht in range(0, 8):
        q = []
        for i, (hand, bid, finish) in enumerate(h):
            if finish:
                continue
            if handtype(hand) == ht:
                q.append(i)
                h[i] = (hand, bid, True)
                continue
        q = [h[z] for z in q]
        q.sort(key=lambda i: i[0], reverse=True)
        for wh in q:
            ph(wh[0])
            total += wh[1] * rank
            rank -= 1
        print(len(q), total)

    print(total)
