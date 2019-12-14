from typing import IO, List, Tuple, Set
from math import gcd


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