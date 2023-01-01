import time
from dataclasses import dataclass


@dataclass(eq=True, frozen=True)
class Point:
    x: int
    y: int


def load_data(input_file: str) -> list[tuple[Point, Point]]:
    with open(input_file) as f:
        lines = f.read().splitlines(keepends=False)

    result = []
    for line in lines:
        segments = line.split(" -> ")
        for i in range(len(segments) - 1):
            start_x, start_y = segments[i].split(",")
            end_x, end_y = segments[i + 1].split(",")
            result.append(
                (
                    Point(x=int(start_x), y=int(start_y)),
                    Point(x=int(end_x), y=int(end_y)),
                )
            )
    return result


def get_limits(
    grid: dict[Point, int], widen_edges: bool = False
) -> tuple[Point, Point]:
    top_y, bottom_y, left_x, right_x = 0, 0, 0, 0
    ys = [p.y for p in grid]
    xs = [p.x for p in grid]
    bottom_y = max(ys) + 1
    left_x = min(xs) - (bottom_y if widen_edges else 1)
    right_x = max(xs) + (bottom_y if widen_edges else 1)
    return Point(left_x, top_y), Point(right_x, bottom_y)


def fill_grid(grid: dict[Point, int]) -> None:
    top_left, bottom_right = get_limits(grid=grid, widen_edges=True)
    for y in range(top_left.y, bottom_right.y + 1):
        for x in range(top_left.x, bottom_right.x + 1):
            this_point = Point(x=x, y=y)
            if this_point not in grid:
                grid[this_point] = 0


def get_grid(data: list[tuple[Point, Point]]) -> dict[Point, int]:
    grid = {}
    for start, end in data:
        for x in range(min(start.x, end.x), max(start.x, end.x) + 1):
            for y in range(min(start.y, end.y), max(start.y, end.y) + 1):
                grid[Point(x=x, y=y)] = 1
    fill_grid(grid=grid)
    return grid


def draw_grid(grid: dict[Point, int]) -> None:
    top_left, bottom_right = get_limits(grid=grid, widen_edges=False)
    pixels = {0: ".", 1: "#", 2: "o"}
    print()
    for y in range(top_left.y, bottom_right.y + 1):
        for x in range(top_left.x, bottom_right.x + 1):
            print(pixels[grid.get(Point(x=x, y=y), 0)], end="")
        print()


def find_destination(
    part: int,
    grid: dict[Point, int],
    current: Point,
    top_left: Point,
    bottom_right: Point,
) -> Point | None:
    # down
    next_point = Point(x=current.x, y=current.y + 1)

    if part == 1:
        if next_point not in grid:
            raise ValueError("This is outside the puzzle")
    else:
        if current == Point(500, 0) and grid[current] == 2:
            raise ValueError("Drop point is blocked")
        if next_point.y == bottom_right.y:
            grid[current] = 2
            return
    if grid[next_point] == 0:
        return find_destination(
            part=part,
            grid=grid,
            current=next_point,
            top_left=top_left,
            bottom_right=bottom_right,
        )
    # down left
    next_point = Point(x=current.x - 1, y=current.y + 1)
    if grid[next_point] == 0:
        return find_destination(
            part=part,
            grid=grid,
            current=next_point,
            top_left=top_left,
            bottom_right=bottom_right,
        )
    # down right
    next_point = Point(x=current.x + 1, y=current.y + 1)
    if grid[next_point] == 0:
        return find_destination(
            part=part,
            grid=grid,
            current=next_point,
            top_left=top_left,
            bottom_right=bottom_right,
        )
    grid[current] = 2


def find_destination_2(
    grid: dict[Point, int], current: Point, top_left: Point, bottom_right: Point
) -> Point | None:
    if current == Point(500, 0) and grid[current] == 2:
        raise ValueError("This is it")
    # down
    next_point = Point(x=current.x, y=current.y + 1)
    if next_point.y == bottom_right.y:
        grid[current] = 2
        return
    if grid[next_point] == 0:
        return find_destination_2(
            grid=grid, current=next_point, top_left=top_left, bottom_right=bottom_right
        )
    # down left
    next_point = Point(x=current.x - 1, y=current.y + 1)
    if grid[next_point] == 0:
        return find_destination_2(
            grid=grid, current=next_point, top_left=top_left, bottom_right=bottom_right
        )
    # down right
    next_point = Point(x=current.x + 1, y=current.y + 1)
    if grid[next_point] == 0:
        return find_destination_2(
            grid=grid, current=next_point, top_left=top_left, bottom_right=bottom_right
        )
    grid[current] = 2


def do_stuff(part: int, grid: dict[Point, int], drop: Point) -> int:
    top_left, bottom_right = get_limits(grid=grid, widen_edges=False)
    try:
        i = 0
        while True:
            find_destination(
                part=part,
                grid=grid,
                current=drop,
                top_left=top_left,
                bottom_right=bottom_right,
            )
            # draw_grid(grid=grid, top_left=top_left, bottom_right=bottom_right)
            i += 1

    except ValueError as e:
        return i


if __name__ == "__main__":
    # data = load_data("test_input.txt")
    data = load_data("input.txt")
    start = time.perf_counter()
    grid = get_grid(data=data)
    print(f"Part 1: {do_stuff(part=1, grid=grid, drop=Point(500,0))}")

    grid = get_grid(data=data)
    print(f"Part 2: {do_stuff(part=2, grid=grid, drop=Point(500,0))}")
    print(f"Done in {time.perf_counter()-start:.3f} sec")
