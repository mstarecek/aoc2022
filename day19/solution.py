import math
from collections import deque
from copy import deepcopy
from dataclasses import dataclass, field
from pprint import pprint


@dataclass
class Cost:
    ore: int
    clay: int
    obsidian: int


@dataclass
class Blueprint:
    name: int
    ore: Cost
    clay: Cost
    obsidian: Cost
    geode: Cost
    max_ore_robots: int = field(init=False)
    max_clay_robots: int = field(init=False)
    max_obsidian_robots: int = field(init=False)

    obsidian_clay_to_ore: float = field(init=False)
    geode_clay_to_ore: float = field(init=False)

    def __post_init__(self):
        self.max_ore_robots = max(self.ore.ore, self.clay.ore, self.obsidian.ore, self.geode.ore)
        self.max_clay_robots = self.obsidian.clay
        self.max_obsidian_robots = self.geode.obsidian
        self.obsidian_clay_to_ore = self.obsidian.clay / self.obsidian.ore
        self.geode_clay_to_ore = (self.geode.obsidian * self.obsidian.clay) / (
            self.geode.ore + (self.geode.obsidian * self.obsidian.ore)
        )

    # fmt: off
    @staticmethod
    def from_text(text: str) -> "Blueprint":
        name, rest = text.split(":")
        name = int(name.split(" ")[1])
        costs = rest.split(".")
        for cost in costs:
            match cost.strip().split(" "):
                case ["Each", "ore", "robot", "costs", amount, "ore"]:
                    ore = Cost(ore=int(amount), clay=0, obsidian=0)
                case ["Each", "clay", "robot", "costs", amount, "ore"]:
                    clay = Cost(ore=int(amount), clay=0, obsidian=0)
                case ["Each", "obsidian", "robot", "costs", amount, "ore", "and", amount2, "clay"]:
                    obsidian = Cost(ore=int(amount), clay=int(amount2), obsidian=0)
                case ["Each", "geode", "robot", "costs", amount, "ore", "and", amount3, "obsidian"]:
                    geode = Cost(ore=int(amount), clay=0, obsidian=int(amount3))
                case [""]:
                    continue
                case _:
                    assert False, f"Unparsed line '{cost}'"
        return Blueprint(name=name, ore=ore, clay=clay, obsidian=obsidian, geode=geode)


@dataclass()
class State:
    minute: int = 0
    ore_robots: int = 1
    ore_stock: int = 0
    clay_robots: int = 0
    clay_stock: int = 0
    obsidian_robots: int = 0
    obsidian_stock: int = 0
    geode_robots: int = 0
    geode_stock: int = 0
    building: str = ""
    wait_for: str = ""

    def __repr__(self) -> str:
        return (
            f"r: {self.ore_robots:2}, {self.clay_robots:2}, {self.obsidian_robots:2}, {self.geode_robots:2} "
            f"s: {self.ore_stock:2}, {self.clay_stock:2}, {self.obsidian_stock:2}, {self.geode_stock:2}"
            f"; T{self.minute:2}, b: {self.building} w: {self.wait_for}"
        )

    def can_build(self, name: str, blueprint: Blueprint) -> bool:
        if self.wait_for and self.wait_for != name:
            return False
        match name:
            case "ore":
                return self.ore_stock >= blueprint.ore.ore and self.ore_robots < blueprint.max_ore_robots
            case "clay":
                return self.ore_stock >= blueprint.clay.ore and self.clay_stock < blueprint.max_clay_robots
            case "obsidian":
                return (
                    self.ore_stock >= blueprint.obsidian.ore
                    and self.clay_stock >= blueprint.obsidian.clay
                    and self.obsidian_robots < blueprint.max_obsidian_robots
                )
            case "geode":
                return self.ore_stock >= blueprint.geode.ore and self.obsidian_stock >= blueprint.geode.obsidian

    def turns_to_build(self, name: str, blueprint: Blueprint) -> int | None:
        match name:
            case "ore":
                if self.ore_stock >= blueprint.ore.ore:
                    return 0
                return math.ceil((blueprint.ore.ore - self.ore_stock) / self.ore_robots)
            case "clay":
                if self.ore_stock >= blueprint.clay.ore:
                    return 0
                return math.ceil((blueprint.clay.ore - self.ore_stock) / self.ore_robots)
            case "obsidian":
                if self.clay_robots == 0:
                    return None
                if self.ore_stock >= blueprint.obsidian.ore and self.clay_stock >= blueprint.obsidian.clay:
                    return 0
                return max(
                    math.ceil((blueprint.obsidian.ore - self.ore_stock) / self.ore_robots),
                    math.ceil((blueprint.obsidian.clay - self.clay_stock) / self.clay_robots),
                )
            case "geode":
                if self.obsidian_robots == 0:
                    return None
                if self.ore_stock >= blueprint.geode.ore and self.obsidian_stock >= blueprint.geode.obsidian:
                    return 0
                return max(
                    math.ceil((blueprint.geode.ore - self.ore_stock) / self.ore_robots),
                    math.ceil((blueprint.geode.obsidian - self.obsidian_stock) / self.obsidian_robots),
                )

    def build(self, name: str, blueprint: Blueprint) -> bool:
        if not self.can_build(name=name, blueprint=blueprint):
            return False
        match name:
            case "ore":
                self.ore_stock -= blueprint.ore.ore
            case "clay":
                self.ore_stock -= blueprint.clay.ore
            case "obsidian":
                self.ore_stock -= blueprint.obsidian.ore
                self.clay_stock -= blueprint.obsidian.clay
            case "geode":
                self.ore_stock -= blueprint.geode.ore
                self.obsidian_stock -= blueprint.geode.obsidian
        self.building = name
        return True

    def copy_build(self, name: str, blueprint: Blueprint) -> "State":
        copy = deepcopy(self)
        copy.build(name=name, blueprint=blueprint)
        return copy

    def copy_wait(self, name: str) -> "State":
        copy = deepcopy(self)
        copy.wait_for = name
        return copy

    def tick(self) -> None:
        self.minute += 1
        self.ore_stock += self.ore_robots
        self.clay_stock += self.clay_robots
        self.obsidian_stock += self.obsidian_robots
        self.geode_stock += self.geode_robots
        match self.building:
            case "":
                pass
            case "ore":
                self.ore_robots += 1
            case "clay":
                self.clay_robots += 1
            case "obsidian":
                self.obsidian_robots += 1
            case "geode":
                self.geode_robots += 1
        if self.wait_for == self.building:
            self.wait_for = ""
        self.building = ""


def get_yield(blueprint: Blueprint, max_time: int) -> int:
    max_obsidian = 0
    seen = set()
    states = deque([State()])
    robots = ["geode", "obsidian", "clay", "ore"]
    while states:
        current = states.popleft()
        current.tick()
        max_obsidian = max(max_obsidian, current.obsidian_stock)

        if current.minute >= max_time:
            continue

        this_fork: deque[State] = []
        for robot in robots:
            if current.turns_to_build(robot, blueprint):
                this_fork.append(current.copy_wait(robot))
            if current.can_build(robot, blueprint):
                this_fork.append(current.copy_build(robot, blueprint))
        if not this_fork:
            states.append(current)
        else:
            states.extend(this_fork)
    return max_obsidian


def part1(blueprints: list[Blueprint]):
    results: dict[int, int] = {}
    for bp in blueprints:
        results[bp.name] = get_yield(blueprint=bp, max_time=24)
    pprint(results)
    return sum(k * v for k, v in results.items())


def load_blueprints(input_file) -> list[Blueprint]:
    with open(input_file) as f:
        lines = f.read().splitlines()
    return [Blueprint.from_text(line) for line in lines]


if __name__ == "__main__":
    blueprints = load_blueprints("test_input.txt")
    # blueprints = load_blueprints("input.txt")
    # pprint(blueprints)
    print(f"Part 1: {part1(blueprints=blueprints)}")
