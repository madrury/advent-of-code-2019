from typing import Tuple, Dict, List
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
UNEXPLORED, EMPTY, WALL, OXYGEN = 0, 1, 2, 3
HIT_WALL, MOVE_SUCCESS, FOUND_OXYGEN = 0, 1, 2

TILE_DRAW_ARRAY = np.array([' ', '.', '#', 'o'])


def next_position(position: Point, input: int):
    if input == NORTH:
        return (position[0], position[1] + 1)
    elif input == SOUTH:
        return (position[0], position[1] - 1)
    elif input == WEST:
        return (position[0] - 1, position[1])
    elif input == EAST:
        return (position[0] + 1, position[1])


def explore(program: Program):
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


def draw_map(map: Map, position) -> None:
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
    strrep[(position[0] - 25, position[1] - 25)] = '@'
    for row in strrep.T:
        print(''.join(row))


program = Program.from_file(open('./data/program.txt'))
map = explore(program)
draw_map(map, (0, 0))