# Advent of Code 2018, Day 25
# (c) blu3r4y

import numpy as np
import networkx as nx

from itertools import product


def part1(points):
    graph = nx.Graph()
    for i, j in product(range(len(points)), repeat=2):
        # two points share a constellation if the are <= 3 apart
        if manhattan(points[i], points[j]) <= 3:
            graph.add_edge(i, j)

    # number of constellations
    return nx.number_connected_components(graph)


def manhattan(a, b):
    return np.sum(np.abs(a - b))


def parse(lines):
    return np.array([tuple(map(int, line.strip().split(','))) for line in lines])


if __name__ == "__main__":
    print(part1(parse(open(r"../assets/day25_demo1.txt").readlines())))
    print(part1(parse(open(r"../assets/day25_demo2.txt").readlines())))
    print(part1(parse(open(r"../assets/day25_demo3.txt").readlines())))
    print(part1(parse(open(r"../assets/day25_demo4.txt").readlines())))

    print(part1(parse(open(r"../assets/day25.txt").readlines())))
