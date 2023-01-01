class Position(tuple[int, int]):
    pass


class Grid(dict[Position]):
    pass


def load_data(input_file: str) -> Grid:
    with open(input_file) as f:
        data = f.read().splitlines()


if __name__ == "__main__":
    pass
