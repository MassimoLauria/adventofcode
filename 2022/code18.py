"""Advent of Code 2022 day 18
"""

from itertools import product

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
    print(surface)


def part2(data=None):
    """solve part 2"""
    D = set(readdata(data))
    border=set()
    start=D.pop()
    D.add(start)
    for x,y,z in D:
        if x<start[0]:
            start = x,y,z
        for b in cube(x,y,z):
            if b not in D:
                border.add(b)
    start=start[0]-1,start[1],start[2]
    assert start in border



if __name__ == "__main__":
    part1(EXAMPLE)
    part1()
    part2(EXAMPLE)
