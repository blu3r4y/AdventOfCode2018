# Advent of Code 2018, Day 7
# (c) blu3r4y

import networkx as nx

from parse import parse


def part1(steps):
    g = nx.DiGraph()
    g.add_edges_from(steps)

    # this is problem is exactly the topological sort of a graph
    return ''.join(nx.lexicographical_topological_sort(g))


def part2(steps, num_workers, offset):
    g = nx.DiGraph()
    g.add_edges_from(steps)

    # dicts storing the time left and active task/node per worker
    times = {i: 0 for i in range(num_workers)}
    tasks = {i: None for i in range(num_workers)}

    time = 0

    # process the graph until there are no nodes left
    while g.number_of_nodes() > 0:

        # nodes without predecessors that are not assigned to a worker already
        fringe = filter(lambda e: len(list(g.predecessors(e))) == 0, nx.nodes(g))
        fringe = list(sorted(set(fringe) - set(tasks.values())))

        # workers without tasks ...
        for worker in filter(lambda w: times[w] <= 0, times.keys()):
            if len(fringe) == 0:
                break

            # assign the first task from the fringe
            task = fringe.pop(0)
            if task:
                times[worker] = step_length(task, offset)
                tasks[worker] = task

        # decrease the time on each worker ...
        for worker in times.keys():
            times[worker] -= 1
            if times[worker] == 0:
                # remove finished nodes
                g.remove_node(tasks[worker])

        time += 1

    return time


def step_length(ch, offset):
    return 1 + offset + ord(ch) - ord('A')


def _parse(lines):
    steps = []
    for line in lines:
        a, b = parse("Step {} must be finished before step {} can begin.", line)
        steps.append((a, b))
    return steps


if __name__ == "__main__":
    print(part1(_parse(open(r"../assets/day7_demo.txt").readlines())))
    print(part1(_parse(open(r"../assets/day7.txt").readlines())))

    print(part2(_parse(open(r"../assets/day7_demo.txt").readlines()), 2, 0))
    print(part2(_parse(open(r"../assets/day7.txt").readlines()), 5, 60))
