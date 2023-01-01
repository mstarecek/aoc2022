def load_data(input_file: str) -> list[str]:
    with open(input_file) as f:
        return f.read().splitlines(keepends=False)


def generate_signal(data: list[str]) -> list[int]:
    signal = [1]
    for line in data:
        signal.append(signal[-1])
        match line.split():
            case ["noop"]:
                pass
            case ["addx", number]:
                # signal.append(signal[-1])
                signal.append(signal[-1] + int(number))
    return signal


def part1(data: list[str]):
    poi = [20, 60, 100, 140, 180, 220]
    signal = generate_signal(data=data)
    for p in poi:
        print(f"{p} -> {signal[p-1]} => {(p)*signal[p-1]}")
    return sum(signal[p - 1] * p for p in poi)


def display(crt: list[bool]) -> None:
    lines = [crt[i : i + 40] for i in range(0, len(crt), 40)]
    for line in lines:
        for pixel in line:
            print("#" if pixel else ".", end="")
        print()


def part2(data: list[str]):
    signal = generate_signal(data=data)
    crt = []
    pixel = 0
    for sprite in signal:
        draw = pixel in range(sprite - 1, sprite + 2)
        crt.append(draw)
        pixel += 1
        pixel %= 40

    return crt


if __name__ == "__main__":
    # data = load_data("test_input.txt")
    data = load_data("input.txt")
    print(f"Part 1: {part1(data)}")
    print(f"Part 2:")
    display(part2(data=data))
