from typing import List, Dict, Tuple, Set
from collections import defaultdict
import numpy as np

from intcode.intcode import Program, run_until_output


Point = Tuple[int, int]
TileInformation = Tuple[int, int]  # color, n-times-changed

BLACK_INPUT = 0
WHITE_INPUT = 1
TURN_LEFT = 0
TURN_RIGHT = 1

class Robot:

    def __init__(self, program: Program):
        self.program = program
        self.facing = 0
        self.position = (0, 0)
        self.painted: Dict[Point, TileInformation] = {}


DIRECTION_INCREMENTS = {
    0: (0, 1),
    1: (-1, 0),
    2: (0, -1),
    3: (1, 0)
}

def paint(robot: Robot, initial_color: int=0) -> Dict[Point, TileInformation]:
    halt = False
    robot.painted[robot.position] = (1, initial_color)
    while True:
        color, n_times_painted = robot.painted.get(robot.position, (0, 0))
        robot.program.input.append(color)
        _, halt = run_until_output(robot.program, 2)
        if halt:
            break
        direction = robot.program.output.pop()
        color = robot.program.output.pop()
        robot.painted[robot.position] = (color, n_times_painted + 1)
        if direction == 0:
            robot.facing = (robot.facing + 1) % 4
        else:
            robot.facing = (robot.facing - 1) % 4
        dv = DIRECTION_INCREMENTS[robot.facing]
        robot.position = (robot.position[0] + dv[0], robot.position[1] + dv[1])
    return robot.painted

def display_painted(painted: Dict[Point, TileInformation]):
    painted_colors = {key: val[0] for key, val in painted.items()}
    minx = min(k[0] for k in painted_colors)
    maxx = max(k[0] for k in painted_colors)
    miny = min(k[1] for k in painted_colors)
    maxy = max(k[1] for k in painted_colors)
    area = np.zeros(shape=(maxx - minx + 1, maxy - miny + 1), dtype=int)
    for (x, y), color in painted_colors.items():
        area[x - minx,  y - miny] = color
    strrep = np.array(['.', '#'])[area]
    return np.flip(strrep.T, axis=0)
        
CODE = [3,8,1005,8,329,1106,0,11,0,0,0,104,1,104,0,3,8,102,-1,8,10,1001,10,1,10,4,10,1008,8,0,10,4,10,1002,8,1,29,2,1102,1,10,1,1009,16,10,2,4,4,10,1,9,5,10,3,8,1002,8,-1,10,101,1,10,10,4,10,108,0,8,10,4,10,101,0,8,66,2,106,7,10,1006,0,49,3,8,1002,8,-1,10,101,1,10,10,4,10,108,1,8,10,4,10,1002,8,1,95,1006,0,93,3,8,102,-1,8,10,1001,10,1,10,4,10,108,1,8,10,4,10,102,1,8,120,1006,0,61,2,1108,19,10,2,1003,2,10,1006,0,99,3,8,1002,8,-1,10,1001,10,1,10,4,10,1008,8,0,10,4,10,101,0,8,157,3,8,102,-1,8,10,1001,10,1,10,4,10,1008,8,1,10,4,10,1001,8,0,179,2,1108,11,10,1,1102,19,10,3,8,102,-1,8,10,1001,10,1,10,4,10,1008,8,1,10,4,10,101,0,8,209,2,108,20,10,3,8,1002,8,-1,10,101,1,10,10,4,10,108,1,8,10,4,10,101,0,8,234,3,8,102,-1,8,10,101,1,10,10,4,10,108,0,8,10,4,10,1002,8,1,256,2,1102,1,10,1006,0,69,2,108,6,10,2,4,13,10,3,8,102,-1,8,10,101,1,10,10,4,10,1008,8,0,10,4,10,1002,8,1,294,1,1107,9,10,1006,0,87,2,1006,8,10,2,1001,16,10,101,1,9,9,1007,9,997,10,1005,10,15,99,109,651,104,0,104,1,21101,387395195796,0,1,21101,346,0,0,1105,1,450,21101,0,48210129704,1,21101,0,357,0,1105,1,450,3,10,104,0,104,1,3,10,104,0,104,0,3,10,104,0,104,1,3,10,104,0,104,1,3,10,104,0,104,0,3,10,104,0,104,1,21101,0,46413147328,1,21102,404,1,0,1106,0,450,21102,179355823323,1,1,21101,415,0,0,1105,1,450,3,10,104,0,104,0,3,10,104,0,104,0,21102,1,838345843476,1,21101,0,438,0,1105,1,450,21101,709475709716,0,1,21101,449,0,0,1105,1,450,99,109,2,22102,1,-1,1,21102,40,1,2,21101,0,481,3,21101,0,471,0,1105,1,514,109,-2,2105,1,0,0,1,0,0,1,109,2,3,10,204,-1,1001,476,477,492,4,0,1001,476,1,476,108,4,476,10,1006,10,508,1101,0,0,476,109,-2,2106,0,0,0,109,4,2101,0,-1,513,1207,-3,0,10,1006,10,531,21101,0,0,-3,21201,-3,0,1,21201,-2,0,2,21101,1,0,3,21101,550,0,0,1105,1,555,109,-4,2106,0,0,109,5,1207,-3,1,10,1006,10,578,2207,-4,-2,10,1006,10,578,21201,-4,0,-4,1105,1,646,22101,0,-4,1,21201,-3,-1,2,21202,-2,2,3,21101,597,0,0,1105,1,555,22102,1,1,-4,21101,0,1,-1,2207,-4,-2,10,1006,10,616,21101,0,0,-1,22202,-2,-1,-2,2107,0,-3,10,1006,10,638,22102,1,-1,1,21101,638,0,0,106,0,513,21202,-2,-1,-2,22201,-4,-2,-4,109,-5,2106,0,0]
program = Program(CODE[:])
robot = Robot(program=program)
painted = paint(robot)

print(f"The number of tiles painted at least once is {len(painted)}")

robot = Robot(program=Program(CODE[:]))
painted = paint(robot)
for row in display_painted(painted):
    print(''.join(row))