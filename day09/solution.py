from collections import defaultdict


def normalize(distance: complex) -> complex:
    return complex(
        (distance.real // abs(distance.real)) if distance.real != 0 else 0,
        (distance.imag // abs(distance.imag)) if distance.imag != 0 else 0,
    )


def calc_tail_move(head: complex, tail: complex) -> complex:
    distance = head - tail
    if abs(distance) < 2:
        return complex(0, 0)
    return normalize(distance)


def load_input(input_file: str) -> list[tuple[str, int]]:
    with open(input_file) as f:
        lines = f.read().splitlines(keepends=False)

    result = []
    for line in lines:
        direction, count = line.split()
        result.append((direction, int(count)))
    return result


def part1(data: list[tuple[str, int]]):
    head = complex(0, 0)
    tail = complex(0, 0)
    grid = defaultdict(int)
    grid[tail] += 1
    for (direction, count) in data:
        for _ in range(count):
            match direction:
                case "U":
                    head += complex(0, 1)
                case "D":
                    head += complex(0, -1)
                case "L":
                    head += complex(-1, 0)
                case "R":
                    head += complex(1, 0)
            diff = calc_tail_move(head, tail)
            if diff:
                tail += diff
                grid[tail] += 1

    return sum(1 for v in grid.values())


def part2(data: list[tuple[str, int]]):
    knots = [complex(0, 0) for _ in range(10)]
    grid = defaultdict(int)
    grid[knots[-1]] += 1

    for (direction, count) in data:
        for _ in range(count):
            match direction:
                case "U":
                    knots[0] += complex(0, 1)
                case "D":
                    knots[0] += complex(0, -1)
                case "L":
                    knots[0] += complex(-1, 0)
                case "R":
                    knots[0] += complex(1, 0)
            for i in range(9):
                diff = calc_tail_move(knots[i], knots[i + 1])
                if not diff:
                    break
                knots[i + 1] += diff
            if diff:
                grid[knots[-1]] += 1

    return sum(1 for v in grid.values())


if __name__ == "__main__":
    # data = load_input("test_input.txt")
    # data = load_input("test_input2.txt")
    data = load_input("input.txt")
    print(f"Part 1: {part1(data)}")
    print(f"Part 2: {part2(data)}")
