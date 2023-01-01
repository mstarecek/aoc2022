import functools
import itertools

Signal = int | list[int] | list["Signal"]


def load_data(input_file: str) -> list[tuple[Signal, Signal]]:
    with open(input_file) as f:
        data = f.read()

    pairs = data.split("\n\n")
    result = []
    for pair in pairs:
        left, right = pair.splitlines(keepends=False)
        result.append((eval(left), eval(right)))
    return result


def compare(left: Signal, right: Signal) -> bool | None:
    for l, r in itertools.zip_longest(left, right):
        match l, r:
            case int(), int():
                if l == r:
                    continue
                return l < r
            case int(), list():
                partial = compare([l], r)
            case list(), int():
                partial = compare(l, [r])
            case list(), list():
                partial = compare(l, r)
            case _, None:
                return False
            case None, _:
                return True
            case _:
                raise RuntimeError(f"Unable to process '{l}' vs '{r}'")
        if partial is not None:
            return partial


def part1(data: list[tuple[str, str]]):
    result = 0
    for i, pair in enumerate(data):
        if compare(left=pair[0], right=pair[1]):
            result += i + 1

    return result


def part2(data: list[tuple[str, str]]):
    new_list = list(itertools.chain(*data, [[[2]], [[6]]]))
    new_list.sort(
        key=functools.cmp_to_key(
            lambda x, y: 1 if compare(x, y) else -1,
        ),
        reverse=True,
    )
    key1 = new_list.index([[6]]) + 1
    key2 = new_list.index([[2]]) + 1
    return key1 * key2


if __name__ == "__main__":
    # data = load_data("test_input.txt")
    data = load_data("input.txt")
    print(f"Part 1: {part1(data)}")
    print(f"Part 2: {part2(data)}")
