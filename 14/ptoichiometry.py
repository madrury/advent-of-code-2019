from typing import IO, List, Dict, Tuple, Deque
from collections import Counter
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

def backtrack_to_ore(table: ReactionTable) -> Tuple[str, int]:
    d = {} 
    have_checked = set()
    fuel_parents = table['FUEL'][1]
    d.update(fuel_parents)
    while not only_ore(d):
        print(d)
        resultant = list(d.keys())[0]
        n_resultants_have = d.pop(resultant)
        if resultant == 'ORE':
            d['ORE'] = d.get('ORE', 0) + n_resultants_have
            have_checked.add('ORE')
            continue
        n_resultants_need, reactants = table[resultant]
        if n_resultants_have < n_resultants_need:
            if resultant not in have_checked:
                d[resultant] = d.get(resultant, 0) + n_resultants_have
                have_checked.add(resultant)
                continue
            # Weve checked everything and there's nothing to trade, so force a trade with some leftovers.
            else:
                d[resultant] = d.get(resultant, 0) + n_resultants_need
                have_checked = set()
                continue
        else:
            n_resultants_have = n_resultants_have - n_resultants_need
            if n_resultants_have > 0:
                d[resultant] = d.get(resultant, 0) + n_resultants_have
            for r, nr in reactants:
                d[r] = d.get(r, 0) + nr
            have_checked = set()
    return d 
         
def only_ore(d: Counter) -> bool:
    return all(r == 'ORE' for r, _ in d.items())


# print(parse_line('2 AB, 3 BC, 4 CA => 1 FUEL'))
table = read_reaction_file(open('./data/example3.txt', 'r'))
print(table)
print()
print(backtrack_to_ore(table))