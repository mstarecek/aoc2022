import string
from dataclasses import dataclass


@dataclass(eq=True, frozen=True)
class Point:
    x: int
    y: int

    def get_neighbors(self) -> tuple["Point", "Point", "Point", "Point"]:
        return (
            Point(x=self.x, y=self.y - 1),
            Point(x=self.x, y=self.y + 1),
            Point(x=self.x - 1, y=self.y),
            Point(x=self.x + 1, y=self.y),
        )


def load_data(input_file: str) -> str:
    with open(input_file) as f:
        return f.read().splitlines(keepends=False)


def get_grid(
    data: list[str],
) -> tuple[Point, Point, dict[Point, int]]:
    grid = {}
    for y, line in enumerate(data):
        for x, hight in enumerate(line):
            if hight == "S":
                start = Point(x, y)
                hight = "a"
            if hight == "E":
                end = Point(x, y)
                hight = "z"
            grid[Point(x, y)] = string.ascii_lowercase.index(hight)
    return start, end, grid


def part1(start: Point, end: Point, grid: dict[Point, int]) -> int:
    seen = [end]
    previous_tails = [end]
    distance = 1
    while True:
        candidates = []
        for tail in previous_tails:
            for neighbor in tail.get_neighbors():
                if neighbor not in grid:
                    continue
                if neighbor in seen:
                    continue
                if grid[tail] - grid[neighbor] > 1:
                    continue
                if neighbor == start:
                    return distance
                seen.append(neighbor)
                candidates.append(neighbor)
        distance += 1
        previous_tails = candidates
        # print(candidates, distance)


def part2(start: Point, end: Point, grid: dict[Point, int]) -> int:
    seen = [end]
    previous_tails = [end]
    distance = 1
    while True:
        candidates = []
        for tail in previous_tails:
            for neighbor in tail.get_neighbors():
                if neighbor not in grid:
                    continue
                if neighbor in seen:
                    continue
                if grid[tail] - grid[neighbor] > 1:
                    continue
                if grid[neighbor] == 0:
                    return distance
                seen.append(neighbor)
                candidates.append(neighbor)
        distance += 1
        previous_tails = candidates
        # print(candidates, distance)


if __name__ == "__main__":
    data = load_data("input.txt")
    # data = load_data("test_input.txt")
    start, end, grid = get_grid(data)

    print(f"Path 1: {part1(start, end, grid)}")
    print(f"Path 2: {part2(start, end, grid)}")
