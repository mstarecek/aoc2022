from collections import Counter
from typing import NamedTuple

OFFSETS = [
    [(-1, -1), (0, -1), (1, -1)],
    [(-1, 1), (0, 1), (1, 1)],
    [(-1, -1), (-1, 0), (-1, 1)],
    [(1, -1), (1, 0), (1, 1)],
]

NEIGHBORS = [(0, -1), (0, 1), (-1, 0), (1, 0)]
DIR_NAMES = {0: "N", 1: "S", 2: "W", 3: "E"}


class Position(NamedTuple):
    x: int
    y: int

    def __repr__(self) -> str:
        return f"({self.x}, {self.y})"


Grid = dict[Position, Position]


def load_data(input_file: str) -> Grid:
    with open(input_file) as f:
        lines = f.read().splitlines()
    grid = Grid()
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char == "#":
                grid[Position(x, y)] = Position(x, y)
    return grid


def get_corners(grid: Grid) -> tuple[Position, Position]:
    x_min, x_max, y_min, y_max = 100, -100, 100, -100
    for x, y in grid:
        x_min = min(x_min, x)
        x_max = max(x_max, x)
        y_min = min(y_min, y)
        y_max = max(y_max, y)
    return Position(x_min, y_min), Position(x_max, y_max)


def get_empty_count(grid: Grid) -> int:
    top_left, bottom_right = get_corners(grid=grid)
    print(f"{top_left=} {bottom_right=}")
    area = (bottom_right.x - top_left.x + 1) * (bottom_right.y - top_left.y + 1)
    return area - len(grid)


def draw(grid: Grid) -> None:
    top_left, bottom_right = get_corners(grid=grid)
    for y in range(top_left.y - 1, bottom_right.y + 2):
        for x in range(top_left.x - 1, bottom_right.x + 2):
            print("#" if (x, y) in grid else ".", end="")
        print()


def is_alone(x: int, y: int, grid: Grid) -> bool:
    for i in range(len(OFFSETS)):
        for dx, dy in OFFSETS[i]:
            if (x + dx, y + dy) in grid:
                return False
    return True


def prepare(grid: Grid, round: int) -> None:
    for (x, y) in grid:
        if is_alone(x, y, grid=grid):
            grid[(x, y)] = (x, y)
            continue
        for i in range(len(OFFSETS)):
            direction = (round + i) % len(OFFSETS)
            for dx, dy in OFFSETS[direction]:
                if (x + dx, y + dy) in grid:
                    break
            else:
                dx, dy = OFFSETS[direction][1]
                grid[(x, y)] = Position(x + dx, y + dy)
                break
        else:
            grid[(x, y)] = Position(x, y)


def block(grid: Grid) -> None:
    counter = Counter(grid.values())
    blocked = [item for item, count in counter.items() if count > 1]
    for elf, target in grid.items():
        if target in blocked:
            grid[elf] = elf


def move(grid: Grid) -> None:
    for elf, target in grid.copy().items():
        if elf == target:
            continue
        del grid[elf]
        grid[target] = target


def part1(grid: Grid, rounds: int = 10) -> int:
    # draw(grid=grid)
    for i in range(rounds):
        # print(f"Round #{i+1}")
        prepare(grid=grid, round=i)
        block(grid=grid)
        move(grid=grid)
        # draw(grid=grid)
    return get_empty_count(grid=grid)


def get_movers(grid: Grid) -> int:
    return sum(elf != target for elf, target in grid.items())


def part2(grid: Grid) -> int:
    i = 0
    while True:
        # print(f"Round #{i+1}")
        prepare(grid=grid, round=i)
        if get_movers(grid=grid) == 0:
            return i + 1
        block(grid=grid)
        move(grid=grid)
        i += 1


if __name__ == "__main__":
    # grid = load_data("mini_input.txt")
    # grid = load_data("test_input.txt")
    grid = load_data("input.txt")
    print(f"Part 1: {part1(grid=grid)}")

    # grid = load_data("test_input.txt")
    grid = load_data("input.txt")
    print(f"Part 2: {part2(grid=grid)}")
