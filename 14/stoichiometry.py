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

def ore_needed_for_fuel(table: ReactionTable, n_fuel: int=1) -> int:
    need = {'FUEL': n_fuel}
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
    return need['ORE']

def amount_of_fuel_for_ore(table: ReactionTable, n_ore: int=1_000_000_000_000) -> int:
    from time import sleep
    low, high = 0, n_ore
    while low != high:
        try_n_fuel = (low + high + 1) // 2
        ore_needed = ore_needed_for_fuel(table, try_n_fuel)
        if ore_needed < n_ore:
            low = try_n_fuel
        elif ore_needed > n_ore:
            high = try_n_fuel - 1
        else:
            return try_n_fuel
    return low

# 82892754 82892753

# table = read_reaction_file(open('./data/example1.txt', 'r'))
# assert ore_needed_for_fuel(table) == 31 

# table = read_reaction_file(open('./data/example2.txt', 'r'))
# assert ore_needed_for_fuel(table) == 165 


table = read_reaction_file(open('./data/example3.txt', 'r'))
assert ore_needed_for_fuel(table) == 13312 
assert amount_of_fuel_for_ore(table, n_ore=1_000_000_000_000) == 82892753

table = read_reaction_file(open('./data/example4.txt', 'r'))
assert ore_needed_for_fuel(table) == 180697 
assert amount_of_fuel_for_ore(table, n_ore=1_000_000_000_000) == 5586022

table = read_reaction_file(open('./data/example5.txt', 'r'))
assert ore_needed_for_fuel(table) == 2210736 
assert amount_of_fuel_for_ore(table, n_ore=1_000_000_000_000) == 460664

table = read_reaction_file(open('./data/reactions.txt', 'r'))
print(f"The ore needed to make a FUEL is {ore_needed_for_fuel(table)}")
print(f"The fuel makable for 1trillion ORE is {amount_of_fuel_for_ore(table)}")