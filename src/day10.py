# Advent of Code 2018, Day 10
# (c) blu3r4y


from itertools import count

import matplotlib.pyplot as plt
import numpy as np
from parse import parse


def solve(positions, velocities):
    last_extend = 1e10
    for i in count(1):
        positions += velocities

        # check if the points already collapsed to their smallest form (in the previous iteration) by
        # checking if the surrounding bounding box is increasing now (i.e. width + height of the bounding box)
        extend = np.sum(np.amax(positions, axis=0) - np.amin(positions, axis=0))
        if extend > last_extend:
            # revert the last step and move the points to the origin by removing the smallest points
            positions -= velocities
            positions -= np.amin(positions, axis=0)

            # draw the points in a matrix and plot it
            image = np.zeros(np.amax(positions, axis=0) + 1)
            for pos in positions:
                image[tuple(pos)] = 1

            plt.imshow(image.T)
            plt.title("Iteration {}".format(i))
            plt.show()

            # seconds passed
            return i

        last_extend = extend


def _parse(lines):
    positions, velocities = [], []
    for line in lines:
        p = parse("position=<{},{}> velocity=<{},{}>", line)
        positions.append((p[0], p[1]))
        velocities.append((p[2], p[3]))

    return np.array(positions, dtype=int), np.array(velocities, dtype=int)


if __name__ == "__main__":
    print(solve(*_parse(open(r"../assets/day10_demo.txt").readlines())))
    print(solve(*_parse(open(r"../assets/day10.txt").readlines())))
