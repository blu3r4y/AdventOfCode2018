# Advent of Code 2018, Day 20
# (c) blu3r4y

from copy import copy

import networkx as nx
from parglare import Parser, Grammar
from parglare.actions import pass_single, pass_inner

GRAMMAR = r"""
root: '^' expression '$';
expression: element+;

element: direction | branch;

branch: '(' option+ ')';
option: expression | '|' expression?;

terminals
direction: /[NSEW]/;
"""


def part1(sequence):
    graph = build_graph(sequence)

    # longest distance to any other node, starting at (0, 0)
    return nx.eccentricity(graph, (0, 0))


def part2(sequence):
    graph = build_graph(sequence)

    # all the shortest path lengths, starting at (0, 0)
    shortest_paths = nx.single_source_shortest_path_length(graph, (0, 0))
    # number of paths longer or equal than 1.000
    return len([v for k, v in shortest_paths.items() if v >= 1000])


def parse(regex):
    actions = {
        "root": pass_inner,
        "branch": pass_inner,
        "option": [pass_single, lambda _, nodes: nodes[1] or -1]
    }

    parser = Parser(Grammar.from_string(GRAMMAR), actions=actions)
    sequence = parser.parse(regex)

    return sequence


def build_graph(sequence):
    graph = nx.Graph()

    def _move(directions, starts):
        # keep all the end points generated so far
        ends = starts

        for di in directions:

            # is branching necessary?
            if isinstance(di, list):

                next_ends = []
                for option in di:
                    if option != -1:
                        # move along each branch option and store the new end points
                        next_ends.extend(_move(option, copy(ends)))

                if -1 in di:
                    # this branch can be skipped, so we just append the newly found end points
                    ends.extend(next_ends)
                else:
                    # only keep the new end points otherwise
                    ends = next_ends
            else:

                # move every endpoint towards the desired direction
                # and create an edge within the graph
                for i in range(len(ends)):
                    pre = ends[i]

                    nxt = offset(pre, di)
                    graph.add_edge(pre, nxt)

                    ends[i] = nxt

        # return all the unique end points
        return list(set(ends))

    # build the graph by moving within the grid, starting at (0, 0)
    _move(sequence, [(0, 0)])

    return graph


def offset(node, direction):
    (x, y) = node
    if direction == 'N':
        return x, y + 1
    elif direction == 'S':
        return x, y - 1
    elif direction == 'E':
        return x + 1, y
    elif direction == 'W':
        return x - 1, y


if __name__ == "__main__":
    print(part1(parse("^WNE$")))
    print(part1(parse("^ENWWW(NEEE|SSE(EE|N))$")))
    print(part1(parse("^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$")))
    print(part1(parse("^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$")))
    print(part1(parse("^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$")))

    print(part1(parse(open(r"../assets/day20.txt").readlines()[0])))
    print(part2(parse(open(r"../assets/day20.txt").readlines()[0])))
