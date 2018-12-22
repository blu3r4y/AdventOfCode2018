# Advent of Code 2018, Day 21
# (c) blu3r4y

from day19 import execute, parse, explain_program


def solve(instructions, ip, return_first_match=True):
    reg = [0] * 6
    seen, last_goal = set(), 0

    # execute the program as long as the ip is valid
    while 0 <= reg[ip] < len(instructions):
        ins = instructions[reg[ip]]

        # optimize the integer division, which is attempted between instructions 17 - 27
        if reg[ip] == 17:
            reg[4] = reg[4] // 256
            reg[ip] = 8
            continue

        # manually disassembled code ... (too slow)
        #
        # d = 0
        # while True:
        #     c = d + 1
        #     c = c * 256
        #
        #     if c > e:
        #         e = d
        #         break
        #     else:
        #         d = d + 1

        # instruction 28 compares the value in register 0 with register 5
        if reg[ip] == 28:
            goal = reg[5]

            # [...] halt after executing the fewest instructions
            if return_first_match:
                return goal

            # [...] halt after executing the most instructions
            if goal in seen:
                return last_goal
            seen.add(goal)
            last_goal = goal

        execute(*ins, reg)
        reg[ip] += 1


if __name__ == "__main__":
    print(solve(*parse(open(r"../assets/day21.txt").readlines())))
    print(solve(*parse(open(r"../assets/day21.txt").readlines()),
                return_first_match=False))

    # print the entire program for better understanding
    explain_program(*parse(open(r"../assets/day21.txt").readlines()))
