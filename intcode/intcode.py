from typing import Tuple, List, Optional


# Constants
POSITION_MODE = 0
IMMEDIATE_MODE = 1

ADD_OP_CODE = 1
MULTIPLY_OP_CODE = 2
INPUT_OPCODE = 3
OUTPUT_OPCODE = 4
JUMP_IF_TRUE_OPCODE = 5
JUMP_IF_FALSE_OPCODE = 6
LESS_THAN_OPCODE = 7
EQUALS_OPCODE = 8
HALT_OP_CODE = 99


class Program:

    def __init__(self, code: List[int], input: Optional[List[int]]):
        self.code = code
        self.input = input if input else []
        self.output = []
    
    def __getitem__(self, idxr):
        return self.code[idxr]
    
    def __setitem__(self, idxr, val):
        self.code[idxr] = val


# Type Definitions
OpCode = int
OpcodeArity = int
OpCodeParameters = List[int]
OpCodeParameterModes = List[int]
InstructionPointer = int
DoHalt = bool
OpcodeReturn = Tuple[Program, InstructionPointer, DoHalt]


def run(program: Program) -> Program:
    instruction_ptr = 0
    halt = False
    while not halt:
        full_opcode = program[instruction_ptr]
        opcode, parameter_modes = parse_opcode(full_opcode)
        operation, n_parameters = OP_CODE_TABLE[opcode]
        # Add imferred parameter modes of zero.
        if len(parameter_modes) != n_parameters:
            parameter_modes = parameter_modes + [0]*(n_parameters - len(parameter_modes))
        parameters = program[instruction_ptr + 1 : instruction_ptr + n_parameters + 1]
        program, instruction_ptr, halt = operation(
            program, parameters, parameter_modes, instruction_ptr)
    return program

def parse_opcode(full_opcode: OpCode) -> Tuple[OpCode, OpCodeParameterModes]:
    s = str(full_opcode)
    return int(s[-2:]), [int(c) for c in reversed(s[:-2])]

def lookup_parameter(program: Program, parameter: int, mode: int) -> int:
    if mode == POSITION_MODE:
        return program[parameter]
    elif mode == IMMEDIATE_MODE:
        return parameter
    else:
        raise ValueError(f"Unknown parameter mode {mode}.")

def lookup_parameters(
    program: Program, 
    parameters: OpCodeParameters, 
    parameter_modes: OpCodeParameterModes) -> OpCodeParameters:
    return [
        lookup_parameter(program, parameter, mode)
        for parameter, mode in zip(parameters, parameter_modes)
    ]


# Opcde Implementations.
def add(
    program: Program, 
    parameters: OpCodeParameters, 
    parameter_modes: OpCodeParameterModes, 
    instruction_ptr: int) -> OpcodeReturn:
    a1, a2 = lookup_parameters(program, parameters[:2], parameter_modes[:2])
    address = parameters[2]
    program[address] = a1 + a2
    return program, instruction_ptr + len(parameters) + 1, False

def multiply(
    program: Program, 
    parameters: OpCodeParameters, 
    parameter_modes: OpCodeParameterModes, 
    instruction_ptr: int) -> OpcodeReturn:
    m1, m2 = lookup_parameters(program, parameters[:2], parameter_modes[:2])
    address = parameters[2]
    program[address] = m1 * m2
    return program, instruction_ptr + len(parameters) + 1, False

def input_(
    program: Program, 
    parameters: OpCodeParameters, 
    parameter_modes: OpCodeParameterModes, 
    instruction_ptr: int) -> OpcodeReturn:
    val = program.input.pop()
    program[parameters[0]] = val
    return program, instruction_ptr + len(parameters) + 1, False

def output(
    program: Program, 
    parameters: OpCodeParameters, 
    parameter_modes: OpCodeParameterModes, 
    instruction_ptr: int) -> OpcodeReturn:
    parameter = lookup_parameter(program, parameters[0], parameter_modes[0])
    program.output.append(parameter)
    return program, instruction_ptr + len(parameters) + 1, False

def jump_if_true(
    program: Program, 
    parameters: OpCodeParameters, 
    parameter_modes: OpCodeParameterModes, 
    instruction_ptr: int) -> OpcodeReturn:
    condition, address = lookup_parameters(program, parameters, parameter_modes)
    if condition:
        instruction_ptr = address
    else:
        instruction_ptr += len(parameters) + 1
    return program, instruction_ptr, False

def jump_if_false(
    program: Program, 
    parameters: OpCodeParameters, 
    parameter_modes: OpCodeParameterModes, 
    instruction_ptr: int) -> OpcodeReturn:
    condition, address = lookup_parameters(program, parameters, parameter_modes)
    if not condition:
        instruction_ptr = address
    else:
        instruction_ptr += len(parameters) + 1
    return program, instruction_ptr, False

def less_than(
    program: Program, 
    parameters: OpCodeParameters, 
    parameter_modes: OpCodeParameterModes, 
    instruction_ptr: int) -> OpcodeReturn:
    a, b = lookup_parameters(program, parameters[:2], parameter_modes[:2])
    address = parameters[2]
    program[address] = int(a < b)
    return program, instruction_ptr + len(parameters) + 1, False 

def equals(
    program: Program, 
    parameters: OpCodeParameters, 
    parameter_modes: OpCodeParameterModes, 
    instruction_ptr: int) -> OpcodeReturn:
    a, b = lookup_parameters(program, parameters[:2], parameter_modes[:2])
    address = parameters[2]
    program[address] = int(a == b)
    return program, instruction_ptr + len(parameters) + 1, False 
    
def halt(
    program: Program, 
    parameters: OpCodeParameters, 
    parameter_modes: OpCodeParameterModes, 
    instruction_ptr: int) -> OpcodeReturn:
    return program, instruction_ptr, True


OP_CODE_TABLE = {
    ADD_OP_CODE: (add, 3),
    MULTIPLY_OP_CODE: (multiply, 3),
    INPUT_OPCODE: (input_, 1),
    OUTPUT_OPCODE: (output, 1),
    JUMP_IF_TRUE_OPCODE: (jump_if_true, 2),
    JUMP_IF_FALSE_OPCODE: (jump_if_false, 2),
    LESS_THAN_OPCODE: (less_than, 3),
    EQUALS_OPCODE: (equals, 3),
    HALT_OP_CODE: (halt, 0)
}