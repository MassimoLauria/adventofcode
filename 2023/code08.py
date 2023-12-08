"""Advent of Code 2023 day 08
"""

import math

EXAMPLE1 = """LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)
"""

EXAMPLE2 = """LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)
"""

def readdata(data=None):
    """Read and parse the input data"""
    if data is None:
       with open("input08.txt") as f:
            data = f.read()
    lines=data.splitlines()
    directions=[0 if x=='L' else 1 for x in lines[0]]
    G = {}
    for i in range(2,len(lines)):
        a,l,r = lines[i][0:3],lines[i][7:10],lines[i][12:15]
        assert a not in G
        G[a] = (l,r)
    return directions,G

def part1(data=None):
    """solve part 1"""
    directions,G = readdata(data)
    pos = 'AAA'
    i=0
    while pos!='ZZZ':
        go = directions[i % len(directions)]
        pos = G[pos][go]
        i+=1
    print(i)

def part2(data=None):
    directions,G = readdata(data)



def until_Z(pos,directions,G):
    i=0
    while pos[2]!='Z':
        go = directions[i % len(directions)]
        pos = G[pos][go]
        i+=1
    return i


def part2(data=None):
    directions,G = readdata(data)
    starts = [x for x in G if x[2]=='A']
    arrivals = []
    for start in starts:
        i = until_Z(start,directions,G)
        arrivals.append(i)
    print(math.lcm(*arrivals))


if __name__ == "__main__":
    part1(EXAMPLE1)
    part1()
    part2(EXAMPLE2)
    part2()
