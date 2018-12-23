# Advent of Code 2018, Day 23
# (c) blu3r4y

import networkx as nx
from parse import parse

X, Y, Z, RANGE = 0, 1, 2, 3
ORIGIN = (0, 0, 0, 0)


def part1(bots):
    # find the nanobot with the largest range
    strongest = max(bots, key=lambda bot: bot[RANGE])
    distances = [manhattan(bot, strongest) for bot in bots]

    # number of nanobots in range of the strongest nanobot
    return len([d for d in distances if d <= strongest[RANGE]])


def part2(bots):
    # build a graph with edges between overlapping nanobots
    graph = nx.Graph()
    for bot in bots:
        # two bots overlap if their distance is smaller or equal than the sum of their ranges
        overlaps = [(bot, other) for other in bots if manhattan(bot, other) <= bot[RANGE] + other[RANGE]]
        graph.add_edges_from(overlaps)

    # find sets of overlapping nanobots (i.e. fully-connected sub-graphs)
    cliques = list(nx.find_cliques(graph))
    cliques_size = [len(c) for c in cliques]

    assert len([s for s in cliques_size if s == max(cliques_size)]) == 1

    # select the largest cluster of overlapping nanobots (maximum clique sub-graph)
    clique = max(cliques, key=len)

    # calculate the point on the nanobots surface which is closest to the origin
    surfaces = [manhattan(ORIGIN, bot) - bot[RANGE] for bot in clique]

    # the furthest away surface point is the minimum manhattan distance
    return max(surfaces)


def manhattan(a, b):
    (x1, y1, z1, _), (x2, y2, z2, _) = a, b
    return abs(x1 - x2) + abs(y1 - y2) + abs(z1 - z2)


def _parse(lines):
    # list of tuples (x, y, z, range)
    return [tuple(parse("pos=<{:d},{:d},{:d}>, r={:d}", line)) for line in lines]


if __name__ == "__main__":
    print(part1(_parse(open(r"../assets/day23_demo1.txt").readlines())))
    print(part1(_parse(open(r"../assets/day23.txt").readlines())))

    print(part2(_parse(open(r"../assets/day23_demo2.txt").readlines())))
    print(part2(_parse(open(r"../assets/day23.txt").readlines())))
