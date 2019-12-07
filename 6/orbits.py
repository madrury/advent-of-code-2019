from typing import Optional, List, Dict, Set, Iterator, IO

class Orbit:

    def __init__(
        self, planet: str, children: Optional[List['Orbit']] = None) -> None:
        self.planet = planet
        self.children: List['Orbit'] = children if children else []
        # self.parents: List['Orbit'] = []
    
    def append(self, orbit: 'Orbit') -> None:
        # orbit.parents.append(self)
        self.children.append(orbit)
    
    def __iter__(self) -> Iterator['Orbit']:
        yield from self.children
    
    def __hash__(self) -> int:
        return hash(self.planet)
    
    def __repr__(self) -> str:
        return f"Orbit{self.planet}"
    
    def count_descendents(self, already_counted: Optional[Set[str]] = None) -> int:
        if not already_counted:
            already_counted = set()
        already_counted.add(self.planet)
        if self.children == []:
            return 0
        else:
            return (
                len([o for o in self.children if o.planet not in already_counted]) 
                + sum(
                    o.count_descendents(
                        already_counted=already_counted) for o in self.children))

    
def from_file(f: IO) -> Dict[str, Orbit]:
    planets: Dict[str, Orbit] = {}
    for line in f:
        parent, child = line.strip().split(")")
        if child not in planets:
           orbit_child = Orbit(planet=child)
           planets[child] = orbit_child
        else:
           orbit_child = planets[child]
        if parent not in planets: 
            orbit_parent = Orbit(planet=parent)
            planets[parent] = orbit_parent
        else:
           orbit_parent = planets[parent]
        orbit_parent.append(orbit_child)
    return planets

orbits = from_file(open('./data/input.txt', 'r'))
# parentless_orbits = [o for o in orbits.values() if not o.parents]
# print(f"Parentless orbits:\n    {parentless_orbits}")
s = sum(o.count_descendents() for o in orbits.values())
print(f"The total number of orbital relations is {s}")