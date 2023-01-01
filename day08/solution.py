import math
from pprint import pprint
from typing import List


def load_data(input_file: str) -> List[str]:
    with open(input_file) as f:
        return f.read().splitlines()


def get_grid(lines: List[str]) -> dict:
    grid = {}
    for y, line in enumerate(lines):
        for x, hight in enumerate(line):
            grid[(x, y)] = hight
    return grid


def get_row_left_coords(coords: tuple, dimension: int) -> list[tuple]:
    x, y = coords
    return [(i, y) for i in range(dimension) if i < x]


def get_row_right_coords(coords: tuple, dimension: int) -> list[tuple]:
    x, y = coords
    return [(i, y) for i in range(dimension) if i > x]


def get_column_top_coords(coords: tuple, dimension: int) -> list[tuple]:
    x, y = coords
    return [(x, i) for i in range(dimension) if i < y]


def get_column_bottom_coords(coords: tuple, dimension: int) -> list[tuple]:
    x, y = coords
    return [(x, i) for i in range(dimension) if i > y]


def is_visible(coords: tuple, grid: dict):
    x, y = coords
    dimension = int(math.sqrt(len(grid)))
    if x == 0 or x == dimension:
        return True
    if y == 0 or x == dimension:
        return True

    my_hight = grid[coords]
    # from top
    hights = [grid[c] for c in get_column_top_coords(coords, dimension)]
    if all(h < my_hight for h in hights):
        return True

    # from bottom
    hights = [grid[c] for c in get_column_bottom_coords(coords, dimension)]
    if all(h < my_hight for h in hights):
        return True

    # from left
    hights = [grid[c] for c in get_row_left_coords(coords, dimension)]
    if all(h < my_hight for h in hights):
        return True

    # from right
    hights = [grid[c] for c in get_row_right_coords(coords, dimension)]
    if all(h < my_hight for h in hights):
        return True

    return False


def scenic_score(coords: tuple, grid: dict) -> int:
    x, y = coords
    dimension = int(math.sqrt(len(grid)))
    my_hight = grid[coords]
    if x == 0 or x == dimension:
        return 0
    if y == 0 or x == dimension:
        return 0

    # to top
    top_coords = reversed(get_column_top_coords(coords, dimension))
    top_hights = [grid[k] for k in top_coords]
    # pprint(top_hights)
    top_visible = 0
    for top_h in top_hights:
        top_visible += 1
        if top_h >= my_hight:
            break

    # to bottom
    bottom_coords = get_column_bottom_coords(coords, dimension)
    bottom_hights = [grid[k] for k in bottom_coords]
    # pprint(bottom_hights)
    bottom_visible = 0
    for bottom_h in bottom_hights:
        bottom_visible += 1
        if bottom_h >= my_hight:
            break

    # to left
    left_coords = reversed(get_row_left_coords(coords, dimension))
    left_hights = [grid[k] for k in left_coords]
    # pprint(left_hights)
    left_visible = 0
    for left_h in left_hights:
        left_visible += 1
        if left_h >= my_hight:
            break

    # to right
    right_coords = get_row_right_coords(coords, dimension)
    right_hights = [grid[k] for k in right_coords]
    # pprint(right_hights)
    right_visible = 0
    for right_h in right_hights:
        right_visible += 1
        if right_h >= my_hight:
            break

    return top_visible * bottom_visible * left_visible * right_visible


def do_stuff(lines: List[str], part: int):
    grid = get_grid(lines=lines)
    if part == 1:
        visible = {coord: is_visible(coord, grid) for coord in grid}
        return sum(visible.values())
    else:
        score = {coord: scenic_score(coord, grid) for coord in grid}
        return max(score.values())


if __name__ == "__main__":
    # lines = load_data("test_input.txt")
    lines = load_data("input.txt")

    part = 1
    result = do_stuff(lines=lines, part=part)
    print(f"Part {part}: {result}")

    part = 2
    result = do_stuff(lines=lines, part=part)
    print(f"Part {part}: {result}")
