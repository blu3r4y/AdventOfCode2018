# Advent of Code 2018, Day 19
# (c) blu3r4y

ADDR, ADDI, MULR, MULI, BANR, BANI, BORR, BORI, SETR, SETI, GTIR, GTRI, GTRR, EQIR, EQRI, EQRR = range(16)

OPERATIONS = ['addr', 'addi', 'mulr', 'muli', 'banr', 'bani', 'borr', 'bori',
              'setr', 'seti', 'gtir', 'gtri', 'gtrr', 'eqir', 'eqri', 'eqrr']


def solve(instructions, ip, optimize_for_part2=False):
    # set register 0 to 1 in part 2
    reg = [1] + [0] * 5 if optimize_for_part2 else [0] * 6

    # execute the program as long as the ip is valid
    while 0 <= reg[ip] < len(instructions):
        ins = instructions[reg[ip]]

        # initialization for part 2 is done at instruction 35
        if optimize_for_part2 and reg[ip] == 35:
            return optimized_loop(reg)

        execute(*ins, reg)
        reg[ip] += 1

    # undo last increment operation
    reg[ip] -= 1

    return reg[0]


def optimized_loop(reg):
    a, b, c, d, ip, f = reg

    # manually disassembled code ... (too slow)

    # f = 1  # 1
    # while f <= d:  # 13 - 15
    #     b = 1  # 2
    #     while b <= d:  # 9 - 11
    #         if (f * b) == d:  # 3 - 6
    #             a += f  # 7
    #         b += 1  # 8
    #     f += 1  # 12

    # optimized inner loop, that checks for factors faster

    f = 1  # 1
    while f <= d:  # 13 - 15
        if d % f == 0:
            a += f
        f += 1  # 12

    return a


def execute(op, a, b, c, reg):
    if op == ADDR:
        reg[c] = reg[a] + reg[b]
    elif op == ADDI:
        reg[c] = reg[a] + b
    elif op == MULR:
        reg[c] = reg[a] * reg[b]
    elif op == MULI:
        reg[c] = reg[a] * b
    elif op == BANR:
        reg[c] = reg[a] & reg[b]
    elif op == BANI:
        reg[c] = reg[a] & b
    elif op == BORR:
        reg[c] = reg[a] | reg[b]
    elif op == BORI:
        reg[c] = reg[a] | b
    elif op == SETR:
        reg[c] = reg[a]
    elif op == SETI:
        reg[c] = a
    elif op == GTIR:
        reg[c] = 1 if a > reg[b] else 0
    elif op == GTRI:
        reg[c] = 1 if reg[a] > b else 0
    elif op == GTRR:
        reg[c] = 1 if reg[a] > reg[b] else 0
    elif op == EQIR:
        reg[c] = 1 if a == reg[b] else 0
    elif op == EQRI:
        reg[c] = 1 if reg[a] == b else 0
    elif op == EQRR:
        reg[c] = 1 if reg[a] == reg[b] else 0


def explain_program(instructions, ip):
    print()
    for i, ins in enumerate(instructions):
        print("{:>2} {:<5} {}".format(i, OPERATIONS[ins[0]], explain(*ins, ip)))


def explain(op, a, b, c, ip):
    names = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', ip: 'IP'}

    if op == ADDR:
        return "{} = {} + {}".format(names[c], names[a], names[b])
    elif op == ADDI:
        return "{} = {} + {}".format(names[c], names[a], b)
    elif op == MULR:
        return "{} = {} * {}".format(names[c], names[a], names[b])
    elif op == MULI:
        return "{} = {} * {}".format(names[c], names[a], b)
    elif op == BANR:
        return "{} = {} & {}".format(names[c], names[a], names[b])
    elif op == BANI:
        return "{} = {} & {}".format(names[c], names[a], b)
    elif op == BORR:
        return "{} = {} | {}".format(names[c], names[a], names[b])
    elif op == BORI:
        return "{} = {} | {}".format(names[c], names[a], b)
    elif op == SETR:
        return "{} = {}".format(names[c], names[a])
    elif op == SETI:
        return "{} = {}".format(names[c], a)
    elif op == GTIR:
        return "{} = {} > {} ?".format(names[c], a, names[b])
    elif op == GTRI:
        return "{} = {} > {} ?".format(names[c], names[a], b)
    elif op == GTRR:
        return "{} = {} > {} ?".format(names[c], names[a], names[b])
    elif op == EQIR:
        return "{} = {} == {} ?".format(names[c], a, names[b])
    elif op == EQRI:
        return "{} = {} == {} ?".format(names[c], names[a], b)
    elif op == EQRR:
        return "{} = {} == {} ?".format(names[c], names[a], names[b])


def parse(lines):
    instructions, ip = [], int(lines[0].split()[1])

    for line in lines[1:]:
        parts = line.split()
        instructions.append((OPERATIONS.index(parts[0]), *map(int, parts[1:])))

    return instructions, ip


if __name__ == "__main__":
    print(solve(*parse(open(r"../assets/day19_demo.txt").readlines())))
    print(solve(*parse(open(r"../assets/day19.txt").readlines())))

    print(solve(*parse(open(r"../assets/day19.txt").readlines()), optimize_for_part2=True))

    # print the entire program for better understanding
    explain_program(*parse(open(r"../assets/day19.txt").readlines()))
