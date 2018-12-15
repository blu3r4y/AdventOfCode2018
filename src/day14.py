# Advent of Code 2018, Day 14
# (c) blu3r4y


def part1(num_recipes):
    recipes = [3, 7]
    elf0, elf1 = 0, 1

    while len(recipes) < num_recipes + 10:
        # combine and pick recipes
        combine(recipes, elf0, elf1)
        elf0, elf1 = pick(recipes, elf0, elf1)

    # the 10 recipes after the num_recipes we made
    return ''.join(map(str, recipes[num_recipes:num_recipes + 10]))


def part2(needle):
    needle = [int(d) for d in str(needle)]

    recipes = [3, 7]
    elf0, elf1 = 0, 1

    # search index offset
    h = 0

    while True:
        # combine and pick recipes
        combine(recipes, elf0, elf1)
        elf0, elf1 = pick(recipes, elf0, elf1)

        # efficient search for the sequence in the recipes list
        i, h = sequential_find(recipes, needle, h)
        if i != -1:
            return i


def combine(recipes, elf0, elf1):
    recipe_sum = recipes[elf0] + recipes[elf1]
    if recipe_sum >= 10:
        recipes.append(1)
    recipes.append(recipe_sum % 10)


def pick(recipes, elf0, elf1):
    elf0 = (elf0 + 1 + recipes[elf0]) % len(recipes)
    elf1 = (elf1 + 1 + recipes[elf1]) % len(recipes)
    return elf0, elf1


def sequential_find(haystack, needle, h=0):
    # h is the start index for the search

    # as long as the needle can fit in the haystack ...
    while len(haystack) - h >= len(needle):
        try:
            h = haystack.index(needle[0], h)  # index of first needle value
        except ValueError:
            return -1, len(haystack) - 1  # first needle value is beyond the haystack

        # check the remaining needle values
        for i in range(1, len(needle)):
            if h + i >= len(haystack) or haystack[h + i] != needle[i]:
                # first mismatch, add +1 to the search position
                h += 1
                break
        else:
            # all values match, found needle!
            return h, None

    # no match, return next start index
    return -1, h - 1


if __name__ == "__main__":
    print(part1(9))
    print(part1(5))
    print(part1(18))
    print(part1(2018))
    print(part1(760221))

    print(part2("51589"))
    print(part2("01245"))
    print(part2("92510"))
    print(part2("59414"))
    print(part2("760221"))
