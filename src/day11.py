# Advent of Code 2018, Day 11
# (c) blu3r4y

import numpy as np
from scipy.ndimage import convolve


def part1(serial):
    grid = build_grid(serial)

    # 2d convolution over the image with a 3x3 summing kernel, stride = 1 and zero-padding (by offset 1)
    totals = convolve(grid, np.ones((3, 3)), mode='constant', cval=0, origin=[1, 1])
    index = np.unravel_index(np.argmax(totals), totals.shape)

    # add (1, 1) because coordinates must start at 1
    return ','.join(map(str, index + np.array((1, 1))))


def part2(serial, max_kernel=30):
    grid = build_grid(serial)

    largest_total = -1e10
    index, size = (0, 0), 0

    for kernel in range(1, max_kernel + 1):
        # 2d convolution over the image with a summing kernel, stride = 1 and zero-padding (by offset (k - 1) / 2)
        totals = convolve(grid, np.ones((kernel, kernel)), mode='constant', cval=0, origin=[(kernel - 1) // 2] * 2)

        # remember maximum value
        if np.max(totals) > largest_total:
            largest_total = np.max(totals)
            index = np.unravel_index(np.argmax(totals), totals.shape)
            size = kernel

    # add (1, 1) because coordinates must start at 1
    return ','.join(map(str, tuple(index + np.array((1, 1))) + (size,)))


def build_grid(serial):
    grid = np.zeros((300, 300), dtype=int)
    for cell, _ in np.ndenumerate(grid):
        # calculate the power level per cell (add +1 to indexes because coordinates must begin at 1)
        rack = cell[0] + 1 + 10
        power = (((rack * (cell[1] + 1) + serial) * rack) // 100) % 10 - 5
        grid[cell] = power

    return grid


if __name__ == "__main__":
    print(part1(18))
    print(part1(42))
    print(part1(7989))

    print(part2(18))
    print(part2(42))
    print(part2(7989))
