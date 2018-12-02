# Advent of Code 2018, Day 2
# (c) blu3r4y

import numpy as np
import itertools


def part1(boxes):
    doubles, triples = 0, 0
    for box in boxes:
        # count occurrences of each char
        _, counts = np.unique(list(box), return_counts=True)

        # look for at least one double or triple
        if any(counts == 2):
            doubles += 1
        if any(counts == 3):
            triples += 1

    return doubles * triples


def part2(boxes):
    # list of numpy arrays, holding integers
    boxes = [np.array(list(map(ord, box))) for box in boxes]

    # iterate over the cartesian product
    for a, b in itertools.product(boxes, boxes):
        diff = np.count_nonzero(a - b)
        if diff == 1:
            # select values, where the difference is zero, and map it back
            return ''.join(map(chr, a[(a - b) == 0].ravel()))


if __name__ == "__main__":
    print(part1(["abcdef", "bababc", "abbcde", "abcccd", "aabcdd", "abcdee", "ababab"]))
    print(part2(["abcde", "fghij", "klmno", "pqrst", "fguij", "axcye", "wvxyz"]))

    print(part1(open(r"../assets/day2.txt").readlines()))
    print(part2(open(r"../assets/day2.txt").readlines()))
