# Advent of Code 2018, Day 9
# (c) blu3r4y

from itertools import cycle

from blist import blist


def part1(players, marbles):
    scores = [0] * players
    circle, current = blist([0]), 0

    # iterate over players taking turns and all the marbles simultaneously
    for player, marble in zip(cycle(range(players)), range(1, marbles + 1)):

        if marble % 23 == 0:
            # the new marble is the one 7 marbles to the left (counter-clockwise)
            current = (current - 7) % len(circle)
            scores[player] += marble + circle.pop(current)
        else:
            # insert new marble 2 marbles to the right (clockwise)
            current = (current + 2) % len(circle)
            circle.insert(current, marble)

    return max(scores)


def part2(players, marbles):
    return part1(players, marbles * 100)


if __name__ == "__main__":
    print(part1(9, 25))
    print(part1(10, 1618))
    print(part1(13, 7999))
    print(part1(17, 1104))
    print(part1(21, 6111))
    print(part1(30, 5807))
    print(part1(411, 71170))

    print(part2(411, 71170))
