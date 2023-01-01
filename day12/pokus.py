import string
import sys
from dataclasses import dataclass
from typing import Callable, Iterator

# big yikes
sys.setrecursionlimit(10_000)


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


class Node:
    def __init__(self, coordinates: Point, hight: int, parent: "Node") -> None:
        self.coordinates = coordinates
        self.hight = hight
        self.children: list["Node"] = []
        self.parent: "Node" = parent
        self.length = parent.length + 1 if parent else 0
        self.seen = parent.seen if parent else []
        self.seen.append(coordinates)

    def __repr__(self) -> str:
        return f"{repr(self.coordinates)}: {self.hight} ({string.ascii_lowercase[self.hight]})"

    def get_lengths(self, predicate: Callable[["Node"], bool]) -> Iterator[int]:
        if predicate(self):
            yield self.length
        for child in self.children:
            yield from child.get_lengths(predicate=predicate)

    def set_children(self, grid: dict[Point, int]) -> None:
        for dir in self.coordinates.get_neighbors():
            if dir not in grid:
                continue
            if dir in self.seen:
                continue
            if self.hight - grid[dir] > 1:
                continue
            self.children.append(Node(dir, grid[dir], self))

    def fill(self, grid: dict[Point, int]) -> Point:
        self.set_children(grid=grid)
        for child in self.children:
            child.fill(grid=grid)

    def print(self):
        current = self
        while current.parent:
            print(current)
            current = current.parent


path = Node(coordinates=None, hight=None, parent=None)


def part1(start, end, grid) -> int:
    path.coordinates = end
    path.hight = grid[end]
    path.fill(grid=grid)
    lengths = list(path.get_lengths(predicate=lambda x: x.coordinates == start))
    print(lengths)
    return min(lengths)


if __name__ == "__main__":

    # data = load_data("test_input.txt")
    data = load_data("input.txt")
    start, end, grid = get_grid(data)
    print(f"Part 1: {part1(start=start, end=end, grid=grid)}")
