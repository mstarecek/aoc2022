from collections import defaultdict


def main(input_file: str):
    cwd = []
    sizes = defaultdict(int)

    with open(input_file) as f:
        for line in f:
            match line.strip().split():
                case ["$", "cd", "/"]:
                    cwd = ["/"]
                case ["$", "cd", ".."]:
                    cwd.pop()
                case ["$", "cd", target]:
                    cwd.append(target)
                case ["$", "ls"]:
                    continue
                case ["dir", _]:
                    continue
                case [size, _]:
                    for i in range(len(cwd)):
                        sizes["/".join(cwd[: i + 1])] += int(size)

    values = sizes.values()
    less_than_hundo = [v for v in values if v < 100_000]
    print(sum(less_than_hundo))

    free = 70000000 - sizes["/"]
    need = 30000000 - free
    will_do = [v for v in values if v > need]
    print(min(will_do))


import time

if __name__ == "__main__":
    # timeit.timeit("main()", number=1)

    start = time.perf_counter()
    main("input.txt")
    end = time.perf_counter()
    print(f"Done in {(end-start)*1000:.3f}")
