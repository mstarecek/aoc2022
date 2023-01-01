import re
import time

import z3


def load_data(input_file: str) -> dict[str, str]:
    with open(input_file) as f:
        return f.read().splitlines()


def lines_to_dict(lines: list[str]) -> dict[str, str]:
    result = {}
    for line in lines:
        dest, src = line.split(":")
        result[dest] = src.strip()
    return result


def get_equation(lines: list[str], part: int) -> str:
    knowledge = lines_to_dict(lines=lines)
    equation = knowledge.pop("root")
    if part == 2:
        knowledge["humn"] = "humn"
        equation = equation.replace("+", "==")
    regex = re.compile(r" | +| -| \*| /| ==|\(|\)")
    while True:
        equation_parts = regex.split(equation)
        non_numerics = 0
        for eq_part in equation_parts:
            if not eq_part:
                continue
            if eq_part.isalpha():
                non_numerics += 1
                equation = equation.replace(eq_part, f"({knowledge[eq_part]})")
        if part == 1 and non_numerics == 0:
            break
        if part == 2 and non_numerics == 1:
            break
    return equation


def part1(lines: list[str]) -> int:
    equation = get_equation(lines=lines, part=1)
    return int(eval(equation))


def part2(lines: list[int]) -> int:
    start = time.perf_counter()
    equation = get_equation(lines=lines, part=2)
    print(f"Equation done in {(time.perf_counter()-start)*1000:.3f} ms.")
    print(f"Equation len: {len(equation)}")
    humn = z3.Int("humn")
    solver = z3.Solver()
    start = time.perf_counter()
    solver.add(eval(equation))
    solver.check()
    print(f"Z3 done in {(time.perf_counter()-start)*1000:.3f} ms.")
    return solver.model()[humn]


if __name__ == "__main__":

    # data = load_data("test_input.txt")
    data = load_data("input.txt")
    print(f"Part1 : {part1(lines=data)}")
    print(f"Part2 : {part2(lines=data)}")
