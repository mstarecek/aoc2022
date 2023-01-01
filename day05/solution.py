import re
from collections import defaultdict
from typing import NamedTuple

regex = re.compile(r"move (?P<count>\d+) from (?P<from>\d+) to (?P<to>\d+)")


class Operation(NamedTuple):
    count: int
    from_col: int
    to_col: int

    @staticmethod
    def from_data(lines: list[str]) -> list["Operation"]:
        return [
            Operation(int(m.group("count")), int(m.group("from")), int(m.group("to")))
            for line in lines
            if (m := regex.match(line))
        ]


class State(defaultdict[str]):
    @staticmethod
    def from_data(lines: list[str]) -> "State":
        state_lines = [line for line in lines if "[" in line]
        state_lines.reverse()
        columns = (max(len(line) for line in state_lines) + 1) // 4
        state = State(str)
        for i in range(columns):
            for line in state_lines:
                cargo = line[i * 4 + 1]
                if cargo in ["", " "]:
                    continue
                state[i + 1] += cargo
        return state

    def operate(self, operation: Operation, keep_order: bool = False) -> None:
        moving = self[operation.from_col][-operation.count :]
        self[operation.from_col] = self[operation.from_col][: -operation.count]
        self[operation.to_col] += moving if keep_order else moving[::-1]

    def get_message(self) -> str:
        return "".join(stack[-1] for stack in self.values())


def load_data(input_file: str) -> tuple[State, list[Operation]]:
    with open(input_file) as f:
        lines = f.read().splitlines()
    return State.from_data(lines), Operation.from_data(lines)


def do_stuff(state: State, operations: list[Operation], part: int) -> str:
    for operation in operations:
        state.operate(operation, keep_order=part == 2)
    return state.get_message()


def part1(state: State, operations: list[Operation]) -> str:
    return do_stuff(state=state, operations=operations, part=1)


def part2(state: State, operations: list[Operation]) -> str:
    return do_stuff(state=state, operations=operations, part=2)


if __name__ == "__main__":
    # state, operations = load_data("test_input.txt")
    state, operations = load_data("input.txt")
    print(f"Part 1: {part1(state, operations)}")
    # state, operations = load_data("test_input.txt")
    state, operations = load_data("input.txt")
    print(f"Part 2: {part2(state, operations)}")
