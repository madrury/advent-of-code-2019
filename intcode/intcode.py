from typing import Tuple, List, Optional

# You need to make relative opcode writes work.

# Constants
POSITION_MODE = 0
IMMEDIATE_MODE = 1
RELATIVE_MODE = 2

ADD_OP_CODE = 1
MULTIPLY_OP_CODE = 2
INPUT_OPCODE = 3
OUTPUT_OPCODE = 4
JUMP_IF_TRUE_OPCODE = 5
JUMP_IF_FALSE_OPCODE = 6
LESS_THAN_OPCODE = 7
EQUALS_OPCODE = 8
ADJUST_RELATIVE_BASE_OPCODE = 9
HALT_OP_CODE = 99


class Program:

    def __init__(self, code: List[int], input: Optional[List[int]]=None):
        self.code = code + [0] * 10000
        self.input = input if input else []
        self.output: List[int] = []
        self.instruction_ptr = 0
        self.relative_base = 0
    
    def __getitem__(self, idxr):
        return self.code[idxr]
    
    def __setitem__(self, idxr, val):
        self.code[idxr] = val
    
    def get_opcode(self):
        return self[self.instruction_ptr]


# Type Definitions
OpCode = int
OpcodeArity = int
OpCodeParameters = List[int]
OpCodeParameterModes = List[int]
InstructionPointer = int
DoHalt = bool
OpcodeReturn = Tuple[Program, DoHalt]


def run(program: Program) -> Program:
    halt = False
    output = []
    while not halt:
        program, halt = run_until_output(program)
        output.extend(program.output)
        program.output = []
    # Restore the output.
    program.output = output
    return program

def run_until_output(program: Program) -> Tuple[Program, bool]:
    halt = False
    while not (halt or program.output):
        full_opcode = program.get_opcode()
        opcode, parameter_modes = parse_opcode(full_opcode)
        operation, n_parameters = OP_CODE_TABLE[opcode]
        # Add imferred parameter modes of zero.
        if len(parameter_modes) != n_parameters:
            parameter_modes = parameter_modes + [0]*(n_parameters - len(parameter_modes))
        parameters = program[
            program.instruction_ptr + 1 : program.instruction_ptr + n_parameters + 1]
        program, halt = operation(program, parameters, parameter_modes)
    return program, halt


def parse_opcode(full_opcode: OpCode) -> Tuple[OpCode, OpCodeParameterModes]:
    s = str(full_opcode)
    return int(s[-2:]), [int(c) for c in reversed(s[:-2])]

def lookup_parameters(
    program: Program, 
    parameters: OpCodeParameters, 
    parameter_modes: OpCodeParameterModes) -> OpCodeParameters:
    return [
        lookup_parameter(program, parameter, mode)
        for parameter, mode in zip(parameters, parameter_modes)
    ]

def lookup_parameter(program: Program, parameter: int, mode: int) -> int:
    if mode == POSITION_MODE:
        return program[parameter]
    elif mode == IMMEDIATE_MODE:
        return parameter
    elif mode == RELATIVE_MODE:
        return program[program.relative_base + parameter]
    else:
        raise ValueError(f"Unknown parameter mode {mode}.")

def write_to_memory(program: Program, value: int, parameter: int, mode: int) -> None:
    if mode == POSITION_MODE:
        program[parameter] = value
    elif mode == RELATIVE_MODE:
        program[program.relative_base + parameter] = value
    else:
        raise ValueError(f"Cannot write with parameter mode {mode}")

# TODO: Make this a decorator.
def increase_instruction_pointer(program: Program, parameters: List[int]) -> None:
    program.instruction_ptr += len(parameters) + 1


# Opcde Implementations.
def add(
    program: Program, 
    parameters: OpCodeParameters, 
    parameter_modes: OpCodeParameterModes) -> OpcodeReturn:
    a1, a2 = lookup_parameters(program, parameters[:2], parameter_modes[:2])
    write_to_memory(program, a1 + a2, parameters[2], parameter_modes[2])
    increase_instruction_pointer(program, parameters)
    return program, False

def multiply(
    program: Program, 
    parameters: OpCodeParameters, 
    parameter_modes: OpCodeParameterModes) -> OpcodeReturn:
    m1, m2 = lookup_parameters(program, parameters[:2], parameter_modes[:2])
    write_to_memory(program, m1 * m2, parameters[2], parameter_modes[2])
    increase_instruction_pointer(program, parameters)
    return program, False

def input_(
    program: Program, 
    parameters: OpCodeParameters, 
    parameter_modes: OpCodeParameterModes) -> OpcodeReturn:
    value = program.input.pop()
    write_to_memory(program, value, parameters[0], parameter_modes[0])
    increase_instruction_pointer(program, parameters)
    return program, False

def output(
    program: Program, 
    parameters: OpCodeParameters, 
    parameter_modes: OpCodeParameterModes) -> OpcodeReturn:
    parameter = lookup_parameter(program, parameters[0], parameter_modes[0])
    program.output.append(parameter)
    increase_instruction_pointer(program, parameters)
    return program, False

def jump_if_true(
    program: Program, 
    parameters: OpCodeParameters, 
    parameter_modes: OpCodeParameterModes) -> OpcodeReturn:
    condition, address = lookup_parameters(program, parameters, parameter_modes)
    if condition:
        program.instruction_ptr = address
    else:
        increase_instruction_pointer(program, parameters)
    return program, False

def jump_if_false(
    program: Program, 
    parameters: OpCodeParameters, 
    parameter_modes: OpCodeParameterModes) -> OpcodeReturn:
    condition, address = lookup_parameters(program, parameters, parameter_modes)
    if not condition:
        program.instruction_ptr = address
    else:
        increase_instruction_pointer(program, parameters)
    return program, False

def less_than(
    program: Program, 
    parameters: OpCodeParameters, 
    parameter_modes: OpCodeParameterModes) -> OpcodeReturn:
    a, b = lookup_parameters(program, parameters[:2], parameter_modes[:2])
    write_to_memory(program, int(a < b), parameters[2], parameter_modes[2])
    increase_instruction_pointer(program, parameters)
    return program, False 

def equals(
    program: Program, 
    parameters: OpCodeParameters, 
    parameter_modes: OpCodeParameterModes) -> OpcodeReturn:
    a, b = lookup_parameters(program, parameters[:2], parameter_modes[:2])
    write_to_memory(program, int(a == b), parameters[2], parameter_modes[2])
    increase_instruction_pointer(program, parameters)
    return program, False 
    
def adjust_relative_base(
    program: Program, 
    parameters: OpCodeParameters, 
    parameter_modes: OpCodeParameterModes) -> OpcodeReturn:
    a = lookup_parameter(program, parameters[0], parameter_modes[0])
    program.relative_base += a
    increase_instruction_pointer(program, parameters)
    return program, False 

def halt(
    program: Program, 
    parameters: OpCodeParameters, 
    parameter_modes: OpCodeParameterModes) -> OpcodeReturn:
    return program, True


OP_CODE_TABLE = {
    ADD_OP_CODE: (add, 3),
    MULTIPLY_OP_CODE: (multiply, 3),
    INPUT_OPCODE: (input_, 1),
    OUTPUT_OPCODE: (output, 1),
    JUMP_IF_TRUE_OPCODE: (jump_if_true, 2),
    JUMP_IF_FALSE_OPCODE: (jump_if_false, 2),
    LESS_THAN_OPCODE: (less_than, 3),
    EQUALS_OPCODE: (equals, 3),
    ADJUST_RELATIVE_BASE_OPCODE: (adjust_relative_base, 1),
    HALT_OP_CODE: (halt, 0)
}