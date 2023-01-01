# A, X - Rock
# B, Y - Paper
# C, Z - Scissors

HAND_POINTS = {"A": 1, "X": 1, "B": 2, "Y": 2, "C": 3, "X": 3}

ROUND_POINTS = {"win": 6, "draw": 3, "loss": 0}

SUBST = {"X": "A", "Y": "B", "Z": "C"}

# them -> me
WIN = {"A": "B", "B": "C", "C": "A"}
LOSS = {"A": "C", "B": "A", "C": "B"}


def outcome(them: str, me: str) -> str:
    if them == me:
        return "draw"
    if them == "A":
        return "win" if me == "B" else "loss"
    if them == "B":
        return "win" if me == "C" else "loss"
    if them == "C":
        return "win" if me == "A" else "loss"


def points(outcome: str, hand: str) -> int:
    return ROUND_POINTS[outcome] + HAND_POINTS[hand]


def modded(them: str, me: str) -> str:
    if me == "Y":
        return them
    # need to lose
    if me == "X":
        return LOSS[them]
    if me == "Z":
        return WIN[them]


def load_data(input_file: str) -> list[str]:
    with open(input_file) as f:
        return f.read().splitlines()


def do_stuff(lines: list[str], part: int) -> int:

    total = 0
    for line in lines:
        them, me = line.split()
        if part == 1:
            me = SUBST[me]
        else:
            me = modded(them=them, me=me)
        result = outcome(them=them, me=me)
        this_round = points(outcome=result, hand=me)
        total += this_round
    return total


def part1(lines: list[str]) -> int:
    return do_stuff(lines=lines, part=1)


def part2(lines: list[str]) -> int:
    return do_stuff(lines=lines, part=2)


if __name__ == "__main__":
    # data = load_data("test_input.txt")
    data = load_data("input.txt")
    print(f"Part 1: {part1(lines=data)}")
    print(f"Part 2: {part2(lines=data)}")
