import re
from dataclasses import dataclass
from itertools import zip_longest
from typing import Callable

Instructions = list[int | str]

DIRECTIONS = {0: "Right", 1: "Down", 2: "Left", 3: "Up"}

# directions: 0 = >, 1 = v, 2 = <, 3 = ^
TEST_TRANSITIONS = {
    1: {
        # (dest, x, y, direction)
        0: lambda x, y: (6, 3, (3 - y), 2),
        2: lambda x, y: (3, y, 0, 1),
        3: lambda x, y: (2, (3 - x), 0, 1),
    },
    2: {
        1: lambda x, y: (5, (3 - x), 3, 3),
        2: lambda x, y: (6, (3 - x), 3, 3),
        3: lambda x, y: (1, (3 - x), 1, 1),
    },
    3: {
        1: lambda x, y: (5, 0, (3 - y), 0),
        3: lambda x, y: (1, 0, x, 0),
    },
    4: {
        0: lambda x, y: (6, (3 - y), 0, 1),
    },
    5: {
        1: lambda x, y: (2, (3 - x), 3, 3),
        2: lambda x, y: (3, (3 - y), 3, 3),
    },
    6: {
        0: lambda x, y: (1, 3, (3 - y), 2),
        1: lambda x, y: (2, 0, x, 0),
        3: lambda x, y: (4, 3, (3 - y), 2),
    },
}
REAL_TRANSITIONS = {
    1: {
        # (dest, x, y, direction)
        2: lambda x, y: (4, 0, (49 - y), 0),
        3: lambda x, y: (6, 0, x, 0),
    },
    2: {
        0: lambda x, y: (5, 49, (49 - y), 2),
        1: lambda x, y: (3, 49, x, 2),
        3: lambda x, y: (6, x, 49, 3),
    },
    3: {
        0: lambda x, y: (2, y, 49, 3),
        2: lambda x, y: (4, y, 0, 1),
    },
    4: {
        2: lambda x, y: (1, 0, (49 - y), 0),
        3: lambda x, y: (3, 0, x, 0),
    },
    5: {
        0: lambda x, y: (2, 49, (49 - y), 2),
        1: lambda x, y: (6, 49, x, 2),
    },
    6: {
        0: lambda x, y: (5, y, 49, 3),
        1: lambda x, y: (2, x, 0, 1),
        2: lambda x, y: (1, y, 0, 1),
    },
}

TEST_STARTS = {1: (8, 0), 2: (0, 4), 3: (4, 4), 4: (8, 4), 5: (8, 8), 6: (12, 8)}
REAL_STARTS = {
    1: (50, 0),
    2: (100, 0),
    3: (50, 50),
    4: (0, 100),
    5: (50, 100),
    6: (0, 150),
}


@dataclass
class Grid:
    max_x: int
    max_y: int
    data: dict[tuple[int, int], str]
    sector_size: int
    sector_starts: dict[int, tuple[int, int]]
    transitions: dict[dict[int, Callable]]

    def get_sector(self, x: int, y: int) -> int:
        for i, (start_x, start_y) in self.sector_starts.items():
            if (
                start_x <= x < start_x + self.sector_size
                and start_y <= y < start_y + self.sector_size
            ):
                return i
        raise RuntimeError(f"Point ({x}, {y}) is not in any sector")

    def transform_coordinates(
        self, x: int, y: int, direction: int
    ) -> tuple[int, int, int]:
        sector = self.get_sector(x=x, y=y)
        tr = self.transitions[sector][direction]
        new_sector, off_x, off_y, new_direction = tr(
            (x % self.sector_size), (y % self.sector_size)
        )
        new_x = self.sector_starts[new_sector][0] + off_x
        new_y = self.sector_starts[new_sector][1] + off_y
        return new_x, new_y, new_direction

    def get_start(self) -> tuple[int, int]:
        for x in range(100):
            if self.data[(x, 0)] == ".":
                return x, 0

    def is_wall(self, x: int, y: int) -> bool:
        return self.data[(x, y)] == "#"

    def is_open(self, x: int, y: int) -> bool:
        return self.data[(x, y)] == "."

    @staticmethod
    def from_data(data: str) -> "Grid":
        grid = {}
        max_x, max_y = 0, 0
        for y, line in enumerate(data.splitlines()):
            for x, char in enumerate(line):
                max_x = max(max_x, x)
                grid[(x, y)] = char
        max_y = y
        for x in range(max_x + 1):
            for y in range(max_y + 1):
                if (x, y) not in grid:
                    grid[(x, y)] = " "
        return Grid(
            max_x=max_x,
            max_y=max_y,
            data=grid,
            sector_size=4 if TEST else 50,
            sector_starts=TEST_STARTS if TEST else REAL_STARTS,
            transitions=TEST_TRANSITIONS if TEST else REAL_TRANSITIONS,
        )


@dataclass
class Player:
    x: int
    y: int
    # 0 = >, 1 = v, 2 = <, 3 = ^
    direction: int = 0

    def __repr__(self) -> str:
        return (
            f"x={self.x}, y={self.y}, d={DIRECTIONS[self.direction]} ({self.direction})"
        )

    def result(self) -> int:
        return (self.y + 1) * 1000 + (self.x + 1) * 4 + self.direction

    def turn(self, rotation: str) -> None:
        self.direction += 1 if rotation == "R" else -1
        self.direction %= 4

    def move(self, grid: Grid, part: int = 1) -> None:
        diffs = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        dx, dy = diffs[self.direction]
        new_x, new_y = self.x + dx, self.y + dy
        direction = self.direction
        while True:
            if (new_x, new_y) not in grid.data:
                if part == 1:
                    if dx == 1:
                        new_x = 0
                    if dx == -1:
                        new_x = grid.max_x
                    if dy == 1:
                        new_y = 0
                    if dy == -1:
                        new_y = grid.max_y
                if part == 2:
                    new_x, new_y, direction = grid.transform_coordinates(
                        x=self.x, y=self.y, direction=self.direction
                    )
            if grid.is_wall(x=new_x, y=new_y):
                return
            if grid.is_open(x=new_x, y=new_y):
                self.x = new_x
                self.y = new_y
                self.direction = direction
                return
            if part == 1:
                new_x += dx
                new_y += dy
            if part == 2:
                new_x, new_y, direction = grid.transform_coordinates(
                    x=self.x, y=self.y, direction=self.direction
                )

    def step(self, instruction: str | int, grid: Grid, part: int):
        if isinstance(instruction, str):
            return self.turn(rotation=instruction)
        for _ in range(instruction):
            self.move(grid=grid, part=part)


def load_data(input_file: str) -> tuple[Grid, Instructions, Player]:
    with open(input_file) as f:
        data = f.read()
    maze, steps = data.split("\n\n")
    grid = Grid.from_data(data=maze)

    instructions = []
    moves = re.findall(r"\d+", steps)
    turns = re.findall(r"[RL]", steps)
    for move, turn in zip_longest(moves, turns):
        if move:
            instructions.append(int(move))
        if turn:
            instructions.append(turn)

    start_x, start_y = grid.get_start()
    player = Player(x=start_x, y=start_y)

    return grid, instructions, player


def part1(grid: Grid, instructions: Instructions, player: Player) -> int:
    for s, instruction in enumerate(instructions):
        # print(f"Step #{s}: {instruction}")
        player.step(instruction=instruction, grid=grid, part=1)
    print(player)
    return player.result()


def part2(grid: Grid, instructions: Instructions, player: Player) -> int:
    for s, instruction in enumerate(instructions):
        # print(f"Step #{s}: {instruction}")
        player.step(instruction=instruction, grid=grid, part=2)
    return player.result()


if __name__ == "__main__":
    TEST = False
    grid, instructions, player = load_data("test_input.txt" if TEST else "input.txt")
    print(f"Part 1: {part1(grid, instructions, player)}")

    grid, instructions, player = load_data("test_input.txt" if TEST else "input.txt")
    print(f"Part 2: {part2(grid, instructions, player)}")
