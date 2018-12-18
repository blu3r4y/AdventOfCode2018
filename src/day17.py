# Advent of Code 2018, Day 17
# (c) blu3r4y

import os

import numpy as np
from colorama import Fore, Back, Style
from parse import parse

SPRING_LOCATION = 500, 0
SPRING, SAND, DRY, WATER, CLAY = 0, 1, 2, 3, 4
SYMBOLS = {SAND: '.', CLAY: '#', SPRING: '+', WATER: '~', DRY: '|'}


def solve(grid, area, debug=False):
    springs = [SPRING_LOCATION]

    # step until nothing changes anymore
    pre = np.zeros_like(grid)
    while not np.array_equal(grid, pre):
        pre = np.copy(grid)
        springs = step(grid, springs)

    if debug:
        print_grid(grid)

    dry_cells = np.count_nonzero(grid[:, area[0]:area[1]] == DRY)
    water_cells = np.count_nonzero(grid[:, area[0]:area[1]] == WATER)

    # reached cells (~ and |), stable water cells (~)
    return dry_cells + water_cells, water_cells


def step(grid, springs):
    def _fill_from(x, y):
        # dry area underneath
        down = np.argmax(grid[x, y + 1:] > DRY)
        down = down if (down > 0 or grid[x, y + 1] > DRY) else grid.shape[1] - 1

        grid[x, y + 1:y + down] = DRY

        # water reaching infinity check
        if down + 1 < grid.shape[1]:

            # fill left and right if solid below
            left = np.argmax(np.concatenate((grid[:x, y + down][::-1] > DRY, [True])))
            right = np.argmax(np.concatenate((grid[x + 1:, y + down] > DRY, [True])))
            below = np.all(grid[x - left:x + right + 1, y + down + 1] >= DRY)

            if below:
                # fill solid bowl
                grid[x, y + down] = WATER
                if left > 0:
                    grid[x - left:x, y + down] = WATER
                if right > 0:
                    grid[x + 1:x + right + 1, y + down] = WATER
            else:
                # overflow the bowl
                left = min(left, np.argmin(grid[:x + 1, y + down + 1][::-1] > DRY))
                right = min(right, np.argmin(grid[x:, y + down + 1] > DRY))

                grid[x - left:x + right + 1, y + down] = DRY

                # add new springs to the left and right if the bowl overflows to sand
                if grid[x - left, y + down + 1] == SAND:
                    springs.append((x - left, y + down))
                if grid[x + right, y + down + 1] == SAND:
                    springs.append((x + right, y + down))

    # let the water flow from all springs
    for spring in springs:
        _fill_from(*spring)

    return springs


def _parse(lines):
    clays = []

    # parse coordinate representation
    for line in lines:
        xy = parse("{a}={a1:d}, {b}={b1:d}..{b2:d}", line.strip())
        a, b = slice(xy['a1'], xy['a1'] + 1), slice(xy['b1'], xy['b2'] + 1)
        if xy['a'] == 'x':
            clays.append((a, b))
        elif xy['a'] == 'y':
            clays.append((b, a))

    # create big enough matrix (+1 for possible water overflow)
    shape = np.amax([(c[0].stop + 1, c[1].stop + 1) for c in clays], axis=0)
    grid = np.full(shape, SAND)

    # counting area (min y, max y)
    area = min([c[1].start for c in clays]), shape[1] - 1

    # fill spring of water and clay
    grid[SPRING_LOCATION] = SPRING
    for clay in clays:
        grid[clay] = CLAY

    return grid, area


def print_grid(grid):
    result = ""
    for row in grid.T:
        for val in row:
            sym = SYMBOLS[val]
            if val == SPRING:
                result += f'{Fore.BLUE}{sym}{Style.RESET_ALL}'
            elif val == SAND:
                result += f'{Fore.LIGHTBLACK_EX}{sym}{Style.RESET_ALL}'
            elif val == DRY:
                result += f'{Back.BLUE}{sym}{Style.RESET_ALL}'
            elif val == WATER:
                result += f'{Back.BLUE}{sym}{Style.RESET_ALL}'
            elif val == CLAY:
                result += f'{Back.LIGHTBLACK_EX}{Fore.WHITE}{sym}{Style.RESET_ALL}'
        result += '\n'

    print(result)
    print()


if __name__ == "__main__":
    os.system('cls')
    print()

    print(solve(*_parse(open(r"../assets/day17_demo.txt").readlines()), debug=False))
    print(solve(*_parse(open(r"../assets/day17.txt").readlines())))
