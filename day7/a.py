import math
import os

PATH = os.path.dirname(__file__)
# IN_FILE = PATH + "/1.txt"
IN_FILE = PATH + "/2.txt"
print(IN_FILE)


def kind5(hand):
    return hand[0] == hand[1] == hand[2] == hand[3] == hand[4]


def kind4(hand):
    counts = dict()
    for card in hand:
        counts[card] = counts.get(card, 0) + 1
    return 4 in counts.values()


def kindfull(hand):
    counts = dict()
    for card in hand:
        counts[card] = counts.get(card, 0) + 1
    return 3 in counts.values() and 2 in counts.values()


def kind3(hand):
    counts = dict()
    for card in hand:
        counts[card] = counts.get(card, 0) + 1
    return 3 in counts.values()


def kind2p(hand):
    counts = dict()
    for card in hand:
        counts[card] = counts.get(card, 0) + 1
    num_2 = 0
    for c in counts.values():
        if c == 2:
            num_2 += 1
    return num_2 == 2


def kindpair(hand):
    counts = dict()
    for card in hand:
        counts[card] = counts.get(card, 0) + 1
    num_2 = 0
    return 3 in counts.values()


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


with open(IN_FILE, "r") as f:
    total = 0
    h = []
    for line in f.readlines():
        line = line.split()
        line[0]
        # Replace K with A
        line[0] = line[0].replace("2", "e")
        line[0] = line[0].replace("3", "f")
        line[0] = line[0].replace("4", "g")
        line[0] = line[0].replace("5", "h")
        line[0] = line[0].replace("6", "i")
        line[0] = line[0].replace("7", "j")
        line[0] = line[0].replace("8", "k")
        line[0] = line[0].replace("9", "l")
        line[0] = line[0].replace("T", "m")
        line[0] = line[0].replace("J", "n")
        line[0] = line[0].replace("Q", "o")
        line[0] = line[0].replace("K", "p")
        line[0] = line[0].replace("A", "q")

        h.append((line[0], int(line[1]), False))

    rank = len(h)

    q = []
    for i, (hand, bid, finish) in enumerate(h):
        if finish:
            continue
        if hand[0] == hand[1] == hand[2] == hand[3] == hand[4]:
            q.append(i)
            h[i] = (hand, bid, True)
            continue
    q = [h[z] for z in q]
    q.sort(key=lambda i: i[0], reverse=True)
    for wh in q:
        total += wh[1] * rank
        rank -= 1
    print(len(q), total)

    q = []
    for i, (hand, bid, finish) in enumerate(h):
        if finish:
            continue
        counts = dict()
        for card in hand:
            counts[card] = counts.get(card, 0) + 1
        if 4 in counts.values():
            q.append(i)
            h[i] = (hand, bid, True)
            continue
    q = [h[z] for z in q]
    q.sort(key=lambda i: i[0], reverse=True)
    for wh in q:
        total += wh[1] * rank
        rank -= 1
    print(len(q), total)

    q = []
    for i, (hand, bid, finish) in enumerate(h):
        if finish:
            continue
        counts = dict()
        for card in hand:
            counts[card] = counts.get(card, 0) + 1
        if 3 in counts.values() and 2 in counts.values():
            q.append(i)
            h[i] = (hand, bid, True)
            continue
    print("q", q)
    q = [h[z] for z in q]
    q.sort(key=lambda i: i[0], reverse=True)
    for wh in q:
        total += wh[1] * rank
        rank -= 1
    print(len(q), total)

    q = []
    for i, (hand, bid, finish) in enumerate(h):
        if finish:
            continue
        counts = dict()
        for card in hand:
            counts[card] = counts.get(card, 0) + 1
        if 3 in counts.values():
            print(i)
            q.append(i)
            h[i] = (hand, bid, True)

    q = [h[z] for z in q]
    print(q)
    q.sort(key=lambda i: i[0], reverse=True)
    for wh in q:
        total += wh[1] * rank
        rank -= 1
    print(len(q), total)

    q = []
    for i, (hand, bid, finish) in enumerate(h):
        if finish:
            continue
        counts = dict()
        for card in hand:
            counts[card] = counts.get(card, 0) + 1
        num_2 = 0
        for c in counts.values():
            if c == 2:
                num_2 += 1
        if num_2 == 2:
            q.append(i)
            h[i] = (hand, bid, True)
            continue

    q = [h[z] for z in q]
    q.sort(key=lambda i: i[0], reverse=True)
    for wh in q:
        total += wh[1] * rank
        rank -= 1
    print(len(q), total)

    q = []
    for i, (hand, bid, finish) in enumerate(h):
        if finish:
            continue
        counts = dict()
        for card in hand:
            counts[card] = counts.get(card, 0) + 1
        num_2 = 0
        if 2 in counts.values():
            num_2 += 1
        if num_2 == 1:
            q.append(i)
            h[i] = (hand, bid, True)
            continue
    q = [h[z] for z in q]
    q.sort(key=lambda i: i[0], reverse=True)
    for wh in q:
        total += wh[1] * rank
        rank -= 1
    print(len(q), total)

    q = []
    for i, (hand, bid, finish) in enumerate(h):
        if finish:
            continue
        q.append(i)
        h[i] = (hand, bid, True)
    q = [h[z] for z in q]
    q.sort(key=lambda i: i[0], reverse=True)
    for wh in q:
        total += wh[1] * rank
        rank -= 1
    print(len(q), total)

    print(total)
