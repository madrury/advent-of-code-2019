from intcode.intcode import Program, run_until_output, run
from intcode.util import draw_array
import numpy as np

from itertools import product
from typing import List, Dict, Tuple, Iterable
Point = Tuple[int, int]


CONVERSION_DICT = {i: chr(i) for i in range(256)}
SCAFFOLD, EMPTY_SPACE, LINE_END = 35, 46, 10
# This is localy what an intersection of scaffolds looks like.
INTERSECTION_MASK = np.array([[46, 35, 46], [35, 35, 35], [46, 35, 46]])


def to_square(output: List[int]) -> np.array:
    '''Transpose the program output into a rectangular array.

    Note:
      - We chop off the final column since that contains all newlines.
      - The end out the output contains TWO newlines, so we remove one
        before reshaping.
    '''
    row_len = output.index(LINE_END)
    return np.array(output[:-1]).reshape(-1, row_len + 1)[:, :-1]


def iter_intersections(console: np.array) -> Iterable[Point]:
    xsh, ysh = console.shape
    for x, y in product(range(1, xsh - 1), range(1, ysh - 1)):
        if np.all(console[x-1:x+2, y-1:y+2] == INTERSECTION_MASK):
            yield x, y


program = Program.from_file(open('./data/ascii.txt', 'r'))

run(program)
console_out = to_square(program.output)
#draw_array(console_out, conversion_table=CONVERSION_DICT)
total_alignment_parameter = sum(x * y for x, y in iter_intersections(console_out))
print(f"The total allignment parameter is {total_alignment_parameter}")