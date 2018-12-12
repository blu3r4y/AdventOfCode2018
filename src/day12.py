# Advent of Code 2018, Day 12
# (c) blu3r4y


def part1(pots, rules):
    return solve(pots, rules, 20)


def part2(pots, rules):
    return solve(pots, rules, 50000000000)


def solve(pots, rules, cycles):
    # put the pots in a canonical form (first and last pot directly on the edges and offset notation)
    offset = pots.index('#')
    offset_end = pots.rindex('#')
    pots = pots[offset:offset_end + 1]

    for gen in range(cycles):
        delta, pots_ = spread(pots, rules)

        # break cycles and only consider the offset
        if pots_ == pots:
            offset += delta * (cycles - gen)
            break

        pots = pots_
        offset += delta

    # sum the pot indexes
    return sum([(i + offset) * (1 if val == '#' else 0) for i, val in enumerate(pots)])


def spread(pots, rules):
    # make room for patterns that would match on the edges
    pots = "." * 3 + ''.join(pots) + "." * 3
    # empty pot for the next iteration
    pots_new = ["."] * len(pots)

    for pattern, value in rules.items():
        # search for all matches of the pattern (+ overlapping ones)
        matches = [i + 2 for i in range(len(pots)) if pots.startswith(pattern, i)]
        for match in matches:
            pots_new[match] = value

    # return in canonical form (offset and bounding box)
    first_pot = pots_new.index('#')
    last_pot = len(pots_new) - 1 - pots_new[::-1].index('#')
    return first_pot - 3, ''.join(pots_new[first_pot:last_pot + 1])


def parse(lines):
    # parse the initial pot
    pots = lines[0].split(": ")[1].strip()

    # parse the pattern rules
    rules = {}
    for pattern in lines[2:]:
        rule = pattern.split(" => ")
        rules[rule[0]] = rule[1].strip()

    return pots, rules


if __name__ == "__main__":
    print(part1(*parse(open(r"../assets/day12_demo.txt").readlines())))
    print(part1(*parse(open(r"../assets/day12.txt").readlines())))

    print(part2(*parse(open(r"../assets/day12_demo.txt").readlines())))
    print(part2(*parse(open(r"../assets/day12.txt").readlines())))
