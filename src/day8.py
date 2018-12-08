# Advent of Code 2018, Day 8
# (c) blu3r4y

import networkx as nx
import numpy as np


def part1(nodes):
    tree, metadata = _build_tree(nodes)
    return sum(map(sum, metadata.values()))


def part2(nodes):
    tree, metadata = _build_tree(nodes)

    def _value(node):
        childs = list(tree.successors(node))
        if len(childs) == 0:
            # sum the metadata for nodes without children
            return sum(metadata[node])

        # otherwise sum the values of children referenced by the metadata
        return sum([_value(childs[meta - 1]) for meta in metadata[node]
                    if meta <= len(childs)])

    return _value("1")


def _build_tree(nodes):
    tree, metadata = nx.DiGraph(), dict()

    def _read_node(name, parent, i):
        tree.add_edge(parent, name)

        num_childs, num_meta = nodes[i], nodes[i + 1]
        i += 2

        # read all the children nodes and then the metadata
        for child in range(num_childs):
            i = _read_node(name + str(child), name, i)
        metadata[name] = nodes[i:i + num_meta]

        return i + num_meta

    _read_node("1", None, 0)
    return tree, metadata


if __name__ == "__main__":
    print(part1(np.array([2, 3, 0, 3, 10, 11, 12, 1, 1, 0, 1, 99, 2, 1, 1, 2])))
    print(part1(np.loadtxt(r"../assets/day8.txt", dtype=int)))

    print(part2(np.array([2, 3, 0, 3, 10, 11, 12, 1, 1, 0, 1, 99, 2, 1, 1, 2])))
    print(part2(np.loadtxt(r"../assets/day8.txt", dtype=int)))
