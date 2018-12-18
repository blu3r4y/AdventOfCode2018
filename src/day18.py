# Advent of Code 2018, Day 18
# (c) blu3r4y

import numpy as np

OPEN, TREE, LUMBER = 0, 1, 2
NUMBERS = {'.': OPEN, '|': TREE, '#': LUMBER}
SYMBOLS = {v: k for k, v in NUMBERS.items()}

# adjacent cell offsets
GRID_OFFSETS = [(-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0)]


def solve(grid, total_minutes):
    # store hashes of seen grids (key) and at which minute (value)
    backlog = {hash(grid.tostring()): 0}

    minute = 0
    while minute < total_minutes:

        reference = np.copy(grid)
        for (x, y), cell in np.ndenumerate(grid):
            num_tree = num_symbol(neighbors(x, y, reference), TREE)
            num_lumber = num_symbol(neighbors(x, y, reference), LUMBER)

            # apply transformation rules
            if cell == OPEN and num_tree >= 3:
                grid[x, y] = TREE
            elif cell == TREE and num_lumber >= 3:
                grid[x, y] = LUMBER
            elif cell == LUMBER and not (num_lumber > 0 and num_tree > 0):
                grid[x, y] = OPEN

        minute += 1

        # store the hash of this grid
        key = hash(grid.tostring())
        if key not in backlog:
            backlog[key] = minute
        else:
            # cycle-break forward if we have already seen this grid hash before
            delta = (total_minutes - minute) % (minute - backlog[key])
            minute = total_minutes - delta

    # count tree and lumber resources
    return num_symbol(grid.ravel(), TREE) * num_symbol(grid.ravel(), LUMBER)


def num_symbol(cells, symbol):
    return sum(1 for c in cells if c == symbol)


def neighbors(x, y, grid):
    return (grid[x + dxy[0]][y + dxy[1]]
            for dxy in GRID_OFFSETS
            if (0 <= x + dxy[0] < grid.shape[0]) and (0 <= y + dxy[1] < grid.shape[1]))


def parse(lines):
    shape = (len(lines), len(lines[0].strip()))
    grid = np.zeros(shape, dtype=int)
    for x in range(shape[0]):
        for y in range(shape[1]):
            grid[x, y] = NUMBERS[lines[x][y]]
    return grid


if __name__ == "__main__":
    print(solve(parse(open(r"../assets/day18_demo.txt").readlines()), 10))
    print(solve(parse(open(r"../assets/day18.txt").readlines()), 10))

    print(solve(parse(open(r"../assets/day18_demo.txt").readlines()), 1000000000))
    print(solve(parse(open(r"../assets/day18.txt").readlines()), 1000000000))
