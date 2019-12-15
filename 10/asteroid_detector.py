from typing import IO, List, Tuple, Set, Iterable
from math import gcd, atan2, pi
from collections import defaultdict


Chart = List[List[int]]
Point = Tuple[int, int]


def read_asteroid_chart(f: IO) -> Chart:
    chart = []
    char_to_int ={'.': 0, '#': 1}
    for line in f:
        chart.append([char_to_int[ch] for ch in line.strip()])
    return chart

def get_asteroid_positions(chart: Chart) -> Set[Point]:
    positions = set()
    for j, row in enumerate(chart):
        for i, has_asteroid in enumerate(row):
            if has_asteroid:
                positions.add((i, j))
    return positions

def get_integer_points_interior_to_segment(p1: Point, p2:Point) -> Set[Point]:
    (x1, y1), (x2, y2) = p1, p2
    g = gcd(x2 - x1, y2 - y1)
    return set(
        (x1 + i * (x2 - x1) // g, y1 + i * (y2 - y1) // g) for i in range(1, g)
    )

def get_asteroids_visible_from(asteroid: Point, poistions: Set[Point]) -> Set[Point]:
    visible = set()
    for candidate in poistions:
        possible_blocked_points = get_integer_points_interior_to_segment(
            asteroid, candidate
        )
        if not possible_blocked_points & poistions:
            visible.add(candidate)
    return visible
    
def find_best_station_position(chart: Chart) -> Tuple[Point, int]:
    positions = get_asteroid_positions(chart)
    candidates = {}
    for position in positions:
        # Off by one because we are counting ourselves as visible
        candidates[position] = len(get_asteroids_visible_from(position, positions)) - 1
    return max(candidates.items(), key=lambda item: item[1])

def angle_to_vertical(p: Point, reference: Point) -> float:
    theta = atan2(*(p[0] - reference[0], p[1] - reference[1]))
    return - theta

def reduce_point(p: Point, reference: Point):
    (x, y), (r1, r2) = p, reference
    g = gcd(x - r1, y - r2)
    return ((x - r1) // g, (y - r2) // g)

def group_asteroids_by_angle(positions: Set[Point], reference: Point):
    groups = defaultdict(list)
    for position in positions:
        groups[reduce_point(position, reference)].append(position)
    return groups

def sort_asteroid_groups_by_angle(positions: Set[Point], reference: Point) -> List[List[Point]]:
    groups = group_asteroids_by_angle(positions, reference)
    s = sorted(groups.items(), key=lambda item: angle_to_vertical(item[1][0], reference))
    norm = lambda p: (p[0] - reference[0])**2 + (p[1] - reference[1])**2
    return [list(sorted(x[1], key=norm)) for x in s]

def iter_asteroids_by_angle(positions: Set[Point], reference: Point) -> Iterable[Point]:
    # positions = chart
    positions.remove(reference)
    s = sort_asteroid_groups_by_angle(positions, reference)
    while not all(group == [] for group in s):
        for group in s:
            if group:
                yield group.pop(0)



if __name__ == '__main__':
    chart1 = read_asteroid_chart(open('./data/chart-1.txt', 'r'))
    assert find_best_station_position(chart1) == ((3, 4), 8)

    chart2 = read_asteroid_chart(open('./data/chart-2.txt', 'r'))
    assert find_best_station_position(chart2) == ((5, 8), 33)

    chart3 = read_asteroid_chart(open('./data/chart-3.txt', 'r'))
    assert find_best_station_position(chart3) == ((1, 2), 35)

    chart4 = read_asteroid_chart(open('./data/chart-4.txt', 'r'))
    assert find_best_station_position(chart4) == ((6, 3), 41)

    chart5 = read_asteroid_chart(open('./data/chart-5.txt', 'r'))
    assert find_best_station_position(chart5) == ((11, 13), 210)

    chart = read_asteroid_chart(open('./data/chart.txt', 'r'))
    location, n_visible = find_best_station_position(chart)
    print(f"Best space station location is {location} with {n_visible} visible asteroids")

    # positions = get_asteroid_positions(chart5)
    # order_destroyed = list(iter_asteroids_by_angle(positions, (11, 13)))
    # print(order_destroyed)
    # print(f"The 200th asteroid to be destroyed is {order_destroyed[199]}")

    # chart_simple = read_asteroid_chart(open('./data/chart-simple.txt', 'r'))
    # positions = get_asteroid_positions(chart_simple)
    # order_destroyed = list(iter_asteroids_by_angle(positions, (2, 2)))
    # print(order_destroyed)

    positions = get_asteroid_positions(chart)
    order_destroyed = list(iter_asteroids_by_angle(positions, (37, 25)))
    print(f"The 200th asteroid to be destroyed is {order_destroyed[199]}")