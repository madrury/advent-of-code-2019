from typing import Dict, Tuple, List, Optional, Union
import numpy as np

Point = Tuple[int, int]

POSITION_CHAR = '@'
PATH_CHAR = '.'


def draw_map(
    map: Dict[Point, int], 
    draw_array: Union[List[str], Dict[int, str]],
    position: Optional[Point]=None, 
    path: Optional[List[Point]]=None) -> None:
    if not map:
        return
    minx = min(k[0] for k in map)
    maxx = max(k[0] for k in map)
    miny = min(k[1] for k in map)
    maxy = max(k[1] for k in map)
    area = np.zeros(shape=(maxx - minx + 1, maxy - miny + 1), dtype=int)
    area = np.zeros(shape=(50, 50), dtype=int)
    for (x, y), id in map.items():
        area[x - 25,  y - 25] = id
    strrep = draw_array[area]
    if position:
        strrep[(position[0] - 25, position[1] - 25)] = POSITION_CHAR
    if path:
        for p in path:
            strrep[p[0] - 25, p[1] - 25] = PATH_CHAR
    for row in strrep.T:
        print(''.join(row))