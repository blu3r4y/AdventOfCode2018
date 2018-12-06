# Advent of Code 2018, Day 6
# (c) blu3r4y

import numpy as np


def part1(coordinates):
    # create a matrix filled with -1 big enough to hold all coordinates
    shape = np.amax(coordinates, axis=0) + (1, 1)
    matrix = np.full(shape, -1)

    for cell, _ in np.ndenumerate(matrix):
        # calculate manhattan distance to every coordinate
        dists = np.sum(np.abs(cell - coordinates), axis=1)
        # assign the minimum distance to the cell, if it is unique
        mins = np.argwhere(dists == np.amin(dists))
        if len(mins) == 1:
            matrix[cell] = mins[0][0]

    # invalidate infinite regions
    infinite = np.unique(np.hstack((matrix[(0, -1), :], matrix[:, (0, -1)].T)))
    matrix[np.isin(matrix, infinite)] = -1

    # measure region size
    _, counts = np.unique(matrix.ravel(), return_counts=True)
    return np.max(counts[1:])


def part2(coordinates, min_dist):
    # create an empty matrix big enough to hold all coordinates
    shape = np.amax(coordinates, axis=0) + (1, 1)
    matrix = np.zeros(shape, dtype=int)

    for cell, _ in np.ndenumerate(matrix):
        # sum manhattan distance to every coordinate
        dist = np.sum(np.abs(cell - coordinates))
        # assign a marker if the distance is small enough
        if dist < min_dist:
            matrix[cell] = 1

    return np.sum(matrix)


if __name__ == "__main__":
    print(part1(np.array([(1, 1), (1, 6), (8, 3), (3, 4), (5, 5), (8, 9)])))
    print(part1(np.loadtxt(r"../assets/day6.txt", delimiter=',', dtype=int)))

    print(part2(np.array([(1, 1), (1, 6), (8, 3), (3, 4), (5, 5), (8, 9)]), 32))
    print(part2(np.loadtxt(r"../assets/day6.txt", delimiter=',', dtype=int), 10000))
