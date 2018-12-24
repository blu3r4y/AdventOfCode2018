# Advent of Code 2018, Day 24
# (c) blu3r4y

from copy import deepcopy
from enum import IntEnum
from itertools import count

from parse import parse


class Faction(IntEnum):
    Immune = 0,
    Infect = 1

    def opposite(self):
        return Faction(1 if self == 0 else 0)

    def __repr__(self):
        return self.name


class Group():
    def __init__(self, id, faction, units, hp, ap, iv, element, immune, weak):
        self.id = id
        self.faction = faction
        self.units = units
        self.hp = hp
        self.ap = ap
        self.iv = iv
        self.element = element
        self.weak = weak or []
        self.immune = immune or []

    @property
    def ep(self):
        return self.units * self.ap

    def vulnerability(self, other):
        if other.element in self.immune:
            return 0
        elif other.element in self.weak:
            return 2 * other.ep
        return other.ep

    def attack(self, other):
        damage = other.vulnerability(self)
        kills = min(other.units, damage // other.hp)
        other.units -= kills

        return kills

    def __str__(self):
        return "{} Group {}".format(repr(self.faction), self.id)

    def __repr__(self):
        return "Group({} x {}, {} HP, {} {} AP, {} EP, {} IV, {} immune, {} weak)".format(
            repr(self.faction), self.units, self.hp, self.ap, self.element, self.ep, self.iv, self.immune, self.weak
        )

    @staticmethod
    def from_string(string, faction, id):
        units, hp, props, ap, element, iv = parse("{:d} units each with {:d} hit points{}with an attack "
                                                  "that does {:d} {} damage at initiative {:d}", string)
        # resolve immunities and weaknesses
        immune, weak = [], []
        if props != " ":
            props = props[2:-2].split('; ')
            for prop in props:
                imm_, weak_ = parse("immune to {}", prop), parse("weak to {}", prop)
                target, elements = immune if imm_ else weak, imm_[0] if imm_ else weak_[0]
                target.extend(elements.split(', '))

        return Group(id, faction, units, hp, ap, iv, element, immune, weak)


class Game():
    def __init__(self, immune, infect):
        self.groups = [immune, infect]

    def optimize(self):
        factory = deepcopy(self.groups)
        for boost in count():
            self.groups = deepcopy(factory)

            # search for the minimum boost required for the immune team to win
            winner, score = self.play(boost)
            if winner == Faction.Immune:
                return winner, score

    def play(self, boost=0):
        # apply boost
        for group in self.groups[Faction.Immune]:
            group.ap += boost

        # fight for as long as both groups have units left
        while all([any(g) for g in self.groups]):
            # let groups select targets, in order of largest EP (break ties on IV)
            groups = self.groups[Faction.Immune] + self.groups[Faction.Infect]
            groups = sorted(groups, key=lambda g: (-g.ep, -g.iv))

            # perform target selection
            taken = set()
            targets = [self.select_target(group, taken) for group in groups]

            # no targets remain
            if not any(targets):
                return None, 0

            # attack in decreasing order of IV
            fights = zip(groups, targets)
            fights = sorted(fights, key=lambda tup: -tup[0].iv)

            # attacking phase
            any_kills = False
            for group, target in fights:
                if target:
                    any_kills |= group.attack(target) > 0

                    # remove groups that lost all their units
                    if target.units == 0:
                        self.groups[target.faction].remove(target)

            # stalemate
            if not any_kills:
                return None, 0

        winner = Faction.Immune if len(self.groups[Faction.Immune]) > 0 else Faction.Infect
        score = sum([g.units for g in self.groups[winner]])

        # winner and number of its remaining units
        return winner, score

    def select_target(self, group, taken):
        # select targets by largest vulnerability (break ties on EP and IV)
        enemies = list(set(self.groups[group.faction.opposite()]) - taken)
        enemies = sorted(enemies, key=lambda g: (-g.vulnerability(group), -g.ep, -g.iv))

        # select if a vulnerable target remains
        if len(enemies) > 0 and enemies[0].vulnerability(group) > 0:
            taken.add(enemies[0])
            return enemies[0]

    @staticmethod
    def from_string(lines):
        immune, infect, i = [], [], 1

        # read immune groups
        while lines[i].strip() != '':
            immune.append(Group.from_string(lines[i], Faction.Immune, i))
            i += 1
        i += 2

        # read infection groups
        off = i - 1
        while i < len(lines):
            infect.append(Group.from_string(lines[i], Faction.Infect, i - off))
            i += 1

        return Game(immune, infect)


if __name__ == "__main__":
    print(Game.from_string(open(r"../assets/day24_demo.txt").readlines()).play())
    print(Game.from_string(open(r"../assets/day24.txt").readlines()).play())

    print(Game.from_string(open(r"../assets/day24_demo.txt").readlines()).play(boost=1570))
    print(Game.from_string(open(r"../assets/day24.txt").readlines()).optimize())
