# Advent of Code 2018, Day 4
# (c) blu3r4y

import datetime

import numpy as np

from parse import parse
from functools import partial
from collections import namedtuple, defaultdict

Guard = namedtuple("Guard", ["id", "shift", "asleep"])


def part1(guards):
    return solve(guards)[0]


def part2(guards):
    return solve(guards)[1]


def solve(guards):
    # fill a matrix with the slept minutes, per guard
    minutes = defaultdict(partial(np.zeros, 60))
    for guard in guards:
        for asleep in guard.asleep:
            t = asleep[0]
            while t < asleep[1]:
                minutes[guard.id][t.minute] += 1
                t += datetime.timedelta(minutes=1)

    # strategy 1: most slept minute of the most sleepy guard
    guard1 = max(minutes.keys(), key=lambda guard: np.sum(minutes[guard]))

    # strategy 2: most slept minute of all guards
    guard2 = max(minutes.keys(), key=lambda guard: np.max(minutes[guard]))

    return guard1 * np.argmax(minutes[guard1]), guard2 * np.argmax(minutes[guard2])


def _parse(lines):
    guards = []
    for line in sorted(lines, key=lambda line: parse("[{time:ti}] {}", line)['time']):
        begin_ = parse("[{time:ti}] Guard #{id:d} begins shift", line)
        asleep_ = parse("[{time:ti}] falls asleep", line)
        wakeup_ = parse("[{time:ti}] wakes up", line)

        if begin_:  guards.append(Guard(id=begin_['id'], shift=begin_['time'], asleep=[]))
        if asleep_: guards[-1].asleep.append([asleep_['time'], None])
        if wakeup_: guards[-1].asleep[-1][1] = wakeup_['time']

    return guards


if __name__ == "__main__":
    print(part1(_parse(open(r"../assets/day4_demo.txt").readlines())))
    print(part1(_parse(open(r"../assets/day4.txt").readlines())))

    print(part2(_parse(open(r"../assets/day4_demo.txt").readlines())))
    print(part2(_parse(open(r"../assets/day4.txt").readlines())))
