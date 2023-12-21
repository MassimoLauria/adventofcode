"""Advent of Code 2023 day 21
"""

from collections import deque,defaultdict


EXAMPLE = """...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........
"""

def printm(M):
    for x in M:
        print("".join(x))


def readdata(data=None):
    """Read and parse the input data"""
    if data is None:
       with open("input21.txt") as f:
            data = f.read()
    return [list(x) for x in data.splitlines()]

def part1(max_dist,data=None):
    """solve part 1"""
    M=readdata(data)
    R,C=len(M),len(M[0])
    sc = C // 2
    sr = R // 2
    Q=deque()
    Q.append((sr,sc))
    DIST={}
    DIST[sr,sc]=0
    while len(Q)>0:
        r,c = Q.popleft()
        if DIST[r,c]==max_dist:
            continue
        for dr,dc in [(+1,0),(-1,0),(0,1),(0,-1)]:
            nr,nc=r+dr,c+dc
            if nr<0 or nc<0 or nr>=R or nc>=C:
                continue
            if M[nr][nc]=='#' or (nr,nc) in DIST:
                continue
            DIST[nr,nc]=DIST[r,c]+1
            Q.append((nr,nc))
    even=0
    for r,c in DIST:
        if DIST[r,c]%2==0:
            even+=1
    print(even)

def part2(data=None):
    """solve part 2"""
    N=26501365
    M=readdata(data)
    R,C=len(M),len(M[0])
    sc = C // 2
    sr = R // 2

if __name__ == "__main__":
    part1(6,EXAMPLE)
    part1(64)
    part2(EXAMPLE)
