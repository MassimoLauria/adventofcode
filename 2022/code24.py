"""Advent of Code 2022 day 24
"""

from collections import deque

EXAMPLE = """
#.######
#>>.<^<#
#.<..<<#
#>v.><>#
#<^v^^>#
######.#
"""

WINDS = { '>' :(0,+1), '<' :(0,-1), '^' :(-1,0), 'v' :(+1,0) }
DIAM  = [ (1,0),(-1,0),(0,1),(0,-1)]


def safe(grid,i,j,t):
    H,W = len(grid),len(grid[0])

    if i==-1 and j==0: return True
    if i==H and j==W-1: return True

    if i<0 or i>=H: return False
    if j<0 or j>=W: return False
    if grid[(i-t) % H ][j] == "v": return False
    if grid[(i+t) % H ][j] == "^": return False
    if grid[i][(j-t) % W ] == ">": return False
    if grid[i][(j+t) % W ] == "<": return False
    return True


def readdata(data=None):
    """Read and parse the input data"""
    if data is None:
       with open("input24.txt") as f:
            data = f.read()
    data=data.splitlines()
    if len(data[-1])==0: data.pop()
    if len(data[0])==0: data.pop(0)
    H=len(data)-2
    W=len(data[0])-2
    G = [ [ "." for _ in range(W) ] for _ in range(H) ]
    for i in range(H):
        for j in range(W):
            G[i][j] = data[i+1][j+1]
    return G

def reaching(start,end,G,tstart=0):
    if start==end:
        return tstart
    Q = deque([(start[0],start[1],tstart)])
    V = set([(start[0],start[1],tstart)])
    while len(Q)>0:
        i,j,t = Q.popleft()
        for di,dj in [ (0,0),(1,0),(-1,0),(0,1),(0,-1)]:
            p = (i+di,j+dj,t+1)
            if safe(G,*p) and p not in V:
                if p[:2]==end: return p[2]
                V.add(p)
                Q.append(p)

def part1(data=None):
    """solve part 1"""
    G = readdata(data)
    H,W = len(G),len(G[0])
    start = (-1,0)
    end   = (H,W-1)
    t = reaching(start,end,G)
    print("part1:",t)

def part2(data=None):
    """solve part 2"""
    G = readdata(data)
    H,W = len(G),len(G[0])
    start = (-1,0)
    end   = (H,W-1)
    t1 = reaching(start,end,G)
    t2 = reaching(end,start,G,t1)
    t3 = reaching(start,end,G,t2)
    print("part2:",t3)

if __name__ == "__main__":
    part1(EXAMPLE)
    part1()
    part2(EXAMPLE)
    part2()
