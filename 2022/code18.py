"""Advent of Code 2022 day 18
"""

from itertools import product
from collections import deque

EXAMPLE = """
2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5
"""

def readdata(data=None):
    """Read and parse the input data"""
    if data is None:
       with open("input18.txt") as f:
            data = f.read()
    L = []
    for line in data.split():
        x,y,z = line.split(',')
        yield (int(x),int(y),int(z))

def cube(x,y,z):
    return ( (x+dx,y+dy,z+dz) for dx,dy,dz in product([-1,0,1],repeat=3) )

def diamond(x,y,z):
    yield (x+1,y,z)
    yield (x-1,y,z)
    yield (x,y+1,z)
    yield (x,y-1,z)
    yield (x,y,z+1)
    yield (x,y,z-1)


def part1(data=None):
    """solve part 1"""
    D = set(readdata(data))
    thin_surface=set()
    surface=0
    for x,y,z in D:
        for t in diamond(x,y,z):
            surface += 1 if t not in D else 0
    print("part1:", surface)


def part2(data=None):
    """solve part 2"""
    lava = set(readdata(data))
    # build the border
    border = set( b for t in lava for b in cube(*t))
    border.difference_update(lava)
    start =  min(border, key=lambda t: t[0])
    # BFS from start
    external=set([start])
    Q = deque([start])
    while len(Q)>0:
        p = Q.popleft()
        for q in diamond(*p):
            if q in border and q not in external:
                external.add(q)
                Q.append(q)
    # external surface
    surface = [ 1 for b in lava for t in diamond(*b)  if t in external]
    print("part2:",len(surface))

if __name__ == "__main__":
    part1(EXAMPLE)
    part1()
    part2(EXAMPLE)
    part2()
