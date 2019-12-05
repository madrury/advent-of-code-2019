from typing import Iterable, Tuple, List, Set, Dict

def create_path(program: str, start: Tuple[(int, int)] = (0, 0)) -> List[Tuple[int, int]]:
    p = compile_to_tuples(program)
    path = [start]
    for instruction in p:
        path.extend(process_instruction(instruction, start=path[-1]))
    return path[1:]

def compile_to_tuples(program: str) -> Iterable[Tuple[str, int]]:
    instructions = program.split(',')
    for instruction in instructions:
        yield instruction[0], int(instruction[1:])

def process_instruction(
    instruction: Tuple[str, int], start: Tuple[int, int]) -> List[Tuple[int, int]]:
    opcode, value = instruction
    if opcode == 'R':
        return [(start[0] + i + 1, start[1]) for i in range(value)]
    elif opcode == 'L':
        return [(start[0] - i - 1, start[1]) for i in range(value)]
    elif opcode == 'U':
        return [(start[0], start[1] + i + 1) for i in range(value)]
    elif opcode == 'D':
        return [(start[0], start[1] - i - 1) for i in range(value)]
    else:
        raise ValueError(f"Opcode {opcode} unknown.")
    
def get_intersection_points(program_1: str, program_2: str) -> Set[Tuple[int, int]]:
    path_1, path_2 = create_path(program_1), create_path(program_2)
    return set(path_1) & set(path_2)

def wire_distance_to_intersection_points(
    program_1: str, program_2: str) -> Tuple[Dict[Tuple[int, int], int], Dict[Tuple[int, int], int]]:
    path_1, path_2 = create_path(program_1), create_path(program_2)
    intersections = set(path_1) & set(path_2)
    distance_lookup_1 = {point: n for n, point in enumerate(path_1, start=1)
                                   if point in intersections}
    distance_lookup_2 = {point: n for n, point in enumerate(path_2, start=1)
                                   if point in intersections}
    return distance_lookup_1, distance_lookup_2

def manhattan_norm(t: Tuple[int, int]) -> int:
    return abs(t[0]) + abs(t[1])

def min_manhattan_norm(program_1: str, program_2: str) -> int:
    return min(manhattan_norm(t) for t in get_intersection_points(program_1, program_2)) 

def min_wire_distance(program_1: str, program_2: str) -> int:
    distance_lookup_1, distance_lookup_2 = wire_distance_to_intersection_points(
        program_1, program_2)
    distance_lookup = {
        point: distance_lookup_1[point] + distance_lookup_2[point]
        for point in distance_lookup_1}
    return min(distance_lookup.values())


assert list(compile_to_tuples("R75,D30,R83,U83")) == [("R", 75), ("D", 30), ("R", 83), ("U", 83)]
assert process_instruction(('U', 5), start=(0, 0)) == [(0, 1), (0, 2), (0, 3), (0, 4), (0, 5)]
assert process_instruction(('D', 5), start=(0, 0)) == [(0, -1), (0, -2), (0, -3), (0, -4), (0, -5)]
assert process_instruction(('R', 5), start=(0, 0)) == [(1, 0), (2, 0), (3, 0), (4, 0), (5, 0)]
assert process_instruction(('L', 5), start=(0, 0)) == [(-1, 0), (-2, 0), (-3, 0), (-4, 0), (-5, 0)]
assert get_intersection_points("R8,U5,L5,D3", "U7,R6,D4,L4") == {(3, 3), (6, 5)}
assert min_manhattan_norm("R75,D30,R83,U83,L12,D49,R71,U7,L72",
                          "U62,R66,U55,R34,D71,R55,D58,R83") == 159
assert min_manhattan_norm("R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51",
                          "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7") == 135

with open('./data/program.txt', 'r') as f:
    program_1, program_2 = f.readline(), f.readline()

distance = min_manhattan_norm(program_1, program_2)
print(f"The minimum manhattan distance to an intersection is {distance}.")

distance = min_wire_distance(program_1, program_2)
print(f"The minimum wire distance to an intersection is {distance}.")