def get_ids(line: str) -> tuple[set[int], set[int]]:
    compact_ranges = line.split(",")
    range1_str = compact_ranges[0].split("-")
    range2_str = compact_ranges[1].split("-")

    range1 = range(int(range1_str[0]), int(range1_str[1]) + 1)
    range2 = range(int(range2_str[0]), int(range2_str[1]) + 1)

    return set(range1), set(range2)


def contains(range: tuple[set[int], ...]) -> bool:
    return range[0].issubset(range[1]) or range[1].issubset(range[0])


def overlap(range: tuple[set[int], ...]) -> bool:
    return bool(range[0].intersection(range[1]))


def load_data(input_file: str) -> list:
    with open(input_file) as f:
        return f.read().splitlines()


def part1(lines: list[str]) -> int:
    total = 0
    for line in lines:
        ids = get_ids(line)
        if contains(ids):
            total += 1
    return total


def part2(lines: list[str]) -> int:
    total = 0
    for line in lines:
        ids = get_ids(line=line)
        if overlap(ids):
            total += 1
    return total


if __name__ == "__main__":
    # data = load_data("test_input.txt")
    data = load_data("input.txt")
    print(f"Part 1: {part1(lines=data)}")
    print(f"Part 2: {part2(lines=data)}")
