# Advent of Code 2018, Day 16
# (c) blu3r4y

from collections import namedtuple

from parse import parse

OPERATIONS = ['addr', 'addi', 'mulr', 'muli', 'banr', 'bani', 'borr', 'bori',
              'setr', 'seti', 'gtir', 'gtri', 'gtrr', 'eqir', 'eqri', 'eqrr']

Observation = namedtuple("Observation", ["instruction", "before", "after"])


def part1(observations):
    three_or_more = 0

    for obsv in observations:

        # execute all possible candidates
        num_matches = 0
        for op in OPERATIONS:
            if obsv.after == execute(obsv.instruction, obsv.before, op):
                num_matches += 1

        # count observations with three or more possible operations
        if num_matches >= 3:
            three_or_more += 1

    return three_or_more


def part2(observations, program):
    # store possible candidates for every opcode
    operations = {i: set(OPERATIONS) for i in range(len(OPERATIONS))}

    for obsv in observations:

        matching_operations = set()
        opcode = obsv.instruction[0]

        # execute all possible candidates
        for op in operations[opcode]:
            if obsv.after == execute(obsv.instruction, obsv.before, op):
                matching_operations.add(op)

        # keep only the matching operations
        operations[opcode] = matching_operations

        # if we uniquely identified an operation ...
        if len(matching_operations) == 1:
            unique_op = next(iter(matching_operations))

            # ... remove it from the other mappings
            for key in set(operations.keys()) - {opcode}:
                operations[key].discard(unique_op)

    # map set values to scalar
    operations = {i: ops.pop() for i, ops in operations.items()}

    # interpret the program
    reg = [0, 0, 0, 0]
    for instruction in program:
        reg = execute(instruction, reg, operations[instruction[0]])

    return reg[0]


def execute(instruction, reg, op):
    _, a, b, c = instruction
    reg = list(reg)  # copy register

    if op == 'addr':
        reg[c] = reg[a] + reg[b]
    elif op == 'addi':
        reg[c] = reg[a] + b
    elif op == 'mulr':
        reg[c] = reg[a] * reg[b]
    elif op == 'muli':
        reg[c] = reg[a] * b
    elif op == 'banr':
        reg[c] = reg[a] & reg[b]
    elif op == 'bani':
        reg[c] = reg[a] & b
    elif op == 'borr':
        reg[c] = reg[a] | reg[b]
    elif op == 'bori':
        reg[c] = reg[a] | b
    elif op == 'setr':
        reg[c] = reg[a]
    elif op == 'seti':
        reg[c] = a
    elif op == 'gtir':
        reg[c] = 1 if a > reg[b] else 0
    elif op == 'gtri':
        reg[c] = 1 if reg[a] > b else 0
    elif op == 'gtrr':
        reg[c] = 1 if reg[a] > reg[b] else 0
    elif op == 'eqir':
        reg[c] = 1 if a == reg[b] else 0
    elif op == 'eqri':
        reg[c] = 1 if reg[a] == b else 0
    elif op == 'eqrr':
        reg[c] = 1 if reg[a] == reg[b] else 0

    return reg


def _parse(lines):
    observations, program, i = [], [], 0

    # parse observations
    while i < len(lines):
        before = parse("Before: [{:d}, {:d}, {:d}, {:d}]", lines[i].strip())
        instruction = parse("{:d} {:d} {:d} {:d}", lines[i + 1].strip())
        after = parse("After:  [{:d}, {:d}, {:d}, {:d}]", lines[i + 2].strip())

        i += 4

        if not (before and after and instruction):
            break

        observations.append(Observation([*instruction], [*before], [*after]))

    # parse program
    for line in lines[i - 2:]:
        program.append(list(map(int, line.strip().split(' '))))

    return observations, program


if __name__ == "__main__":
    print(part1(_parse(open(r"../assets/day16.txt").readlines())[0]))
    print(part2(*_parse(open(r"../assets/day16.txt").readlines())))
