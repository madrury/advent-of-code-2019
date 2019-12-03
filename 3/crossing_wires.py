from typing import Iterable, Tuple, List

def create_path(program: str, start=(0, 0)) -> List[Tuple[int, int]]:
    p = compile_to_tuples(program)
    path = [start]
    for instruction in p:
        path.append(process_instruction(instruction, start=path[-1]))
    return path

def process_instruction(instruction: Tuple[str, int], start: Tuple[int, int]) -> List[Tuple[int, int]]:
    opcode, value = instruction
    if opcode == 'R':
        return [(start[0] + i + 1, start[0]) for i in range(value)]
    elif opcode == 'L':
        return [(start[0] - i - 1, start[0]) for i in range(value)]
    elif opcode == 'U':
        return [(start[0], start[1] + i + 1) for i in range(value)]
    elif opcode == 'D':
        return [(start[0], start[1] - i - 1) for i in range(value)]
    else:
        raise ValueError(f"Opcode {opcode} unknown.")
    

def compile_to_tuples(program: str) -> Iterable[Tuple[str, int]]:
    instructions = program.split(',')
    for instruction in instructions:
        yield instruction[0], int(instruction[1:])

assert list(compile_to_tuples("R75,D30,R83,U83")) == [("R", 75), ("D", 30), ("R", 83), ("U", 83)]
assert process_instruction(('U', 5), start=(0, 0)) == [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5)]
