from typing import Tuple, List
from itertools import combinations
import math
import functools
import re

# TIL: Python has no built in sign.
sign = lambda x: 0 if x == 0 else math.copysign(1, x)


class Planet:

    def __init__(self, position: Tuple[int, int, int]):
        self.position = position
        self.velocity: Tuple[int, int, int] = (0, 0, 0)
    
    def update(self):
        self.position = tuple(x + v for x, v in zip(self.position, self.velocity))
    
    def apply_gravity(self, other: 'Planet'):
        self.velocity = tuple(
            v + sign(y - x) for v, x, y in zip(self.velocity, self.position, other.position)
        )
    
    def energy(self):
        return sum(abs(x) for x in self.position) * sum(abs(x) for x in self.velocity)
    
    @classmethod
    def from_string(cls, s: str) -> 'Planet':
        positions_str = s[1:-1].strip().split(', ')
        positions = tuple(int(re.match(r'.=\s*(-?\d+)', s).groups()[0]) for s in positions_str)
        return cls(positions)
    
    def __str__(self):
        return f'Planet{self.position}, v={self.velocity}'


def simulate(planets: List[Planet], n_steps: int=100) -> List[Planet]:
    for _ in range(n_steps):
        for p1, p2 in combinations(planets, r=2):
            p1.apply_gravity(p2)
            p2.apply_gravity(p1)
        for p in planets:
            p.update()

def find_period_for_axis(planets: List[Planet], axis: int) -> int:
    n = 0
    past = {}
    while True:
        state = tuple((p.position[axis], p.velocity[axis]) for p in planets)
        if state in past:
            return n
        past[state] = n
        for p1, p2 in combinations(planets, r=2):
            p1.apply_gravity(p2)
            p2.apply_gravity(p1)
        for p in planets:
            p.update()
        n += 1
        


s = open('./data/planets.txt', 'r')
planets = [Planet.from_string(row.strip()) for row in s]
simulate(planets, n_steps=1000)
print(f"The total enery is {sum(p.energy() for p in planets)}")


s = open('./data/planets.txt', 'r')
planets = [Planet.from_string(row.strip()) for row in s]
periods = tuple(find_period_for_axis(planets, i) for i in range(3))

lcm = lambda a, b: a * b // math.gcd(a, b)

print(f"The period of repition of the planetary system is {functools.reduce(lcm, periods)}")