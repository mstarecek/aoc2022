import itertools
import re
from typing import Iterator, NamedTuple


class Point(NamedTuple):
    x: int
    y: int


class Sensor(NamedTuple):
    x: int
    y: int
    reach: int

    def points_at_y(self, y: int) -> list[Point] | None:
        distance = abs(self.y - y)
        if distance > self.reach:
            return None
        spare = self.reach - distance
        return [Point(self.x + offset, y) for offset in range(-spare, spare + 1)]

    def outer_points(self, max_distance: int, offset: int = 0) -> Iterator[Point]:
        reach = self.reach + offset
        for i in range(reach + 1):
            for x_sign, y_sign in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
                x = self.x + (i * x_sign)
                y = self.y + (i * y_sign + -1 * y_sign * reach)
                if not (0 <= x <= max_distance and 0 <= y <= max_distance):
                    continue
                # we need to be able to quit early
                yield Point(x, y)
            # yield Point(self.x + i, self.y - reach + i)  # 1Q
            # yield Point(self.x - i, self.y - reach + i)  # 2Q
            # yield Point(self.x - i, self.y + reach - i)  # 3Q
            # yield Point(self.x + i, self.y + reach - i)  # 4Q


def load_data(input_file) -> tuple[list[Sensor], list[Point]]:
    regex = re.compile(
        r"Sensor at x=(?P<s_x>[0-9\-]+), y=(?P<s_y>[0-9\-]+): .* x=(?P<b_x>[0-9\-]+), y=(?P<b_y>[0-9\-]+)"
    )
    sensors = []
    beacons = []

    with open(input_file) as f:
        for line in f:
            if m := regex.match(line):
                s_x = int(m.group("s_x"))
                s_y = int(m.group("s_y"))
                b_x = int(m.group("b_x"))
                b_y = int(m.group("b_y"))
                sensors.append(
                    Sensor(x=s_x, y=s_y, reach=(abs(s_x - b_x) + abs(s_y - b_y)))
                )
                beacons.append(Point(x=b_x, y=b_y))

    return sensors, beacons


def get_impossible_xs(sensors: list[Sensor], intersect_line: int) -> list[int]:
    intersects = [sensor.points_at_y(y=intersect_line) for sensor in sensors]
    intersects = filter(None, intersects)
    flat_list = itertools.chain(*intersects)
    return [p.x for p in flat_list]


def part1(sensors: list[Sensor], beacons: list[Point], intersect_line: int) -> int:
    present_beacons = [b for b in beacons if b.y == intersect_line]
    xs = get_impossible_xs(sensors=sensors, intersect_line=intersect_line)
    return len(set(xs)) - len(set(present_beacons))


def is_point_in_range(sensors: list[Sensor], point: Point) -> bool:
    for sensor in sensors:
        distance = abs(sensor.x - point.x) + abs(sensor.y - point.y)
        if distance <= sensor.reach:
            return True
    return False


def part2(sensors: list[Sensor], beacons: list[Point], max_distance: int) -> int:
    # this one is computation-heavy, use generators whenever possible to quit early
    for sensor in sensors:
        candidates = sensor.outer_points(max_distance=max_distance, offset=1)
        for candidate in candidates:
            if not is_point_in_range(sensors=sensors, point=candidate):
                return candidate.x * 4_000_000 + candidate.y


if __name__ == "__main__":
    # sensors, beacons = load_data("test_input.txt")
    # print(f"Part 1: {part1(sensors, beacons, intersect_line=11)}")
    # print(f"Part 2: {part2(sensors, beacons, max_distance=20)}")

    sensors, beacons = load_data("input.txt")
    # print(f"Part 1: {part1(sensors, beacons, intersect_line=2_000_000)}")
    print(f"Part 2: {part2(sensors, beacons, max_distance=4_000_000)}")
