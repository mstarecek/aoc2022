SectionRange = tuple[int, int]


def get_ids(line: str) -> tuple[SectionRange, SectionRange]:
    compact_ranges = line.split(",")
    range1_str = compact_ranges[0].split("-")
    range2_str = compact_ranges[1].split("-")

    return (int(range1_str[0]), int(range1_str[1])), (int(range2_str[0]), int(range2_str[1]))


def contains(range: tuple[SectionRange, SectionRange]) -> bool:
    if range[0][0] <= range[1][0] <= range[0][1]:
        return True
    if range[1][0] <= range[0][0] <= range[1][1]:
        return True
    return False


def overlap(range: tuple[SectionRange, SectionRange]) -> bool:
    if range[0][0] <= range[1][0] <= range[1][1] <= range[0][1]:
        return True
    if range[1][0] <= range[0][0] <= range[0][1] <= range[1][1]:
        return True
    return False


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
