import re
from collections import defaultdict
from dataclasses import dataclass, field
from pprint import pprint

Distance = dict[(str, str), int]


@dataclass(frozen=True)
class Valve:
    name: str
    rate: int
    is_open: bool = False
    tunnels: list[str] = field(default_factory=list)


class Valves(list[Valve]):
    def get_valve(self, name: str) -> Valve | None:
        for valve in self:
            if valve.name == name:
                return valve
        return None

    def get_pressure(self) -> int:
        return sum(valve.rate for valve in self if valve.is_open)

    def names(self) -> list[str]:
        return [valve.name for valve in self]


@dataclass
class State:
    minute: int
    at_valve: Valve
    opened: list[str] = field(default_factory=list)
    rate: int = 0
    total: int = 0

    def at_end(self, end: int = 30):
        return self.total + self.rate * (end - self.minute + 1)

    def __repr__(self):
        return "T%s @%s OP:%s r%d total: %d flow: %d" % (
            self.minute,
            self.at_valve.name,
            self.opened,
            self.rate,
            self.total,
            self.at_end(),
        )


def load_data(input_file: str) -> Valves:
    with open(input_file) as f:
        lines = f.read().splitlines(keepends=False)
    regex = re.compile(
        r"Valve (?P<name>\w+) .* rate=(?P<rate>\d+); .* valve(s)? (?P<tunnels>[A-Z, ]+)"
    )
    result = Valves()
    for line in lines:
        if m := regex.match(line):
            result.append(
                Valve(
                    name=m.group("name"),
                    rate=int(m.group("rate")),
                    is_open=int(m.group("rate")) == 0,
                    tunnels=m.group("tunnels").replace(" ", "").split(","),
                )
            )
    return result


def get_distances(valves: Valves) -> list[Distance]:
    all_distances = defaultdict(lambda: 99)
    names = valves.names()

    for name in names:
        for tunnel in valves.get_valve(name=name).tunnels:
            all_distances[(name, tunnel)] = 1
    for k in names:
        for i in names:
            for j in names:
                all_distances[(i, j)] = min(
                    all_distances[(i, j)], all_distances[(i, k)] + all_distances[(k, j)]
                )
    working_valves = [valve.name for valve in valves if valve.rate > 0]
    distances = {}
    for name in names:
        for tunnel in working_valves:
            if name == tunnel:
                continue
            distances[(name, tunnel)] = all_distances[(name, tunnel)]
    return distances


def part1(data: Valves, time: int = 30) -> int:
    working_valves = [valve for valve in data if valve.rate > 0]
    working_valves.sort(key=lambda x: x.name)
    distances = get_distances(valves=data)
    # pprint(distances)
    possibilities = [State(minute=1, at_valve=data.get_valve(name="AA"))]
    expected_flow = 0
    while possibilities:
        # pprint(f"\n{possibilities=}\n")
        state = possibilities.pop()
        expected_flow = max(expected_flow, state.at_end())
        if state.minute == time:
            continue
        current_valve = state.at_valve
        if state.at_valve.name not in state.opened and state.at_valve.rate > 0:
            possibilities.append(
                State(
                    minute=state.minute + 1,
                    at_valve=current_valve,
                    opened=state.opened.copy() + [current_valve.name],
                    rate=state.rate + current_valve.rate,
                    total=state.total + state.rate,
                )
            )
            continue
        for destination_valve in working_valves:
            if destination_valve.name in state.opened:
                continue
            distance = distances[(current_valve.name, destination_valve.name)]
            if state.minute + distance >= time:
                continue
            possibilities.append(
                State(
                    minute=state.minute + distance,
                    at_valve=destination_valve,
                    opened=state.opened.copy(),
                    rate=state.rate,
                    total=state.total + (state.rate * distance),
                )
            )
    return expected_flow


if __name__ == "__main__":
    data = load_data("input.txt")
    print(f"Part1: {part1(data=data, time=30)}")
