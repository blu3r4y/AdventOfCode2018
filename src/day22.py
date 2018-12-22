# Advent of Code 2018, Day 22
# (c) blu3r4y

from queue import PriorityQueue

import numpy as np
from colorama import Fore, Style

NOTOOL, TORCH, GEAR = 0, 1, 2
ROCKY, WET, NARROW = 0, 1, 2
SYMBOLS = {0: '.', 1: '=', 2: '|'}


def part1(depth, target):
    cave = build_cave(depth, target)

    # select and sum the subregion
    region = cave[0:target[0] + 1, 0:target[1] + 1]
    return np.sum(region)


def part2(depth, target):
    cave = build_cave(depth, target)

    # find the path to the target with the torch tool in the hand
    _, costs = a_star_search(cave, (0, 0), target)
    return costs[(target, TORCH)]


def build_cave(depth, target, overhang=(100, 100)):
    xs, ys = np.array(target) + overhang

    # geological index and erosion
    geo, erosion = np.zeros((xs, ys), dtype=int), np.zeros((xs, ys), dtype=int)

    geo[:, 0] = np.arange(xs) * 16807
    geo[0, :] = np.arange(ys) * 48271

    erosion[:, 0] = (geo[:, 0] + depth) % 20183
    erosion[0, :] = (geo[0, :] + depth) % 20183

    # determine geological index and erosion
    for x in range(1, xs):
        for y in range(1, ys):
            if not (x, y) == target:
                geo[x, y] = erosion[x - 1, y] * erosion[x, y - 1]
                erosion[x, y] = (geo[x, y] + depth) % 20183

    # calculate the region type
    cave = erosion % 3
    return cave


def a_star_search(cave, start, goal):
    start = (start, TORCH)
    goal = (goal, TORCH)

    # manhattan distance (admissible)
    def _heuristic(a, b):
        ((x1, y1), _), ((x2, y2), _) = a, b
        return abs(x1 - x2) + abs(y1 - y2)

    # cost of moving from current region to next one
    def _cost(current, neighbor):
        pos_cur, tool_cur = current
        pos_nxt, tool_nxt = neighbor

        assert pos_cur != pos_nxt or tool_cur != tool_nxt

        # 7 minutes for a tool switch, 1 minute for a regular move
        return 7 if tool_cur != tool_nxt else 1

    def _neighbors(current):
        pos, tool = current
        region = cave[pos]
        x, y = pos

        children = []

        # tool switching options
        if region == ROCKY:
            children.append((pos, GEAR) if tool == TORCH else (pos, TORCH))
        elif region == WET:
            children.append((pos, GEAR) if tool == NOTOOL else (pos, NOTOOL))
        elif region == NARROW:
            children.append((pos, TORCH) if tool == NOTOOL else (pos, NOTOOL))

        # available adjacent cells
        adjacent = [(x + dxy[0], y + dxy[1])
                    for dxy in [(-1, 0), (0, -1), (0, 1), (1, 0)]
                    if (0 <= x + dxy[0] < cave.shape[0]) and (0 <= y + dxy[1] < cave.shape[1])]

        # filter out those regions, that are not reachable with the current tool
        for adj in adjacent:
            adj_region = cave[adj]
            if adj_region == ROCKY and (tool in (GEAR, TORCH)) \
                    or adj_region == WET and (tool in (GEAR, NOTOOL)) \
                    or adj_region == NARROW and (tool in (TORCH, NOTOOL)):
                children.append((adj, tool))

        return children

    # A* Search Algorithm
    # (c) https://www.redblobgames.com/pathfinding/a-star/implementation.html#python-astar

    # next nodes to be observed (greedy)
    fringe = PriorityQueue()
    fringe.put((0, start))
    # total costs for getting to any point
    costs = {start: 0}
    # parent relationships for backtracking the path
    parents = {start: None}

    while not fringe.empty():
        _, cur = fringe.get()

        # goal reached!
        if cur == goal:
            break

        # expand current position
        for nxt in _neighbors(cur):
            # add costs to the neighbor
            new_cost = costs[cur] + _cost(cur, nxt)
            # put the node into the fringe if the costs are lower
            if nxt not in costs or new_cost < costs[nxt]:
                costs[nxt] = new_cost
                priority = new_cost + _heuristic(goal, nxt)
                fringe.put((priority, nxt))
                parents[nxt] = cur

    return parents, costs


def print_cave(cave, target, mark=None):
    result = ""
    for y in range(cave.shape[1]):
        for x in range(cave.shape[0]):
            if mark and (x, y) == mark:
                result += f'{Fore.RED}X{Style.RESET_ALL}'
            elif (x, y) == (0, 0):
                result += 'M'
            elif (x, y) == target:
                result += 'T'
            else:
                result += SYMBOLS[cave[x, y]]
        result += '\n'
    print(result)


if __name__ == "__main__":
    print(part1(510, (10, 10)))
    print(part1(3066, (13, 726)))

    print(part2(510, (10, 10)))
    print(part2(3066, (13, 726)))
