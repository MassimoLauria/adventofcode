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

def printm(M,dist=None):
    R,C=len(M),len(M[0])
    for i in range(R):
        for j in range(C):
            if dist is not None and (i,j) in dist:
                print(dist[i,j]%10,end="")
            else:
                print(M[i][j],end="")
        print()


def tile(P,rows,cols):
    R,C=len(P),len(P[0])
    M=[]
    for i in range(rows*R):
        M.append( P[i%R]*cols )
    return M

def readdata(data=None):
    """Read and parse the input data"""
    if data is None:
       with open("input21.txt") as f:
            data = f.read()
    M = [list(x) for x in data.splitlines()]
    sr,sc=len(M)//2,len(M[0])//2
    M[sr][sc]='.'
    return M

def bfs(M,start,radius=None):
    R,C=len(M),len(M[0])
    sr,sc = start
    Q=deque()
    Q.append((sr,sc))
    DIST={}
    DIST[sr,sc]=0
    while len(Q)>0:
        r,c = Q.popleft()
        for dr,dc in [(+1,0),(-1,0),(0,1),(0,-1)]:
            nr,nc=r+dr,c+dc
            if nr<0 or nc<0 or nr>=R or nc>=C:
                continue
            if M[nr][nc]=='#' or (nr,nc) in DIST:
                continue
            DIST[nr,nc]=DIST[r,c]+1
            if radius is None or DIST[nr,nc]<radius:
                Q.append((nr,nc))
    return DIST

def part1(radius,data=None):
    """solve part 1"""
    M=readdata(data)
    start = len(M)//2,len(M[0])//2
    DIST=bfs(M,start,radius)
    even=0
    for r,c in DIST:
        if DIST[r,c]%2==0:
            even+=1
    print(even)

def part2(data=None):
    """solve part 2"""
    N=26501365
    M=readdata(data)
    assert len(M)==len(M[0])
    rR=13
    rC=1
    M2=tile(M,rR,rC)
    R,C=len(M),len(M[0])
    sc = (rC*C) // 2
    sr = (rR*R) // 2
    dist=bfs(M2,(sr,sc))
    printm(M2)
    print(dist)
    check_dist(M2,dist,R,C)
    list_dist(M2,dist,R,C)

def list_dist(M,dist,R,C):
    repR=len(M)/R
    repC=len(M[0])/C
    assert repR%2==1
    assert repC%2==1
    distlist=defaultdict(list)
    for i in range(len(M)):
        for j in range(len(M[0])):
            if M[i][j]=='#': continue
            if (i,j) not in dist: continue
            distlist[i%R,j%C].append(dist[i,j])
    print('blah')
    for i in range(R):
        for j in range(C):
            if M[i][j]=='#': continue
            if (i,j) not in distlist: continue
            print((i,j),":",distlist[i,j])

def check_dist(M,dist,R,C):
    repR=len(M)/R
    repC=len(M[0])/C
    assert repR%2==1
    assert repC%2==1
    lookR=+1
    lookC=+1
    for i in range(len(M)):
        for j in range(len(M[0])):
            if M[i][j]=='#': continue
            if (i,j) not in dist: continue
            bi,bj=i//R,j//C
            if bi<(repR//2)-1: lookR=+1
            elif bi>(repR//2)+1: lookR=-1
            elif bi==repR//2:
                continue
            else:
                lookR=0
            if bj<(repC//2)-1: lookC=+1
            elif bj>(repC//2)+1: lookC=-1
            elif bj==repC//2:
                continue
            else:
                lookC=0
            assert dist[i,j]==dist[i+R*lookR,j]+R*abs(lookR)
            assert dist[i,j]==dist[i,j+C*lookC]+C*abs(lookC)




if __name__ == "__main__":
    part1(6,EXAMPLE)
    part1(64)
    part2(EXAMPLE)
    part2()
