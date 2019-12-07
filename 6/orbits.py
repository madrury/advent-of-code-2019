from typing import Optional, List, Dict, Set, Iterator, IO


class Orbit:

    def __init__(
        self, planet: str, children: Optional[List['Orbit']] = None) -> None:
        self.planet = planet
        self.children: List['Orbit'] = children if children else []
        self.parents: List['Orbit'] = []
    
    def append(self, orbit: 'Orbit') -> None:
        orbit.parents.append(self)
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
    
    def find_minimum_transfter_path(
        self, target: 'Orbit', all_orbits: Set['Orbit']) -> List['Orbit']:
        # Dijkstra's algorithm.
        all_orbits = all_orbits.copy() 
        distances: Dict['Orbit', int] = {o: 10**10 for o in all_orbits}
        previous: Dict['Orbit', 'Orbit'] = {}
        distances[self] = 0
        while all_orbits:
            min_distance_orbit = min(
                {o: dist for o, dist in distances.items() if o in all_orbits},
                 key=distances.get)
            all_orbits.remove(min_distance_orbit)
            if min_distance_orbit == target:
                break
            for nbr in min_distance_orbit.parents + min_distance_orbit.children:
                alt_distance = distances[min_distance_orbit] + 1
                if alt_distance < distances[nbr]:
                    distances[nbr] = alt_distance
                    previous[nbr] = min_distance_orbit
        # Now walk backwards from the target to find the path.        
        path: List['Orbit'] = []
        current = target
        while current != self:
            if previous[current]:
                path.append(current)
                current = previous[current]
        path.append(self)
        return path





        # print(current_path)
        # if not current_path:
        #     current_path = []
        # if self == target:
        #     return current_path + [target]
        # else:
        #     return o.find_minimum_transfter_path(target=target, current_path=current_path + [self])
        #                for o in self.children + self.parents if o not in current_path


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

you, santa = orbits['YOU'], orbits['SAN']
path = you.find_minimum_transfter_path(santa, all_orbits=set(orbits.values()))
# Watch out for fencepost errors.
print(f"The length of the minimal transfer path is {len(path) - 3}")