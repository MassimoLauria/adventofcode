"""Advent of Code 2023 day 16
"""

from collections import defaultdict
from collections import deque

EXAMPLE = r""".|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|....
"""

UP=0
LEFT=1
DOWN=2
RIGHT=3


def readdata(data=None):
    """Read and parse the input data"""
    if data is None:
       with open("input16.txt") as f:
            data = f.read()
    G=defaultdict(list)
    data=data.splitlines()
    R=len(data)
    C=len(data[0])
    # from left
    for r in range(R):
        for c in range(C):
            if data[r][c] in ".-" and c<(C-1):
                G[(r,c,LEFT)].append((r,c+1,LEFT))
            if data[r][c] in "/|" and r>0:
                G[(r,c,LEFT)].append((r-1,c,DOWN))
            if data[r][c] in "\\|" and r<(R-1):
                G[(r,c,LEFT)].append((r+1,c,UP))
    # from right
    for r in range(R):
        for c in range(C):
            if data[r][c] in ".-" and c>0 :
                G[(r,c,RIGHT)].append((r,c-1,RIGHT))
            if data[r][c] in "/|" and r<(R-1):
                G[(r,c,RIGHT)].append((r+1,c,UP))
            if data[r][c] in "\\|" and r>0:
                G[(r,c,RIGHT)].append((r-1,c,DOWN))
    # from up
    for r in range(R):
        for c in range(C):
            if data[r][c] in ".|" and r<(R-1):
                G[(r,c,UP)].append((r+1,c,UP))
            if data[r][c] in "/-" and c>0:
                G[(r,c,UP)].append((r,c-1,RIGHT))
            if data[r][c] in "\\-" and c<(C-1):
                G[(r,c,UP)].append((r,c+1,LEFT))
    # from down
    for r in range(R):
        for c in range(C):
            if data[r][c] in ".|"  and r>0:
                G[(r,c,DOWN)].append((r-1,c,DOWN))
            if data[r][c] in "/-" and c<(C-1):
                G[(r,c,DOWN)].append((r,c+1,LEFT))
            if data[r][c] in "\\-" and c>0:
                G[(r,c,DOWN)].append((r,c-1,RIGHT))
    return G,R,C

def BFS(G,start):
    seen = {start:True}
    Q = deque([start])
    while len(Q)>0:
        u = Q.popleft()
        for v in G[u]:
            if v not in seen:
                seen[v]=True
                Q.append(v)
    return seen


def part1(data=None):
    """solve part 1"""
    G,R,C=readdata(data)
    start=(0,0,LEFT)
    visited=BFS(G,start)
    touched={(r,c) for (r,c,d) in visited}
    #print(touched)
    print(len(touched))

def part2(data=None):
    """solve part 2"""
    G,R,C=readdata(data)
    max_touched=0
    starts=[]
    # starts
    for r in range(R):
        starts.append((r,0  ,LEFT ))
        starts.append((r,C-1,RIGHT))
    for c in range(C):
        starts.append((0  ,c  ,UP ))
        starts.append((R-1,0  ,DOWN))
    for start in starts:
        visited=BFS(G,start)
        touched={(r,c) for (r,c,d) in visited}
        if len(touched)>max_touched:
            max_touched = len(touched)
    print(max_touched)



if __name__ == "__main__":
    part1(EXAMPLE)
    part1()
    part2(EXAMPLE)
    part2()
