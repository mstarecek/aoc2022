import functools


def find_common(packs: list[str]) -> str:
    set_list = (set(pack) for pack in packs)
    return functools.reduce(set.intersection, set_list).pop()


def get_priority(item: str) -> int:
    if "a" <= item <= "z":
        return ord(item) - ord("a") + 1
    if "A" <= item <= "Z":
        return ord(item) - ord("A") + 27


def load_data(input_file: str) -> list[str]:
    with open(input_file) as f:
        return f.read().splitlines()


def part1(lines: list[str]) -> int:
    total = 0
    for line in lines:
        compartments = [line[: len(line) // 2], line[len(line) // 2 :]]
        duplicate = find_common(compartments)
        priority = get_priority(item=duplicate)
        total += priority
    return total


def part2(lines: list[str]) -> int:
    set_lines = (lines[i : i + 3] for i in range(0, len(lines), 3))
    total = 0
    for line_set in set_lines:
        duplicate = find_common(line_set)
        priority = get_priority(item=duplicate)
        total += priority
    return total


if __name__ == "__main__":
    # data = load_data("test_input.txt")
    data = load_data("input.txt")
    print(f"Part 1: {part1(lines=data)}")
    print(f"Part 2: {part2(lines=data)}")
