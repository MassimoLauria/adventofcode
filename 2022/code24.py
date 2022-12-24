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

class grid:
    def __init__(self,H,W):
        assert H>0 and W>0
        self._M = [ [ list() for _ in range(W)] for _ in range(H) ]
        self._H = H
        self._W = W

    def size(self):
        return self._H,self._W

    def print(self):
        W = self._W
        print("#."+'#'*W)
        for l in self._M:
            print('#',end='')
            for v in l:
                if len(v)==0:
                    print('.',end='')
                elif len(v)==1:
                    print(v[0],end='')
                else:
                    print(len(v),end='')
            print('#')
        print('#'*W+".#")

    def forward(self,steps=1):
        H,W = self.size()
        new = grid(H,W)
        for i in range(H):
            for j in range(W):
                for w in self._M[i][j]:
                    di,dj = WINDS[w]
                    new._M[(i+steps*di) % H][(j+steps*dj) % W].append(w)
        return new

    def copy(self):
        H,W = self.size()
        new = grid(H,W)
        for i in range(H):
            for j in range(W):
                new[i,j].extend(self._M[i][j])
        return new

    def safe(self,i,j):

        if i==-1 and j==0: return True
        if i==self._H and j==self._W-1: return True

        if i<0 or i>=self._H: return False
        if j<0 or j>=self._W: return False
        return len(self._M[i][j])==0

    def __getitem__(self,pair):
        i,j = pair
        return self._M[i][j]

    def __setitem__(self,pair,value):
        i,j = pair
        self._M[i][j] = value


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
    G = grid(H,W)
    for i in range(H):
        for j in range(W):
            v = data[i+1][j+1]
            if v == ".": continue
            assert v in WINDS
            G[i,j].append(v)
    return G

def reaching(start,end,G):
    Q = deque([(start[0],start[1],0)])
    V = set()
    t_grid = 0
    reached = [(start[0],start[1],0)]
    while len(Q)>0:
        i,j,t = Q.popleft()
        if (i,j)==end:
            break
        assert t == t_grid or t==t_grid-1
        if t_grid == t:
            G = G.forward()
            t_grid += 1
            #print("Another grid",t_grid)
            #G.print()
        if G.safe(i,j):
            Q.append((i,j,t_grid))
        for di,dj in DIAM:
            if G.safe(i+di,j+dj) and (i+di,j+dj,t_grid) not in V:
                V.add((i+di,j+dj,t_grid))
                Q.append((i+di,j+dj,t_grid))
    return t


def part1(data=None):
    """solve part 1"""
    G = readdata(data)
    H,W = G.size()
    start = (-1,0)
    end   = (H,W-1)
    t = reaching(start,end,G)
    print("part1:",t)

def part2(data=None):
    """solve part 2"""
    G0 = readdata(data)
    H,W = G0.size()
    start = (-1,0)
    end   = (H,W-1)
    path1 = reaching(start,end,G0)
    G1    = G0.forward(path1)
    path2 = reaching(end,start,G1)
    G2    = G1.forward(path2)
    path3 = reaching(start,end,G2)
    print("part2:",path1+path2+path3)

if __name__ == "__main__":
    part1(EXAMPLE)
    part1()
    part2(EXAMPLE)
    part2()
