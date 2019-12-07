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
    s = str(full_opcode)
    return int(s[-2:]), [int(c) for c in reversed(s[:-2])]

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
    parameter = lookup_parameter(program, parameters[0], parameter_modes[0])
    print(parameter)
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

PROGRAM = [
    3,225,
    1,225,6,6,
    1100,1,238,225,
    104,0,
    
    101,71,150,224,
    101,-123,224,224,
    4,224,
    
    102,8,223,223,101,2,224,224,1,224,223,223,2,205,209,224,1001,224,-3403,224,4,224,1002,223,8,223,101,1,224,224,1,223,224,223,1101,55,24,224,1001,224,-79,224,4,224,1002,223,8,223,101,1,224,224,1,223,224,223,1,153,218,224,1001,224,-109,224,4,224,1002,223,8,223,101,5,224,224,1,224,223,223,1002,201,72,224,1001,224,-2088,224,4,224,102,8,223,223,101,3,224,224,1,223,224,223,1102,70,29,225,102,5,214,224,101,-250,224,224,4,224,1002,223,8,223,1001,224,3,224,1,223,224,223,1101,12,52,225,1101,60,71,225,1001,123,41,224,1001,224,-111,224,4,224,102,8,223,223,1001,224,2,224,1,223,224,223,1102,78,66,224,1001,224,-5148,224,4,224,1002,223,8,223,1001,224,2,224,1,223,224,223,1101,29,77,225,1102,41,67,225,1102,83,32,225,1101,93,50,225,1102,53,49,225,4,223,99,0,0,0,677,0,0,0,0,0,0,0,0,0,0,0,1105,0,99999,1105,227,247,1105,1,99999,1005,227,99999,1005,0,256,1105,1,99999,1106,227,99999,1106,0,265,1105,1,99999,1006,0,99999,1006,227,274,1105,1,99999,1105,1,280,1105,1,99999,1,225,225,225,1101,294,0,0,105,1,0,1105,1,99999,1106,0,300,1105,1,99999,1,225,225,225,1101,314,0,0,106,0,0,1105,1,99999,1107,677,677,224,1002,223,2,223,1005,224,329,101,1,223,223,7,677,677,224,1002,223,2,223,1005,224,344,1001,223,1,223,7,226,677,224,102,2,223,223,1006,224,359,101,1,223,223,1108,226,226,224,1002,223,2,223,1005,224,374,1001,223,1,223,8,226,677,224,1002,223,2,223,1006,224,389,1001,223,1,223,1108,226,677,224,1002,223,2,223,1006,224,404,101,1,223,223,1107,677,226,224,102,2,223,223,1006,224,419,101,1,223,223,1007,677,677,224,1002,223,2,223,1005,224,434,101,1,223,223,7,677,226,224,102,2,223,223,1006,224,449,1001,223,1,223,1008,226,677,224,1002,223,2,223,1006,224,464,101,1,223,223,8,677,677,224,1002,223,2,223,1006,224,479,101,1,223,223,108,226,226,224,102,2,223,223,1005,224,494,101,1,223,223,1107,226,677,224,1002,223,2,223,1006,224,509,101,1,223,223,107,226,226,224,1002,223,2,223,1006,224,524,1001,223,1,223,107,677,677,224,1002,223,2,223,1005,224,539,101,1,223,223,1007,226,226,224,102,2,223,223,1006,224,554,101,1,223,223,108,677,677,224,102,2,223,223,1005,224,569,101,1,223,223,107,677,226,224,102,2,223,223,1005,224,584,101,1,223,223,1008,226,226,224,102,2,223,223,1006,224,599,101,1,223,223,1108,677,226,224,1002,223,2,223,1006,224,614,101,1,223,223,8,677,226,224,102,2,223,223,1005,224,629,1001,223,1,223,1008,677,677,224,102,2,223,223,1006,224,644,101,1,223,223,1007,226,677,224,102,2,223,223,1005,224,659,101,1,223,223,108,226,677,224,102,2,223,223,1006,224,674,101,1,223,223,4,223,99,226]

run(PROGRAM[:])