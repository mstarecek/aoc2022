import functools
import itertools
from pprint import pprint


def load_data(input_file: str) -> list[tuple[str, str]]:
    with open(input_file) as f:
        data = f.read()

    pairs = data.split("\n\n")
    return [(pair.splitlines(keepends=False)) for pair in pairs]


data = load_data("test_input.txt")
chain = itertools.chain(*data, ["[[2]]", "[[6]]"])
new_list = list(chain)
sorted_list = sorted(
    new_list,
    key=functools.cmp_to_key(lambda x, y: 1 if len(x) < len(y) else -1),
    # key=lambda x: len(x),
    # reverse=True,
)
pprint(sorted_list)
