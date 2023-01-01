import math

import z3


def load_data(input_file: str) -> list[str]:
    with open(input_file) as f:
        return f.read().splitlines()


SNAFU_TO_INT = {"=": -2, "-": -1}
INT_TO_SNAFU = {-2: "=", -1: "-"}


def get_digit(snafu: str) -> int:
    try:
        return SNAFU_TO_INT[snafu]
    except KeyError:
        return int(snafu)


def get_snafu(digit: int) -> str:
    return INT_TO_SNAFU.get(digit, str(digit))


def to_int(snafu: str) -> int:
    result = 0
    for power, number in enumerate(reversed(snafu)):
        order = math.pow(5, power)
        multiplier = get_digit(number)
        result += multiplier * order
    # print(f"{snafu=}, {result=}")
    return int(result)


def to_snafu(number: int) -> str:
    max_digits = math.ceil(math.log(number, 5)) + 1
    solver = z3.Solver()
    A = z3.IntVector("a", max_digits)
    for a in A:
        solver.add(a < 3)
        solver.add(a > -3)
    AP = [a * math.pow(5, i) for i, a in enumerate(A)]
    solver.add(z3.Sum(AP) == number)
    assert solver.check() == z3.sat, "Not satisfiable"
    model = solver.model()
    result = ""
    for a in A:
        coefficient = model.eval(a).as_long()
        snafu = get_snafu(coefficient)
        # print(a, coefficient, snafu)
        result = snafu + result
    return result.lstrip("0")


def part1(snafus: list[str]) -> str:
    total = sum(to_int(s) for s in snafus)
    # print(f"{total=}")
    return to_snafu(total)


if __name__ == "__main__":
    # data = load_data("test_input.txt")
    data = load_data("input.txt")
    print(f"Part1 : {part1(data)}")
