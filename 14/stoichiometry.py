from typing import IO, List, Dict, Tuple, Deque
from collections import Counter
from math import ceil
import re


MaterialAmt = Tuple[str, int]
# resultant: (n_resultant, [(reactant, n_reactant), ...])
Reaction = Tuple[str, Tuple[int, List[MaterialAmt]]]
ReactionTable = Dict[str, Tuple[int, List[MaterialAmt]]] 


def read_reaction_file(f: IO) -> ReactionTable:
    table = {}
    for line in f:
        resultant, entry = parse_line(line)
        table[resultant] = entry
    return table

def parse_line(line: str) -> Reaction:
    matches = re.findall(r"\d+ \w+", line)
    parsed_matches = []
    for match in matches:
        n, chem = match.split(' ')
        parsed_matches.append((chem, int(n)))
    return parsed_matches[-1][0], (parsed_matches[-1][1], parsed_matches[:-1]) 

def ore_needed_for_fuel(table: ReactionTable) -> int:
    need = {'FUEL': 1}
    reserves = {}
    while set(need.keys()) != {'ORE'}:
        new_need = {}
        for chem_needed, n_chem_needed in need.items():
            if chem_needed == 'ORE':
                new_need['ORE'] = new_need.get('ORE', 0) + n_chem_needed
                continue
            n_from_reaction, reactants = table[chem_needed]    
            n_reactions_needed = ceil((n_chem_needed - reserves.get(chem_needed, 0)) / n_from_reaction)
            extra = n_reactions_needed * n_from_reaction - n_chem_needed
            reserves[chem_needed] = reserves.get(chem_needed, 0) + extra
            for reactant, n_reactant in reactants:
                new_need[reactant] = new_need.get(reactant, 0) + n_reactions_needed * n_reactant
        need = new_need
    return need.get('ORE')



table = read_reaction_file(open('./data/example1.txt', 'r'))
assert ore_needed_for_fuel(table) == 31 

table = read_reaction_file(open('./data/example2.txt', 'r'))
assert ore_needed_for_fuel(table) == 165 

table = read_reaction_file(open('./data/example3.txt', 'r'))
assert ore_needed_for_fuel(table) == 13312 

table = read_reaction_file(open('./data/example4.txt', 'r'))
assert ore_needed_for_fuel(table) == 180697 

table = read_reaction_file(open('./data/example5.txt', 'r'))
assert ore_needed_for_fuel(table) == 2210736 

table = read_reaction_file(open('./data/reactions.txt', 'r'))
print(f"The ore needed to make a FUEL is {ore_needed_for_fuel(table)}")