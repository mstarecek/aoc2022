import math
from typing import Callable


class Monkey:
    def __init__(
        self,
    ) -> None:
        self.name: str = "x"
        self.starting_items: list[int] = []
        self.operation: Callable[[int], int] = lambda x: None
        self.test: Callable[[int], bool] = lambda x: None
        self.divider: int = 1
        self.target = {True: "x", False: "x"}
        self.inspections = 0

    def __repr__(self) -> str:
        return (
            f"Monkey {self.name}, {self.inspections} ins, items: {self.starting_items}"
        )

    def calc_replacement(self, number: int, monkeys: "Monkeys") -> int:
        replacement = 1
        for monkey in monkeys:
            replacement *= monkey.divider * monkey.divider
        return number % replacement

    def operate(self, monkeys: "Monkeys", part: int, congruent: int = 1) -> None:
        for item in self.starting_items[:]:
            self.inspections += 1
            new_level = self.operation(item)
            if part == 1:
                new_level //= 3
            else:
                new_level = new_level % congruent
            test_result = self.test(new_level)
            throw_to = self.target[test_result]
            target_monkey = monkeys.get(throw_to)
            target_monkey.starting_items.append(new_level)
            self.starting_items.remove(item)

    @staticmethod
    def from_data(data: str) -> "Monkey":
        lines = data.splitlines()
        monkey = Monkey()
        for line in lines:
            match line.split():
                case ["Monkey", monkey_name]:
                    monkey.name = monkey_name.replace(":", "")
                case ["Starting", "items:", *items_list]:
                    monkey.starting_items = [
                        int(value.replace(",", "")) for value in items_list
                    ]
                case ["Operation:", "new", "=", op1, "+", op2]:
                    assert op1 == "old", "first operand is not 'old'"
                    if op2.isnumeric():
                        monkey.operation = lambda x: x + int(op2)
                    else:
                        monkey.operation = lambda x: x + x
                case ["Operation:", "new", "=", op1, "*", op2]:
                    assert op1 == "old", "first operand is not 'old'"
                    if op2.isnumeric():
                        monkey.operation = lambda x: x * int(op2)
                    else:
                        monkey.operation = lambda x: x * x
                case ["Test:", "divisible", "by", op]:
                    monkey.divider = int(op)
                    monkey.test = lambda x: x % int(op) == 0
                case ["If", "true:", "throw", "to", "monkey", target_name]:
                    monkey.target[True] = target_name
                case ["If", "false:", "throw", "to", "monkey", target_name]:
                    monkey.target[False] = target_name
                case _:
                    assert False, f"Unparsed line: {line}"
        return monkey


class Monkeys(list[Monkey]):
    def get(self, name) -> Monkey:
        for monkey in self:
            if monkey.name == name:
                return monkey

    def operate(self, part: bool, congruent: int) -> None:
        for monkey in self:
            monkey.operate(self, part=part, congruent=congruent)

    def get_congruent(self):
        return math.lcm(*[m.divider for m in self])


def load_data(input_file: str) -> list[str]:
    with open(input_file) as f:
        data = f.read()
    return data.split("\n\n")


def load_monkeys(data: list[str]) -> Monkeys:
    return Monkeys([Monkey.from_data(d) for d in data])


def do_stuff(monkeys: Monkeys, part: int) -> int:
    congruent = monkeys.get_congruent()
    for i in range(20 if part == 1 else 10_000):
        monkeys.operate(part=part, congruent=congruent)
        print(
            f"After round {i+1}, the monkeys are holding items with these worry levels:"
        )
        for monkey in monkeys:
            print(
                f"Monkey {monkey.name}: inspected: {monkey.inspections}, items: {monkey.starting_items}"
            )
        print()

    inspections = sorted([m.inspections for m in monkeys], reverse=True)
    return inspections[0] * inspections[1]


if __name__ == "__main__":
    # data = load_data("test_input.txt")
    data = load_data("input.txt")
    monkeys = load_monkeys(data)
    print(f"Part1: {do_stuff(monkeys, part=1)}")

    monkeys = load_monkeys(data)
    print(f"Part2: {do_stuff(monkeys, part=2)}")
