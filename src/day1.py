# Advent of Code 2018, Day 1
# (c) blu3r4y

import numpy as np
import itertools


def part1(arr):
    return arr.sum()


def part2(arr):
    frequency, seen = 0, {0}
    for e in itertools.cycle(arr):
        frequency += e
        if frequency in seen:
            return frequency
        seen.add(frequency)


if __name__ == "__main__":
    print(part1(np.loadtxt(r"../assets/day1.txt", dtype=int)))
    print(part2(np.loadtxt(r"../assets/day1.txt", dtype=int)))
