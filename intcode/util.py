from typing import Dict, Tuple, List, Optional, Union
import numpy as np

Point = Tuple[int, int]

POSITION_CHAR = '@'
PATH_CHAR = '.'


def draw_map(
    map: Dict[Point, int], 
    conversion_table: Union[List[str], Dict[int, str]],
    position: Optional[Point]=None, 
    path: Optional[List[Point]]=None) -> None:
    if not map:
        return
    minx = min(k[0] for k in map)
    maxx = max(k[0] for k in map)
    miny = min(k[1] for k in map)
    maxy = max(k[1] for k in map)
    area = np.zeros(shape=(maxx - minx + 1, maxy - miny + 1), dtype=int)
    for (x, y), id in map.items():
        area[x - minx,  y - miny] = id
    strrep = conversion_table[area]
    if position:
        strrep[(position[0] - minx, position[1] - miny)] = POSITION_CHAR
    if path:
        for p in path:
            strrep[p[0] - minx, p[1] - miny] = PATH_CHAR
    for row in strrep.T:
        print(''.join(row))


def draw_array(
    arr: Union[List[int], np.array],
    conversion_table: Union[List[str], Dict[int, str]]) -> None:
    arr = np.asarray(arr)
    if isinstance(conversion_table, dict):
        conversion_table = np.array([conversion_table[i] for i in range(256)])
    strrep = conversion_table[arr]
    for row in strrep:
        print(''.join(row))