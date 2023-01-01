def get_start(line: str, token_len: int) -> int:
    for i in range(token_len, len(line)):
        chunk = line[i - token_len : i]
        if len(set(chunk)) == token_len:
            return i


def load_data(input_file: str) -> str:
    with open(input_file) as f:
        return f.read().strip()


def part1(signal: str) -> int:
    return get_start(signal, token_len=4)


def part2(signal: str) -> int:
    return get_start(signal, token_len=14)


if __name__ == "__main__":
    data = load_data("input.txt")
    print(f"Part 1: {part1(signal=data)}")
    print(f"Part 2: {part2(signal=data)}")
