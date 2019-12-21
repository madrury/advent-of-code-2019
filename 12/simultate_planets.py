from typing import Tuple, List
import re


class Planet:

    def __init__(self, position: Tuple[int, int, int]):
        self.position = position
        self.valocity: Tuple[int, int, int] = (0, 0, 0)
    
    @classmethod
    def from_string(cls, s: str) -> 'Planet':
        positions_str = s[1:-1].strip().split(', ')
        positions = tuple(int(re.match(r'.=\s*(-?\d+)', s).groups()[0]) for s in positions_str)
        return cls(positions)
    
    def __str__(self):
        return f'Planet{self.position}'

s = '<x=2, y=  5, z= -22>'
print(Planet.from_string(s))