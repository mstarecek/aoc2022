import functools
import time

import colorama

colorama.init()

Point = tuple[int, int]
Grid = dict[Point, int]


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
                    (int(start_x), int(start_y)),
                    (int(end_x), int(end_y)),
                )
            )
    return result


def get_limits(grid: Grid, widen_edges: bool = False) -> tuple[Point, Point]:
    top_y, bottom_y, left_x, right_x = 0, 0, 0, 0
    ys = [p[1] for p in grid]
    xs = [p[0] for p in grid]
    bottom_y = max(ys) + 1
    left_x = min(xs) - (bottom_y if widen_edges else 1)
    right_x = max(xs) + (bottom_y if widen_edges else 1)
    return (left_x, top_y), (right_x, bottom_y)


def fill_grid(grid: Grid) -> None:
    top_left, bottom_right = get_limits(grid=grid, widen_edges=True)
    for y in range(top_left[1], bottom_right[1] + 1):
        for x in range(top_left[0], bottom_right[0] + 1):
            this_point = (x, y)
            if this_point not in grid:
                grid[this_point] = 0
    grid[(500, 0)] = 4


def clear_path(grid: Grid) -> None:
    top_left, bottom_right = get_limits(grid=grid, widen_edges=False)
    for y in range(top_left[1] + 1, bottom_right[1]):
        for x in range(top_left[0] + 1, bottom_right[0]):
            this_point = (x, y)
            if grid[this_point] == 3:
                grid[this_point] = 0


def get_grid(data: list[tuple[Point, Point]]) -> Grid:
    grid = {}
    for start, end in data:
        for x in range(min(start[0], end[0]), max(start[0], end[0]) + 1):
            for y in range(min(start[1], end[1]), max(start[1], end[1]) + 1):
                grid[(x, y)] = 1
    fill_grid(grid=grid)
    return grid


def draw_grid(grid: Grid, repaint: bool = True) -> None:
    top_left, bottom_right = get_limits(grid=grid, widen_edges=False)
    if repaint:
        print("\033[A" * (bottom_right[1] + 3))
    pixels = {0: " ", 1: "#", 2: "o", 3: "v", 4: "+"}
    colors = {
        0: colorama.Fore.WHITE,
        1: colorama.Fore.BLUE,
        2: colorama.Fore.LIGHTYELLOW_EX,
        3: colorama.Fore.RED,
        4: colorama.Fore.GREEN,
    }
    print()
    for y in range(top_left[1], bottom_right[1] + 1):
        for x in range(top_left[0], bottom_right[0] + 1):
            value = grid.get((x, y), 0)
            print(colors[value] + pixels[value], end="")
        print()


def start_animation(grid: Grid, point: Point) -> None:
    if point != (500, 0):
        grid[point] = 3
    draw_grid(grid=grid)
    time.sleep(0.02)


def stop_animation(grid: Grid) -> None:
    draw_grid(grid=grid)
    time.sleep(0.2)
    clear_path(grid=grid)


def find_destination(
    part: int,
    grid: Grid,
    current: Point,
    top_left: Point,
    bottom_right: Point,
    animate: bool,
) -> Point | None:
    if animate:
        start_animation(grid=grid, point=current)

    # down
    next_point = (current[0], current[1] + 1)

    if part == 1:
        if next_point not in grid:
            raise ValueError("This is outside the puzzle")
    else:
        if current == (500, 0) and grid[current] in [2]:
            raise ValueError("Drop point is blocked")
        if next_point[1] == bottom_right[1]:
            grid[current] = 2
            if animate:
                stop_animation(grid=grid)
            return
    if grid[next_point] == 0:
        return find_destination(
            current=next_point,
            part=part,
            grid=grid,
            top_left=top_left,
            bottom_right=bottom_right,
            animate=animate,
        )
    # down left
    next_point = (current[0] - 1, current[1] + 1)
    if grid[next_point] == 0:
        return find_destination(
            current=next_point,
            part=part,
            grid=grid,
            top_left=top_left,
            bottom_right=bottom_right,
            animate=animate,
        )
    # down right
    next_point = (current[0] + 1, current[1] + 1)
    if grid[next_point] == 0:
        return find_destination(
            current=next_point,
            part=part,
            grid=grid,
            top_left=top_left,
            bottom_right=bottom_right,
            animate=animate,
        )
    grid[current] = 2
    if animate:
        stop_animation(grid=grid)


def do_stuff(part: int, grid: Grid, drop: Point, animate: bool = False) -> int:
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
                animate=animate,
            )
            i += 1

    except ValueError as e:
        return i


if __name__ == "__main__":
    data = load_data("test_input.txt")
    # data = load_data("input.txt")
    animate = True
    start = time.perf_counter()
    grid = get_grid(data=data)
    if animate:
        draw_grid(grid=grid, repaint=False)
    print(f"Part 1: {do_stuff(part=1, grid=grid, drop=(500,0), animate=animate)}")

    grid = get_grid(data=data)
    if animate:
        draw_grid(grid=grid, repaint=False)
    print(f"Part 2: {do_stuff(part=2, grid=grid, drop=(500,0), animate=animate)}")
    print(f"Done in {time.perf_counter()-start:.3f} sec")
