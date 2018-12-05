# Advent of Code 2018, Day 5
# (c) blu3r4y

import re


def part1(polymer):
    result = []
    for element in polymer:
        # remove the last element if the new one would react with it
        if len(result) > 0 and reactive(element, result[-1]):
            result.pop()
        else:
            result.append(element)

    return len(result)


def part2(polymer):
    units = set(polymer.lower())

    # remove all units of one type and look for the shortest polymer
    lengths = [part1(re.sub(u, '', polymer, flags=re.IGNORECASE)) for u in units]
    return min(lengths)


def reactive(a, b):
    # upper and lower case letters are exactly 32 values apart ('A' - 'a' = 32)
    return abs(ord(a) - ord(b)) == 32


if __name__ == "__main__":
    print(part1("dabAcCaCBAcCcaDA"))
    print(part1(open(r"../assets/day5.txt").read()))

    print(part2("dabAcCaCBAcCcaDA"))
    print(part2(open(r"../assets/day5.txt").read()))
