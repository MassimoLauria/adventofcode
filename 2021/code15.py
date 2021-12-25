from heapq import heapify,heappop,heappush
from itertools import product

example='''
1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581
'''


def parsedata(data=None):
    if data is None:
        with open("input15.txt") as f:
            data=f.read()
    M=[]
    for line in data.splitlines():
        if len(line)==0:
            continue
        M.append([int(c) for c in line])
    return M


def scalemap(M,h,v):
    R=len(M)
    C=len(M[0])
    N = [ [0]*(C*h) for _ in range(R*v) ]
    for i,j,r,c in product(range(v),range(h),range(R),range(C)):
        N[r+i*R][c+j*C] = (M[r][c] + i + j -1) % 9 + 1
    return N


def costmatrix(R,C,fill=float('inf')):
    M=[ [fill]*C for _ in range(R)]
    return M

def solve(density):
    R=len(density)
    C=len(density[0])
    cost=costmatrix(R,C)
    pq=[]
    heappush(pq,(0,0,0))
    cost[0][0]=0
    while len(pq)!=0:
        d,x,y = heappop(pq)
        if cost[y][x]<d:
            continue
        if x==C-1 and y==R-1:
            break
        for nx,ny in ((x+1,y),(x,y+1),(x,y-1),(x-1,y)):
            if nx<0 or nx>=C or ny<0 or ny>=R:
                continue
            newcost=density[ny][nx]+d
            if cost[ny][nx]>newcost:
                cost[ny][nx]=newcost
                heappush(pq,(newcost,nx,ny))

    print(cost[R-1][C-1])

if __name__ == "__main__":
    # part 1
    solve(parsedata(example))
    solve(parsedata())
    # part 2
    solve(scalemap(parsedata(example), 5, 5))
    solve(scalemap(parsedata(), 5, 5))
