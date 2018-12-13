# Advent of Code 2018, Day 13
# (c) blu3r4y

from collections import defaultdict
from enum import IntEnum
from itertools import tee

import networkx as nx
import numpy as np


def part1(graph: nx.Graph, carts):
    return solve(graph, carts)


def part2(graph: nx.Graph, carts):
    return solve(graph, carts, True)


def solve(graph: nx.Graph, carts, delete_on_crash=False):
    # save the turning strategy with the cart location (x, y) as its key
    turns = defaultdict(lambda: TurnStrategy.Left)

    while True:

        # iterate over cart positions
        for pos in sorted(carts.keys()):
            # a previous crash could might removed this cart already
            if pos not in carts:
                continue

            # neigbors, which also exist in the graph
            options = list(filter(lambda tup: graph.has_edge(pos, tup[1]), carts[pos].next_neighbors(pos)))

            new_facing, new_pos = options[0]

            # intersection? (use turn-rule and set next turn)
            if len(options) > 1:
                new_facing, new_pos = options[turns[pos]]
                turns[pos] = turns.pop(pos).next_turn()

            if new_pos in carts:
                # crash detected
                if delete_on_crash:
                    del carts[pos]
                    del carts[new_pos]
                else:
                    # (part 1) first crash position
                    return ','.join(map(str, reversed(new_pos)))

            else:
                # cart moved (change position key)
                carts[new_pos] = new_facing
                turns[new_pos] = turns[pos]
                del carts[pos]

        # (part 2) position of single cart left
        if delete_on_crash and len(carts) == 1:
            return ','.join(map(str, reversed(next(iter(carts.keys())))))


class TurnStrategy(IntEnum):
    Left = 0
    Straight = 1
    Right = 2

    def next_turn(self):
        # Left -> Straight -> Right -> Left -> ...
        return TurnStrategy((self + 1) % 3)


class Direction(IntEnum):
    Up = 0
    Down = 1
    Left = 2
    Right = 3

    @staticmethod
    def from_char(ch):
        if ch == '^':
            return Direction.Up
        elif ch == 'v':
            return Direction.Down
        elif ch == '<':
            return Direction.Left
        elif ch == '>':
            return Direction.Right

    def as_offset(self):
        # offset within the matrix if you go in this direction
        if self == Direction.Up:
            return np.array((-1, 0))
        elif self == Direction.Down:
            return np.array((1, 0))
        elif self == Direction.Left:
            return np.array((0, -1))
        elif self == Direction.Right:
            return np.array((0, 1))

    def next_neighbors(self, pos):
        options = []

        # possible set of directions when moving in [left, straight, right] order
        if self == Direction.Up:
            options = [Direction.Left, Direction.Up, Direction.Right]
        elif self == Direction.Down:
            options = [Direction.Right, Direction.Down, Direction.Left]
        elif self == Direction.Left:
            options = [Direction.Down, Direction.Left, Direction.Up]
        elif self == Direction.Right:
            options = [Direction.Up, Direction.Right, Direction.Down]

        # tuples of (direction, (x, y)) with all possible options
        return zip(options, [tuple(pos + facing.as_offset()) for facing in options])


def parse_gridlines(matrix) -> nx.Graph:
    g = nx.Graph()

    def _pairwise(iterable):
        u, v = tee(iterable)
        next(v, None)
        return zip(u, v)

    # helper matrices
    rows = np.vectorize(lambda ch: ch in {'-', '+', '>', '<'})(matrix).astype(int)
    cols = np.vectorize(lambda ch: ch in {'|', '+', 'v', '^'})(matrix).astype(int)
    edges = np.vectorize(lambda ch: ch in {'/', '\\'})(matrix).astype(int)

    # horizontal connections
    for x, row in enumerate(rows):
        for (ay, a), (by, b) in _pairwise(enumerate(row)):
            if a == b == 1:
                g.add_edge((x, ay), (x, by))

    # vertical connections
    for y, col in enumerate(cols.T):
        for (ay, a), (by, b) in _pairwise(enumerate(col)):
            if a == b == 1:
                g.add_edge((ay, y), (by, y))

    # edge connections
    up, down, left, right = map(np.array, [(-1, 0), (1, 0), (0, -1), (0, 1)])
    for yx, edge in np.ndenumerate(edges):
        if edge == 1:

            is_up = cols[tuple(yx + up)] if yx[0] > 0 else 0
            is_down = cols[tuple(yx + down)] if yx[0] < cols.shape[0] - 1 else 0
            is_left = rows[tuple(yx + left)] if yx[1] > 0 else 0
            is_right = rows[tuple(yx + right)] if yx[1] < rows.shape[1] - 1 else 0

            # an edge must be within exactly one quadrant and have exactly two attached lines
            assert is_up + is_down + is_left + is_right == 2

            if is_right and is_up:  # 1st quadrant
                g.add_edge(tuple(yx), tuple(yx + right))
                g.add_edge(tuple(yx), tuple(yx + up))

            elif is_up and is_left:  # 4th quadrant
                g.add_edge(tuple(yx), tuple(yx + up))
                g.add_edge(tuple(yx), tuple(yx + left))

            elif is_left and is_down:  # 3rd quadrant
                g.add_edge(tuple(yx), tuple(yx + left))
                g.add_edge(tuple(yx), tuple(yx + down))

            elif is_down and is_right:  # 2nd quadrant
                g.add_edge(tuple(yx), tuple(yx + down))
                g.add_edge(tuple(yx), tuple(yx + right))

    return g


def parse(lines):
    # create a 2d char matrix from the lines
    row_length = max(map(len, lines)) - 1
    matrix = np.array([list(l.rstrip() + " " * (row_length - len(l.rstrip()))) for l in lines])

    # parse the matrix into a graph
    graph = parse_gridlines(matrix)

    # store the cart direction with the (x, y) location as their key
    carts = {}
    for yx, val in np.ndenumerate(matrix):
        if val in {'^', 'v', '>', '<'}:
            carts[yx] = Direction.from_char(val)

    return graph, carts


if __name__ == "__main__":
    print(part1(*parse(open(r"../assets/day13_demo1.txt").readlines())))
    print(part1(*parse(open(r"../assets/day13.txt").readlines())))

    print(part2(*parse(open(r"../assets/day13_demo2.txt").readlines())))
    print(part2(*parse(open(r"../assets/day13.txt").readlines())))
