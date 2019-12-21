from typing import Dict, Tuple, DefaultDict, Optional
from collections import defaultdict
from time import sleep
import subprocess

from intcode.intcode import Program, run_until_output
import numpy as np

TILE_ID_LOOKUP ={
    0: ' ',  # Empty
    1: '#',  # Wall
    2: '+',  # Block
    3: '-',  # Paddle
    4: 'o'   # Ball
}
TILE_DRAW_ARRAY = np.array([' ', '#', '+', '-', 'o'])
NEUTRAL, LEFT, RIGHT = 0, -1, 1

Screen = DefaultDict[Tuple[int, int], int]

class Breakout:

    def __init__(self, program: Program):
        self.program = program
        self.program[0] = 2  # Free to play mode.
        self.screen: Screen = defaultdict(lambda: 0)
        self.paddle: Optional[Tuple[int, int]] = None
        self.ball: Optional[Tuple[int, int]] = None
        self.score: int = 0

    def run_game(self) -> None:
        halt = False
        prior_screen = None
        while True:
            _, _ = run_until_output(self.program, output_len=3)
            try:
                x, y, tile_id = self.program.output
            except ValueError:
                break
            if x == -1 and y == 0:
                self.score = tile_id  # Not really a tile_id...
            else:
                self.screen[(x, y)] = tile_id
            self.draw_screen()
            #if self.screen == prior_screen:
            # sleep(0.001)
            self.paddle, self.ball = game.get_paddle_position(), game.get_ball_position()
            self.move_paddle_towards_ball()
            self.program.reset_output()
            #subprocess.call('clear', shell=True)
        # return screen
    
    def move_paddle_towards_ball(self) -> None:
        if self.paddle and self.ball:
            dx = self.paddle[0] - self.ball[0]
            if dx == 0:
                self.program.input.append(NEUTRAL)
            elif dx > 0:
                self.program.input.append(LEFT)
            elif dx < 0:
                self.program.input.append(RIGHT)
            else:
                raise ValueError
    
    def get_position(self, needle: int) -> Optional[Tuple[int, int]]:
        positions = [position for position, val in self.screen.items() if val == needle]
        if positions:
            assert len(positions) == 1
            return positions[0]
        else:
            return None
    
    def get_paddle_position(self) -> Optional[Tuple[int, int]]:
        return self.get_position(needle=3)
    
    def get_ball_position(self) -> Optional[Tuple[int, int]]:
        return self.get_position(needle=4)

    def draw_screen(self) -> None:
        if not self.screen:
            return
        minx = min(k[0] for k in self.screen)
        maxx = max(k[0] for k in self.screen)
        miny = min(k[1] for k in self.screen)
        maxy = max(k[1] for k in self.screen)
        area = np.zeros(shape=(maxx - minx + 1, maxy - miny + 1), dtype=int)
        for (x, y), id in self.screen.items():
            area[x - minx,  y - miny] = id
        strrep = TILE_DRAW_ARRAY[area]
        for row in strrep.T:
            print(''.join(row))
        print(f"Score: {self.score}")
        print(f"Paddle: {self.paddle}")
        print(f"Ball: {self.ball}")


program = Program.from_file(open('./data/game.txt', 'r'))
game = Breakout(program)
game.run_game()

#screen = run_game(program)
#draw_screen(screen)

# n_blocks = sum(val == 2 for val in screen.values())
# print(f"There are {n_blocks} on screen at exit.")