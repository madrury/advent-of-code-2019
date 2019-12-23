from typing import Tuple, Dict, List, Iterable, Optional
from intcode.intcode import Program, run_until_output
from time import sleep
import random
import numpy as np

Point = Tuple[int, int]
Map = Dict[Point, int]


NORTH, SOUTH, WEST, EAST = 1, 2, 3, 4
TURN_RIGHT = {
    NORTH: EAST, EAST: SOUTH, SOUTH: WEST, WEST: NORTH
}
TURN_LEFT = {
    NORTH: WEST, WEST: SOUTH, SOUTH: EAST, EAST: NORTH
}
UNEXPLORED, EMPTY, WALL, OXYGEN, GAS = 0, 1, 2, 3, 4
HIT_WALL, MOVE_SUCCESS, FOUND_OXYGEN = 0, 1, 2

TILE_DRAW_ARRAY = np.array([' ', ' ', '#', 'o', '~'])


def next_position(position: Point, input: int) -> Point:
    if input == NORTH:
        return (position[0], position[1] + 1)
    elif input == SOUTH:
        return (position[0], position[1] - 1)
    elif input == WEST:
        return (position[0] - 1, position[1])
    elif input == EAST:
        return (position[0] + 1, position[1])


def explore(program: Program) -> Map:
    map: Map = {}
    position: Point = (0, 0)
    current_direction, output = NORTH, None
    # Move north until we hit a wall.
    while True:
        program.add_input(current_direction)
        _, _ = run_until_output(program)
        output = program.output.pop()
        if output == MOVE_SUCCESS:
            position = next_position(position, current_direction)
            map[position] = EMPTY
            continue
        elif output == HIT_WALL:
            map[next_position(position, current_direction)] = WALL
            current_direction = TURN_LEFT[current_direction]
            break
    # Now the main explore loop. The goal here is to make sure we keep a wall
    # to the right. We start with a wall to the north of us.
    have_moved = False
    while True:
        program.add_input(current_direction)
        _, _ = run_until_output(program)
        output = program.output.pop()
        if output == HIT_WALL:
            map[next_position(position, current_direction)] = WALL
            current_direction = TURN_LEFT[current_direction]
        elif output == FOUND_OXYGEN:
            position, have_moved = next_position(position, current_direction), True
            map[position] = OXYGEN
        elif output == MOVE_SUCCESS:
            position, have_moved = next_position(position, current_direction), True
            map[position] = EMPTY
            # Check if there is a wall to our right.
            current_direction = TURN_RIGHT[current_direction]
            program.add_input(current_direction)
            _, _ = run_until_output(program)
            output = program.output.pop()
            # If we hit a well, there is still a wall to our right, so we
            # should keep going.
            if output == HIT_WALL:
                map[next_position(position, current_direction)] = WALL
                current_direction = TURN_LEFT[current_direction]
            # There is no longer a wall to the right, so we need to turn and
            # move in that direction.
            elif output == MOVE_SUCCESS:
                position = next_position(position, current_direction)
                map[position] = EMPTY
            elif output == FOUND_OXYGEN:
                position = next_position(position, current_direction)
                map[position] = OXYGEN
        # We're back where we started, so we can bail.
        if have_moved and position == (0, 0):
            break
    return map


def find_shortest_path(map: Map, origin: Point) -> List[Point]:
    all_positions = {p for p in map if map[p] in (EMPTY, OXYGEN)}
    pervious: Dict[Point, Point] = {}
    distances = {p: 10**4 for p in all_positions}
    distances[origin] = 0
    # Dijkstra's algorithm.
    while all_positions:
        min_distance_position = min(
            {p: dist for p, dist in distances.items() if p in all_positions},
            key=distances.get
        )
        all_positions.remove(min_distance_position)
        if map[min_distance_position] == OXYGEN:
            break
        for p in adjacent_positions(map, min_distance_position):
            alt_distance = distances[min_distance_position] + 1
            if alt_distance < distances[p]:
                distances[p] = alt_distance
                pervious[p] = min_distance_position
    # Now find the shortet path.
    path: List[Point] = []
    current = min_distance_position
    while current != origin:
        path.append(current)
        current = pervious[current]
    return path


def adjacent_positions(map: Map, position: Point) -> Iterable[Point]:
    for direction in [NORTH, SOUTH, EAST, WEST]:
        attempt = next_position(position, direction)
        if map[attempt] in (EMPTY, OXYGEN):
            yield attempt


def draw_map(map: Map, position: Optional[Point]=None, path: Optional[List[Point]]=None) -> None:
    if not map:
        return
    minx = min(k[0] for k in map)
    maxx = max(k[0] for k in map)
    miny = min(k[1] for k in map)
    maxy = max(k[1] for k in map)
    #area = np.zeros(shape=(maxx - minx + 1, maxy - miny + 1), dtype=int)
    area = np.zeros(shape=(50, 50), dtype=int)
    for (x, y), id in map.items():
        area[x - 25,  y - 25] = id
    strrep = TILE_DRAW_ARRAY[area]
    if position:
        strrep[(position[0] - 25, position[1] - 25)] = '@'
    if path:
        for p in path:
            strrep[p[0] - 25, p[1] - 25] = '.'
    for row in strrep.T:
        print(''.join(row))

program = Program.from_file(open('./data/program.txt'))
map = explore(program)
path = find_shortest_path(map, (0, 0))
draw_map(map, (0, 0), path[1:])

print(f"The shortest path to the oxygen is {len(path)} steps.")