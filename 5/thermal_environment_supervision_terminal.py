from typing import Tuple, List

POSITION_MODE = 0
IMMEDIATE_MODE = 1

ADD_OP_CODE = 1
MULTIPLY_OP_CODE = 2
INPUT_OPCODE = 3
OUTPUT_OPCODE = 4
HALT_OP_CODE = 99

def run(program: List[int]) -> List[int]:
    instruction_ptr = 0
    halt = False
    while not halt:
        full_opcode = program[instruction_ptr]
        opcode, parameter_modes = parse_opcode(full_opcode)
        operation, n_parameters = OP_CODE_TABLE[opcode]
        if len(parameter_modes) != n_parameters:
            parameter_modes = parameter_modes + [0]*(n_parameters - len(parameter_modes))
        parameters = program[instruction_ptr + 1 : instruction_ptr + n_parameters + 1]
        program, halt = operation(
            program, parameters, parameter_modes, instruction_ptr)
        instruction_ptr += n_parameters + 1
    return program

def parse_opcode(full_opcode: int) -> Tuple[int, List[int]]:
    s = ''.join(reversed(str(full_opcode)))
    return int(s[:2]), [int(c) for c in s[2:]]

def lookup_parameter(program: List[int], parameter: int, mode: int) -> int:
    if mode == POSITION_MODE:
        return program[parameter]
    elif mode == IMMEDIATE_MODE:
        return parameter
    else:
        raise ValueError(f"Unknown parameter mode {mode}.")

# Opcde Implementations.

def add(
    program: List[int], 
    parameters: List[int], 
    parameter_modes: List[int], 
    current_position: int) -> Tuple[List[int], bool]:
    a1, a2 = [
        lookup_parameter(program, parameter, mode)
        for parameter, mode in zip(parameters[:2], parameter_modes[:2])
    ]
    address = parameters[2]
    program[address] = a1 + a2
    return program, False

def multiply(
    program: List[int], 
    parameters: List[int], 
    parameter_modes: List[int], 
    current_position: int) -> Tuple[List[int], bool]:
    m1, m2 = [
        lookup_parameter(program, parameter, mode)
        for parameter, mode in zip(parameters[:2], parameter_modes[:2])
    ]
    address = parameters[2]
    program[address] = m1 * m2
    return program, False

def input_(
    program: List[int], 
    parameters: List[int], 
    parameter_modes: List[int], 
    current_position: int) -> Tuple[List[int], bool]:
    val = int(input('> '))
    program[parameters[0]] = val
    return program, False

def output(
    program: List[int], 
    parameters: List[int], 
    parameter_modes: List[int], 
    current_position: int) -> Tuple[List[int], bool]:
    print(program[parameters[0]])
    return program, False
    
def halt(
    program: List[int], 
    parameters: List[int], 
    parameter_modes: List[int], 
    current_position: int) -> Tuple[List[int], bool]:
    return program, True


OP_CODE_TABLE = {
    ADD_OP_CODE: (add, 3),
    MULTIPLY_OP_CODE: (multiply, 3),
    INPUT_OPCODE: (input_, 1),
    OUTPUT_OPCODE: (output, 1),
    HALT_OP_CODE: (halt, 0)
}


assert run([1,0,0,0,99]) == [2,0,0,0,99]
assert run([2,3,0,3,99]) == [2,3,0,6,99]
assert run([2,4,4,5,99,0]) == [2,4,4,5,99,9801]
assert run([1,1,1,4,99,5,6,0,99]) == [30,1,1,4,2,5,6,0,99]
assert run([1,9,10,3,2,3,11,0,99,30,40,50]) == [3500,9,10,70,2,3,11,0,99,30,40,50]