# Advent of Code 2018, Day 15
# (c) blu3r4y

import os
import copy
from abc import abstractmethod
from enum import Enum
from itertools import count
from typing import List, Optional

from colorama import Fore, Back, Style


class Cell:
    """
    Abstract class for any cell within the matrix
    """

    @abstractmethod
    def __init__(self, maze, x, y):
        self.maze = maze
        self.x = x
        self.y = y


class Air(Cell):
    """
    A free spot in the matrix
    """

    def __init__(self, maze, x, y):
        super().__init__(maze, x, y)

    def __str__(self):
        return "."

    def __repr__(self):
        return "Air({}, {})".format(self.x, self.y)


class Wall(Cell):
    """
    An obstacle in the matrix
    """

    def __init__(self, maze, x, y):
        super().__init__(maze, x, y)

    def __str__(self):
        return "#"

    def __repr__(self):
        return "Wall({}, {})".format(self.x, self.y)


class PlayerFaction(Enum):
    Goblin = 0,
    Elf = 1

    def opponent(self):
        # resolve the opposite team
        return PlayerFaction.Goblin if self == PlayerFaction.Elf else PlayerFaction.Elf

    def __str__(self):
        return "E" if self == PlayerFaction.Elf else "G"

    def __repr__(self):
        return self.name


class Player(Cell):
    """
    A player within the matrix (elf or goblin)
    """

    def __init__(self, maze, x, y, faction: PlayerFaction):
        super().__init__(maze, x, y)
        self.faction = faction
        self.health = 200
        self.power = 3

    def take_turn(self):
        if not self.maze.targets_remaining(self):
            # stop if there are no more targets remaining
            return False

        # 1) move towards targets (if we aren't already in combat distance)
        opponents = self.maze.targets_in_combat_distance(self)
        if not opponents:
            self.move()

        # 2) attack targets (if they are in combat distance)
        self.attack()

        return True

    def move(self):
        # the target cell where we want to go
        target = self.maze.nearest_cell(self)
        if target:
            path = self.maze.shortest_path_bfs(self, target, return_path=True)
            if len(path) > 1:
                # move to target
                self.maze.swap_cells(self, path[1])

    def attack(self):
        opponents = self.maze.targets_in_combat_distance(self)
        if opponents:
            victim = opponents[0]

            # reduce health and remove if dead
            victim.health -= self.power
            if victim.health <= 0:
                self.maze.remove_player(victim)

    def __str__(self):
        return str(self.faction)

    def __repr__(self):
        return "{}({}, {}, {} HP, {} AP)".format(repr(self.faction), self.x, self.y, self.health, self.power)


class Maze:
    """
    Manages the entire game state
    """

    grid: List[List[Cell]]
    players: List[Player]

    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.players = []
        self.dead_elves = 0
        self.dead_goblins = 0
        self.grid = [[Air(self, x, y) for y in range(width)] for x in range(height)]

    def fight(self, stop_on_elf_death=False, debug=False, interactive=False):
        for r in count():

            if debug:
                drawing = self.__str__()
                if interactive:
                    os.system('cls')

                print(f"{Fore.LIGHTMAGENTA_EX}After {r} rounds:{Style.RESET_ALL}")
                print(drawing)

            last_turn = False

            # each player makes a turn (in reading order)
            for player in sorted(self.players, key=lambda p: (p.x, p.y)):

                # still alive?
                if player in self.players:
                    last_turn = player.take_turn()
                    if not last_turn:
                        break

            # if the last turn didn't succeed (no targets left), we are done
            if not last_turn:
                return r

            # possible early-stopping for part 2 brute-force
            if stop_on_elf_death and self.dead_elves > 0:
                return r

    def add_player(self, player: Player):
        self.players.append(player)
        self.grid[player.x][player.y] = player

    def remove_player(self, player: Player):
        self.players.remove(player)
        self.grid[player.x][player.y] = Air(self, player.x, player.y)

        # keep death statistics
        if player.faction == PlayerFaction.Goblin:
            self.dead_goblins += 1
        elif player.faction == PlayerFaction.Elf:
            self.dead_elves += 1

    def swap_cells(self, a: Cell, b: Cell):
        # swapping is useful when moving from a -> b
        self.grid[a.x][a.y], self.grid[b.x][b.y] = self.grid[b.x][b.y], self.grid[a.x][a.y]
        a.x, b.x = b.x, a.x
        a.y, b.y = b.y, a.y

    def targets(self, player: Player) -> List[Player]:
        # players of the other faction
        return [p for p in self.players if p.faction == player.faction.opponent()]

    def targets_in_combat_distance(self, player: Player) -> List[Player]:
        # players of the other faction, that are adjacent to the current player (i.e., neighbouring)
        opponents = [p for p in self.targets(player) if p in self.neighbors(player)]
        return sorted(opponents, key=lambda p: (p.health, p.x, p.y))

    def targets_remaining(self, player: Player):
        # are their any players of the other faction left?
        return len(self.targets(player)) > 0

    def nearest_cell(self, player: Player) -> Optional[Cell]:
        # identify opponent cells
        targets = self.targets(player)
        # adjacent cells that are in range of the opponent
        in_range = [cell for target in targets for cell in self.neighbors_air(target)]
        # reachable cells and their distances
        distances = [self.shortest_path_bfs(player, cell) for cell in in_range]

        try:
            # nearest cells
            min_distance = min(filter(lambda d: d >= 0, distances))
            nearest = [cell for dist, cell in zip(distances, in_range) if dist == min_distance]
        except ValueError:
            # no reachable cells
            return None

        # sort in reading order and chose first
        return sorted(nearest, key=lambda c: (c.x, c.y))[0]

    def shortest_path_bfs(self, start: Cell, goal: Cell, return_path=False):
        queue, distances = [start], {start: 0}
        parents = {}

        def _backtrace_path():
            # resolve all the parents, starting with goal, until we reach start
            path = [goal]
            while path[-1] != start:
                path.append(parents[path[-1]])
            return list(reversed(path))

        # bfs shortest path algorithm
        while queue:
            node = queue.pop(0)
            if node is goal:
                # path found!
                return _backtrace_path() if return_path else distances[node]

            for neighbor in self.neighbors_air(node):
                if neighbor not in distances:
                    queue.append(neighbor)
                    parents[neighbor] = node

                    # distance to this cell is the distance to the parent plus one step
                    distances[neighbor] = distances[node] + 1

        # no path found
        return -1

    def neighbors_air(self, cell: Cell) -> List[Air]:
        # neighbouring cells that are free (Air), within the grid bounds, returned in reading order
        return [c for c in self.neighbors(cell) if isinstance(c, Air)]

    def neighbors(self, cell: Cell) -> List[Cell]:
        # neighbouring cells, within the grid bounds, returned in reading order
        return [self.grid[cell.x + dxy[0]][cell.y + dxy[1]]
                for dxy in [(-1, 0), (0, -1), (0, 1), (1, 0)]
                if (0 <= cell.x + dxy[0] < self.height) and (0 <= cell.y + dxy[1] < self.width)]

    @staticmethod
    def from_file(path) -> 'Maze':
        return Maze.from_string([l.rstrip() for l in open(path).readlines()])

    @staticmethod
    def from_string(lines) -> 'Maze':
        width, height = len(lines[0]), len(lines)
        maze = Maze(width, height)

        for x, line in enumerate(lines):
            for y, value in enumerate(line):
                if value == '#':
                    maze.grid[x][y] = Wall(maze, x, y)
                elif value == 'G':
                    maze.add_player(Player(maze, x, y, PlayerFaction.Goblin))
                elif value == 'E':
                    maze.add_player(Player(maze, x, y, PlayerFaction.Elf))

        return maze

    def __str__(self, highlight=None):
        result = ""
        for x in range(self.height):
            for y in range(self.width):
                cell = self.grid[x][y]

                # cell colors
                color = f'{Fore.LIGHTWHITE_EX}'
                if isinstance(cell, Player):
                    color = f'{Fore.LIGHTGREEN_EX}' if cell.faction == PlayerFaction.Elf else f'{Fore.LIGHTRED_EX}'
                elif isinstance(cell, Wall):
                    color = f'{Back.LIGHTBLACK_EX}{Fore.WHITE}'
                elif isinstance(cell, Air):
                    color = f'{Fore.LIGHTBLUE_EX}'

                # possible highlight
                result += color + str(cell) if not highlight or cell not in highlight else f'{Back.RED}X'
                result += f'{Style.RESET_ALL}'

            # player stats
            result_players = []
            for player in sorted([p for p in self.players if p.x == x], key=lambda p: p.y):
                color = f'{Fore.LIGHTGREEN_EX}' if player.faction == PlayerFaction.Elf else f'{Fore.LIGHTRED_EX}'
                result_players.append(color + f"{player.faction}{Style.RESET_ALL}({player.health})")

            result += "   " + ", ".join(result_players)
            result += '\n'
        return result

    def __repr__(self):
        return "Maze({}, {})".format(self.width, self.height)


def part1(maze, debug=False, interactive=False):
    rounds = maze.fight(debug=debug, interactive=interactive)
    total_health = sum([p.health for p in maze.players])
    return rounds * total_health


def part2(maze, debug=False, interactive=False):
    factory = copy.deepcopy(maze)

    # brute-force different power settings
    print("power = ", end="")
    for power in count(4):
        print(power, end=".. ")

        # grab a fresh maze
        maze = copy.deepcopy(factory)

        # modify the attack power of elves only
        for elf in [p for p in maze.players if p.faction == PlayerFaction.Elf]:
            elf.power = power

        # fight
        rounds = maze.fight(stop_on_elf_death=True, debug=debug, interactive=interactive)

        if maze.dead_elves == 0:
            print()

            # result without any elf looses
            total_health = sum([p.health for p in maze.players])
            return rounds * total_health


if __name__ == "__main__":
    debug = True
    print()
    print(f'{Fore.RED}=============== PART 1 ==============={Style.RESET_ALL}')
    print()

    print(part1(Maze.from_file(r"../assets/day15_demo1.txt"), debug))
    print(part1(Maze.from_file(r"../assets/day15_demo2.txt"), debug))
    print(part1(Maze.from_file(r"../assets/day15_demo3.txt"), debug))
    print(part1(Maze.from_file(r"../assets/day15_demo4.txt"), debug))
    print(part1(Maze.from_file(r"../assets/day15_demo5.txt"), debug))
    print(part1(Maze.from_file(r"../assets/day15_demo6.txt"), debug))
    print(part1(Maze.from_file(r"../assets/day15_demo7.txt"), debug))
    print(part1(Maze.from_file(r"../assets/day15_demo8.txt"), debug))
    print(part1(Maze.from_file(r"../assets/day15_demo9.txt"), debug))

    print("==> " + str(part1(Maze.from_file(r"../assets/day15.txt"), debug, interactive=True)))

    debug = False
    print()
    print(f'{Fore.RED}=============== PART 2 ==============={Style.RESET_ALL}')
    print()

    print(part2(Maze.from_file(r"../assets/day15_demo1.txt"), debug))
    print(part2(Maze.from_file(r"../assets/day15_demo2.txt"), debug))
    print(part2(Maze.from_file(r"../assets/day15_demo3.txt"), debug))
    print(part2(Maze.from_file(r"../assets/day15_demo4.txt"), debug))
    print(part2(Maze.from_file(r"../assets/day15_demo5.txt"), debug))
    print(part2(Maze.from_file(r"../assets/day15_demo6.txt"), debug))
    print(part2(Maze.from_file(r"../assets/day15_demo7.txt"), debug))
    print(part2(Maze.from_file(r"../assets/day15_demo8.txt"), debug))
    print(part2(Maze.from_file(r"../assets/day15_demo9.txt"), debug))

    print("==> " + str(part2(Maze.from_file(r"../assets/day15.txt"))))
