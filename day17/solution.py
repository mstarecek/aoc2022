import itertools
from dataclasses import dataclass
from pprint import pprint
from typing import Iterator, NamedTuple


class Point(NamedTuple):
    x: int
    y: int


@dataclass
class Rock:
    points: list[tuple[int, int]]

    def move(self, dx: int, dy: int, chamber: list[Point]) -> bool:
        target_points = [Point(x + dx, y + dy) for x, y in self.points]
        for point in target_points:
            if point.x < 0 or point.x > 6:
                return False
            if point in chamber:
                return False
        self.points = target_points
        return True


@dataclass
class RockFactory:
    height: int
    width: int
    layout: list[tuple[int, int]]

    def create(self, x: int, y: int) -> Rock:
        return Rock(points=[Point(x + dx, y + dy) for dx, dy in self.layout])

    @staticmethod
    def parse(data: str) -> "RockFactory":
        lines = data.splitlines(keepends=False)
        layout = []
        for column, line in enumerate(reversed(lines)):
            for row, char in enumerate(line):
                if char == "#":
                    layout.append((row, column))
        return RockFactory(height=len(lines), width=len(line), layout=layout)


def load_shapes() -> list[RockFactory]:
    with open("shapes.txt") as f:
        data = f.read()
    shapes = data.split("\n\n")
    return [RockFactory.parse(portion) for portion in shapes]


def load_data(input_file: str) -> list[str]:
    with open(input_file) as f:
        return list(f.readline().strip())


def draw_chamber(chamber: list[Point], hight: int):
    for y in range(hight + 1, -1, -1):
        for x in range(7):
            print("#" if Point(x=x, y=y) in chamber else ".", end="")
        print()
    print("\n\n")


def fall(
    chamber: list[Point], rock_factory: RockFactory, jet_gen: Iterator[str], hight: int
) -> int:
    rock = rock_factory.create(x=2, y=hight + 4)
    new_hight = hight
    while True:
        dx = 1 if next(jet_gen) == ">" else -1
        rock.move(dx=dx, dy=0, chamber=chamber)
        if rock.move(dx=0, dy=-1, chamber=chamber) is False:
            # contact
            for point in rock.points:
                chamber.append(point)
                new_hight = max(new_hight, point.y)
            return new_hight


def part1(shapes: list[RockFactory], jets: str) -> int:
    chamber = [Point(x=x, y=0) for x in range(7)]
    jet_gen = itertools.cycle(jets)
    hight = 0
    for rock_id, shape in enumerate(itertools.cycle(shapes), start=1):
        hight = fall(chamber=chamber, rock_factory=shape, jet_gen=jet_gen, hight=hight)
        # draw_chamber(chamber=chamber, hight=hight)
        if rock_id == 2022:
            return hight


if __name__ == "__main__":
    shapes = load_shapes()
    pprint(shapes)
    jets = load_data("input.txt")
    print(f"Part1: {part1(shapes=shapes, jets=jets)}")
