from itertools import product

def run(program):
    current_position = 0
    halt = False
    while not halt:
        op_code = OP_CODES[program[current_position]]
        program, halt = op_code(program, current_position)
        current_position += 4
    return program

def run_with_noun_and_verb(program, noun, verb):
    program[1], program[2] = noun, verb
    program = run(program)
    return program[0]

def add(program, current_position):
    idx_1, idx_2 = program[current_position + 1], program[current_position + 2]
    summand_1, summand_2 = program[idx_1], program[idx_2]
    register = program[current_position + 3]
    program[register] = summand_1 + summand_2
    return program, False

def multiply(program, current_position):
    idx_1, idx_2 = program[current_position + 1], program[current_position + 2]
    multiplicand_1, multiplicand_2 = program[idx_1], program[idx_2]
    register = program[current_position + 3]
    program[register] = multiplicand_1 * multiplicand_2
    return program, False

def halt(program, current_position):
    return program, True

OP_CODES ={
    1: add,
    2: multiply,
    99: halt
}

assert run([1,0,0,0,99]) == [2,0,0,0,99]
assert run([2,3,0,3,99]) == [2,3,0,6,99]
assert run([2,4,4,5,99,0]) == [2,4,4,5,99,9801]
assert run([1,1,1,4,99,5,6,0,99]) == [30,1,1,4,2,5,6,0,99]
assert run([1,9,10,3,2,3,11,0,99,30,40,50]) == [3500,9,10,70,2,3,11,0,99,30,40,50]

# Input copied from problem.
PROGRAM = [1,0,0,3,1,1,2,3,1,3,4,3,1,5,0,3,2,1,10,19,1,19,5,23,2,23,9,27,1,5,27,31,1,9,31,35,1,35,10,39,2,13,39,43,1,43,9,47,1,47,9,51,1,6,51,55,1,13,55,59,1,59,13,63,1,13,63,67,1,6,67,71,1,71,13,75,2,10,75,79,1,13,79,83,1,83,10,87,2,9,87,91,1,6,91,95,1,9,95,99,2,99,10,103,1,103,5,107,2,6,107,111,1,111,6,115,1,9,115,119,1,9,119,123,2,10,123,127,1,127,5,131,2,6,131,135,1,135,5,139,1,9,139,143,2,143,13,147,1,9,147,151,1,151,2,155,1,9,155,0,99,2,0,14,0]

# Restore the 1202 alarm state.

print(f"The value at position zero is: {run_with_noun_and_verb(PROGRAM[:], 12, 2)}")

# The output we are searching for.
NEEDLE = 19690720

# Note that the role of noun and verb are interchangable since both possible
# opperations are commutative.
for noun, verb in product(range(100), range(100)):
    result = run_with_noun_and_verb(PROGRAM[:], noun, verb)
    if result == NEEDLE:
        break

print(f"The desired inputs are {noun}, {verb}")