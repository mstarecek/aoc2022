def load_file(input_file: str) -> list[int]:
    with open(input_file) as f:
        data = f.read().splitlines()
    return [int(x) for x in data]


def mix(file: list[int], n: int = 1) -> list[int]:
    modulus = len(file)
    indexes = {i: i for i in range(modulus)}
    for j in range(n):
        for i in range(len(file)):
            for k, v in indexes.items():
                if v == i:
                    pop_index = k
                    break
            if file[pop_index] == 0:
                # print("skipping 0")
                continue
            v = file.pop(pop_index)
            target_index = (pop_index + v) % (modulus - 1)
            if target_index == 0:
                target_index = modulus
            file.insert(target_index, v)
            if pop_index < target_index:
                for shift_i in range(pop_index, target_index):
                    try:
                        indexes[shift_i] = indexes[shift_i + 1]
                    except KeyError:
                        indexes[shift_i] = i
            else:
                for shift_i in range(pop_index, target_index, -1):
                    indexes[shift_i] = indexes[shift_i - 1]

            if target_index != modulus:
                indexes[target_index] = i
            # assert len(indexes) == len(set(indexes.values()))
            # print(v, file)
        # print(f"After {j+1}: {file=}")
    return file


def get_result(file: list[int]) -> int:
    start = file.index(0)
    one = file[(start + 1000) % len(file)]
    two = file[(start + 2000) % len(file)]
    three = file[(start + 3000) % len(file)]
    print(f"{one=}, {two=}, {three=}")
    return sum([one, two, three])


def part1(file: list[int]) -> int:
    mixed_file = mix(file=file)
    return get_result(mixed_file)


def part2(file: list[int]) -> int:
    file = [x * 811589153 for x in file]
    mixed_file = mix(file=file, n=10)
    return get_result(mixed_file)


if __name__ == "__main__":
    input_file = "test_input.txt"
    file = load_file(input_file=input_file)
    print(f"Part1 :{part1(file=file)}")
    file = load_file(input_file=input_file)
    print(f"Part2 :{part2(file=file)}")
