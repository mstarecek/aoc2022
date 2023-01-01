import functools
import time
from collections import deque
from dataclasses import dataclass
from typing import Iterator, NamedTuple


# @dataclass(frozen=True)
# class Face:
class Face(NamedTuple):
    x_start: int
    y_start: int
    z_start: int
    x_end: int
    y_end: int
    z_end: int

    def __repr__(self) -> str:
        return (
            f"({self.x_start}, {self.y_start}, {self.z_start}) -> "
            f"({self.x_end}, {self.y_end}, {self.z_end})"
        )


# @dataclass(frozen=True)
# class Cube:
class Cube(NamedTuple):
    x: int
    y: int
    z: int

    def get_neighbors(self) -> list["Cube"]:
        return [
            Cube(self.x + dx, self.y + dy, self.z + dz)
            for dx, dy, dz in [
                (1, 0, 0),
                (-1, 0, 0),
                (0, 1, 0),
                (0, -1, 0),
                (0, 0, 1),
                (0, 0, -1),
            ]
        ]

    def get_faces(self) -> list[Face]:
        return [
            Face(
                self.x + start_dx,
                self.y + start_dy,
                self.z + start_dz,
                self.x + end_dx,
                self.y + end_dy,
                self.z + end_dz,
            )
            for start_dx, start_dy, start_dz, end_dx, end_dy, end_dz in [
                (0, 0, 0, 1, 1, 0),  # bottom
                (0, 0, 1, 1, 1, 1),  # top
                (0, 0, 0, 1, 0, 1),  # front
                (0, 1, 0, 1, 1, 1),  # back
                (0, 0, 0, 0, 1, 1),  # left
                (1, 0, 0, 1, 1, 1),  # right
            ]
        ]

    def is_in_bounds(self, min: "Cube", max: "Cube"):
        return (
            min.x <= self.x <= max.x
            and min.y <= self.y <= max.y
            and min.z <= self.z <= max.z
        )


def load_cubes(input_file: str) -> list[Cube]:
    with open(input_file) as f:
        lines = f.read().splitlines(keepends=False)
    result = []
    for line in lines:
        parts = line.split(",")
        result.append(Cube(x=int(parts[0]), y=int(parts[1]), z=int(parts[2])))
    return result


def part1(cubes: list[Cube]) -> int:
    faces = []
    for cube in cubes:
        faces.extend(cube.get_faces())
    faces_set = set(faces)
    diff = len(faces) - len(faces_set)
    return len(faces) - 2 * diff


def get_exterior(start: Cube, end: Cube, cubes: list[Cube]) -> set[Cube]:
    stack = deque([start])
    visited = set()

    visited.add(start)

    while stack:
        current = stack.pop()

        for neighbor in current.get_neighbors():
            if not neighbor.is_in_bounds(min=start, max=end):
                continue
            if neighbor in visited:
                continue
            if neighbor in cubes:
                continue
            stack.append(neighbor)
            visited.add(neighbor)
    return visited


def find_boundaries(cubes: list[Cube]) -> tuple[Cube, Cube]:
    max_x, max_y, max_z = -1, -1, -1
    min_x, min_y, min_z = 100, 100, 100

    for cube in cubes:
        max_x = max(max_x, cube.x)
        max_y = max(max_y, cube.y)
        max_z = max(max_z, cube.z)

        min_x = min(min_x, cube.x)
        min_y = min(min_y, cube.y)
        min_z = min(min_z, cube.z)

    return Cube(min_x - 1, min_y - 1, min_z - 1), Cube(max_x + 1, max_y + 1, max_z + 1)


def part2(cubes: list[Cube]) -> int:
    surface = 0
    min_bound, max_bound = find_boundaries(cubes=cubes)
    exterior = get_exterior(start=min_bound, end=max_bound, cubes=cubes)
    # with open("surface_steam.txt", "w") as f:
    for cube in cubes:
        for neighbor in cube.get_neighbors():
            if neighbor in cubes:
                continue
            if neighbor in exterior:
                surface += 1
                # f.write(f"{cube} - {neighbor}\n")
    return surface


if __name__ == "__main__":
    # cubes = [Cube(1, 1, 1), Cube(1, 0, 1)]
    # cubes = load_cubes("test_input.txt")
    cubes = load_cubes("input.txt")
    start = time.perf_counter()
    print(f"Part 1: {part1(cubes=cubes)}")
    print(f"Done in: {time.perf_counter()-start:.3f}")
    start = time.perf_counter()
    print(f"Part 2: {part2(cubes=cubes)}")
    print(f"Done in: {time.perf_counter()-start:.3f}")
