from intcode.intcode import Program, run_until_output, run
from intcode.util import draw_array

from typing import List, Dict, Tuple

CONVERSION_DICT = {i: chr(i) for i in range(256)}

program = Program.from_file(open('./data/ascii.txt', 'r'))

run(program)
draw_array(program.output, conversion_table=CONVERSION_DICT)