import time
from typing import Callable, Iterator


class Node:
    def __init__(self, name: str, parent: "Node") -> None:
        self.name = name
        self.parent = parent
        self.full_path = self._set_full_path()
        self.files: dict[str, int] = {}
        self.children: list["Node"] = []

    def _set_full_path(self) -> str:
        if self.parent is None:
            return self.name
        full_name = self.parent.full_path
        if not full_name.endswith("/"):
            full_name += "/"
        full_name += self.name
        return full_name

    def __repr__(self) -> str:
        return f"{self.full_path} : {len(self.files)} files"

    def add_children(self, name: str) -> None:
        if any(child.name == name for child in self.children):
            return
        self.children.append(Node(name=name, parent=self))

    def add_file(self, name: str, size: int) -> None:
        self.files[name] = size

    def get_node(self, name: str) -> "Node":
        for node in self.children:
            if node.name == name:
                return node

    def find_node(self, predicate: Callable[["Node"], bool]) -> "Node":
        if predicate(self):
            yield self
        for child in self.children:
            yield from child.find_node(predicate)

    def get_size(self) -> int:
        size = sum(self.files.values())
        size += sum(child.get_size() for child in self.children)
        return size

    def get_sizes(self, predicate: Callable[[int], bool]) -> Iterator[int]:
        size = self.get_size()
        if predicate(size):
            yield size
        for child in self.children:
            yield from child.get_sizes(predicate)

    @staticmethod
    def setup_tree(data: list[str]) -> "Node":
        root_node = Node(name="/", parent=None)
        actual_node = root_node
        for line in data:
            match line.split():
                case ["$", "cd", "/"]:
                    actual_node = root_node
                case ["$", "cd", ".."]:
                    actual_node = actual_node.parent
                case ["$", "cd", name]:
                    actual_node = actual_node.get_node(name=name)
                case ["$", "ls"]:
                    pass
                case ["dir", name]:
                    actual_node.add_children(name=name)
                case [type_size, name]:
                    actual_node.add_file(name=name, size=int(type_size))
        return root_node


def load_data(input_file: str) -> list[str]:
    with open(input_file) as f:
        return f.read().splitlines()


def part1(start: Node) -> int:
    return sum(start.get_sizes(lambda x: x < 100_000))


def part2(start: Node) -> int:
    free = 70_000_000 - start.get_size()
    needed = 30_000_000 - free

    return min(start.get_sizes(lambda x: x > needed))


if __name__ == "__main__":
    overall_start = time.perf_counter()
    print("Using transformation")

    start = time.perf_counter()
    data = load_data("input.txt")
    print(f"Data Load in {(time.perf_counter()-start)*1000:.3f} ms.")

    start = time.perf_counter()
    root_node = Node.setup_tree(data)
    print(f"Setup in {(time.perf_counter()-start)*1000:.3f} ms.")

    start = time.perf_counter()
    print(f"Part1: {part1(root_node)}")
    print(f"Part1 done in {(time.perf_counter()-start)*1000:.3f} ms.")

    start = time.perf_counter()
    print(f"Part2: {part2(root_node)}")
    print(f"Part2 done in {(time.perf_counter()-start)*1000:.3f} ms.")

    print(f"Done in {(time.perf_counter()-overall_start)*1000:.3f} ms")
