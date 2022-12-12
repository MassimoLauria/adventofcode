"""Advent of Code 2022 day 12
"""
from collections import deque
from pprint import pprint

EXAMPLE = """
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
"""

def readdata(data=None):
    """Read and parse the input data"""
    if data is None:
        with open("input12.txt") as f:
            data = f.read()
    M = []
    for line in data.splitlines():
        if len(line)==0:
            continue
        M.append(list(line))
    s,e=None,None
    for i in range(len(M)):
        for j in range(len(M[i])):
            if M[i][j]=='S':
                s = (i,j)
                M[i][j] = 'a'
            if M[i][j]=='E':
                e = (i,j)
                M[i][j] = 'z'
    return M,s,e


def creatematrix(R,C,fill):
    return [[fill]*C for _ in range(R)]

def part1(data=None):
    """solve part 1"""
    M,s,e = readdata(data)
    #pprint(M)
    #print(s,e)
    W=len(M)
    H=len(M[0])
    INF=W*H+1
    D = creatematrix(W,H,INF)
    D[s[0]][s[1]] = 0
    Q = deque()
    Q.append(s)
    while len(Q)>0:
        x,y = Q.popleft()
        d = D[x][y]
        # print("Deque",x,y,"at dist",d)
        if (x,y) == e:
            break
        for dx,dy in [(-1,0),(+1,0),(0,-1),(0,+1)]:
            nx,ny = x+dx,y+dy
            if not (0 <= nx < W):
                continue
            if not (0 <= ny < H):
                continue
            if D[nx][ny]==INF and ord(M[nx][ny])<=ord(M[x][y])+1:
                D[nx][ny] = d+1
                Q.append((nx,ny))
                # print("reach",nx,ny,"at dist",d+1)
    # pprint(D)
    print("part1:",d)


def part2(data=None):
    """solve part 2"""
    M,_,e = readdata(data)
    #pprint(M)
    #print(s,e)
    W=len(M)
    H=len(M[0])
    INF=W*H+1
    D = creatematrix(W,H,INF)
    Q = deque()
    for i in range(W):
        for j in range(H):
            if M[i][j]=='a':
                D[i][j] = 0
                Q.append((i,j))
    while len(Q)>0:
        x,y = Q.popleft()
        d = D[x][y]
        # print("Deque",x,y,"at dist",d)
        if (x,y) == e:
            break
        for dx,dy in [(-1,0),(+1,0),(0,-1),(0,+1)]:
            nx,ny = x+dx,y+dy
            if not (0 <= nx < W):
                continue
            if not (0 <= ny < H):
                continue
            if D[nx][ny]==INF and ord(M[nx][ny])<=ord(M[x][y])+1:
                D[nx][ny] = d+1
                Q.append((nx,ny))
                # print("reach",nx,ny,"at dist",d+1)
    # pprint(D)
    print("part2:",d)



if __name__ == "__main__":
    part1(EXAMPLE)
    part1()
    part2(EXAMPLE)
    part2()
