def load_data(input_file: str) -> list[int]:
    with open(input_file) as f:
        data = f.read()

    packages = data.split("\n\n")
    return [sum(map(int, part.split())) for part in packages]


def part1(calories: list[int]) -> int:
    return max(calories)


def part2(calories: list[int]) -> int:
    return sum(sorted(calories, reverse=True)[0:3])


if __name__ == "__main__":
    # calories = load_data("test_input.txt")
    calories = load_data("input.txt")
    print(f"Part 1: {part1(calories)}")
    print(f"Part 2: {part2(calories)}")
