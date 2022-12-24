"""Advent of Code 2022 day 23
"""

from math import inf
from collections import defaultdict

EXAMPLE = """
....#..
..###.#
#...#.#
.#...##
#.###..
##.#.##
.#..#..
"""

EEXAMPLE="""
.....
..##.
..#..
.....
..##.
.....
"""

diam2d = [(-1, 0),(+1, 0),( 0,-1),( 0,+1)]
cube2d = [(+1, 0),(-1, 0),( 0,+1),( 0,-1),(+1,+1),(-1, -1),(-1,+1),(+1,-1)]

def readdata(data=None):
    """Read and parse the input data"""
    if data is None:
       with open("input23.txt") as f:
            data = f.read()
    rows = data.splitlines()
    if len(rows[-1])==0:
        rows.pop()
    if len(rows[0])==0:
        rows.pop(0)
    elf=0
    Map = {}
    Pos = []
    for i in range(len(rows)):
        for j in range(len(rows[i])):
            if rows[i][j]=="#":
                Map[i,j]=elf
                Pos.append((i,j))
                elf += 1
    return Map,Pos

def print_map(Map,Pos):
    elves_pos=set(Pos)
    r0,c0,r1,c1 = rectangle(Map)
    for i in range(r0,r1+1):
        for j in range(c0,c1+1):
            if (i,j) == (0,0):
                print("O",end="")
            elif (i,j) in elves_pos:
                print("#",end="")
            else:
                print(".",end="")
        print()



def rectangle(Map):
    r0,c0,r1,c1 = (+inf,+inf,-inf,-inf)
    for (i,j) in Map:
        r0 = min(i,r0)
        r1 = max(i,r1)
        c0 = min(j,c0)
        c1 = max(j,c1)
    return r0,c0,r1,c1

def make_one_round(M,P,R):
    elves_num = len(P)
    proposing = []
    for e in range(elves_num):
        er,ec = P[e]
        for dr,dc in cube2d:
            if (er+dr,ec+dc) in M:
                proposing.append(e)
                break
    # first half - move proposal
    Proposals = defaultdict(list)
    for e in proposing:
        er,ec = P[e]
        for p in range(R,R+4):
            dr,dc = diam2d[p % 4]
            if dr==0:
                test = [(er-1,ec+dc),(er,ec+dc),(er+1,ec+dc)]
            else:
                test = [(er+dr,ec-1),(er+dr,ec),(er+dr,ec+1)]
            if len([pos for pos in test if pos in M])==0:
                Proposals[(er+dr,ec+dc)].append(e)
                break
    # second half - move elves if no collision
    hasmoved=False
    for i,j in Proposals:
        if len(Proposals[i,j])==1:
            hasmoved=True
            e = Proposals[i,j][0]
            M.pop(P[e])
            M[i,j] = e
            P[e] = (i,j)
    return hasmoved

def part1(data=None):
    """solve part 1"""
    M,P = readdata(data)
    elves_num = len(P)
    for R in range(10):
        make_one_round(M,P,R)
    r0,c0,r1,c1 = rectangle(M)
    print("part1:",(r1-r0+1)*(c1-c0+1) - elves_num)

def part2(data=None):
    """solve part 1"""
    M,P = readdata(data)
    elves_num = len(P)
    R = 0
    while make_one_round(M,P,R):
        R +=1
    print("part2:",R+1)


if __name__ == "__main__":
    part1(EXAMPLE)
    part1()
    part2(EXAMPLE)
    part2()
