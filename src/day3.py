# Advent of Code 2018, Day 3
# (c) blu3r4y

import re
import collections

import numpy as np

Claim = collections.namedtuple('Claim', ['id', 'x', 'y', 'w', 'h'])


def part1(claims):
    # overlapping claims have cell numbers greater than 1
    return np.sum(fill_claims(claims) > 1)


def part2(claims):
    arr = fill_claims(claims)
    for c in claims:
        # the claim whose cells are all equal to 1 has not been overlapped
        if np.all(arr[c.x:c.x + c.w, c.y:c.y + c.h] == 1):
            return c.id


def fill_claims(claims):
    # create an empty matrix big enough to hold all claims
    shape = np.amax(np.array([(c.x + c.w, c.y + c.h) for c in claims]), axis=0)
    arr = np.zeros(shape, dtype=int)

    for c in claims:
        # for every claim, increase the value within those cells
        arr[c.x:c.x + c.w, c.y:c.y + c.h] += 1

    return arr


def parse(lines):
    pattern = r'#(?P<id>\d+) @ (?P<x>\d+),(?P<y>\d+): (?P<w>\d+)x(?P<h>\d+)'
    return [Claim(id=int(e["id"]), x=int(e["x"]), y=int(e["y"]), w=int(e["w"]), h=int(e["h"]))
            for e in re.finditer(pattern, ''.join(lines))]


if __name__ == "__main__":
    print(part1(parse(["#1 @ 1,3: 4x4", "#2 @ 3,1: 4x4", "#3 @ 5,5: 2x2"])))
    print(part2(parse(["#1 @ 1,3: 4x4", "#2 @ 3,1: 4x4", "#3 @ 5,5: 2x2"])))

    print(part1(parse(open(r"../assets/day3.txt").readlines())))
    print(part2(parse(open(r"../assets/day3.txt").readlines())))
