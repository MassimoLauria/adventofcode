"""Advent of Code 2023 day 21

I am stupid. I did not check that the input has no obstacle on the row
and column of the start point. The map has no obstacle on borders
either, but that I noticed and used. """

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


def part2examples(data=None):
    """solve part 1"""
    M=readdata(data)
    o = len(M)//2
    for rad in [6,10,50,100,500]:
        DIST=bfs(M,(o,o),box='inf',radius=rad)
        even=0
        for r,c in DIST:
            if DIST[r,c]%2==rad%2:
                even+=1
        print(rad,even)

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
    assert len(M)==len(M[0])
    return M

def bfs(M,start,box=None,radius=None):
    side=len(M)
    if box is None:
        box=(0,0,1,1)
    if box!='inf':
        top,left,bottom,right=[i*side for i in box]
    else:
        top=left=bottom=right=None
    #assert top<=0 and left<=0 and bottom>=1 and right>=1
    sr,sc = start
    Q=deque()
    Q.append((sr,sc))
    DIST={}
    DIST[sr,sc]=0
    while len(Q)>0:
        r,c = Q.popleft()
        for dr,dc in [(+1,0),(-1,0),(0,1),(0,-1)]:
            nr,nc=r+dr,c+dc
            if box!='inf' and (nr<top or nc<left or nr>=bottom or nc>=right):
                continue
            if M[nr%side][nc%side]=='#' or (nr,nc) in DIST:
                continue
            if radius is None or DIST[r,c]<radius:
                DIST[nr,nc]=DIST[r,c]+1
                Q.append((nr,nc))
    return DIST

def part1(radius,data=None):
    """solve part 1"""
    M=readdata(data)
    o = len(M)//2
    DIST=bfs(M,(o,o),radius=radius)
    even=0
    for r,c in DIST:
        if DIST[r,c]%2==radius%2:
            even+=1
    print(even)

class pairinfo:
    def __init__(self):
        self.reach=False
        self.here=None
        self.tl=None
        self.bl=None
        self.tr=None
        self.br=None
        self.tchain=None
        self.bchain=None
        self.lchain=None
        self.rchain=None

def load_pair_info(M):
    """solve part 2"""
    side=len(M)
    o=side//2
    lookahead=5
    dist=bfs(M,(o,o),[-1,-1,2,2])
    pairdata={}
    # corners
    for i in range(side):
        for j in range(side):
            pairdata[i,j]=pairinfo()
            pairdata[i,j].reach=(i,j) in dist
            if not pairdata[i,j].reach: continue
            pairdata[i,j].here=dist[i,j]
            pairdata[i,j].tl=dist[i-side,j-side]
            pairdata[i,j].tr=dist[i-side,j+side]
            pairdata[i,j].bl=dist[i+side,j-side]
            pairdata[i,j].br=dist[i+side,j+side]
    # above
    dist=bfs(M,(o,o),[-lookahead+1,0,1,1])
    for i in range(side):
        for j in range(side):
            if not pairdata[i,j].reach: continue
            pairdata[i,j].tchain=[dist[i-k*side,j] for k in range(1,lookahead)]
    # below
    dist=bfs(M,(o,o),[0,0,lookahead,1])
    for i in range(side):
        for j in range(side):
            if not pairdata[i,j].reach: continue
            pairdata[i,j].bchain=[dist[i+k*side,j] for k in range(1,lookahead)]
    # left
    dist=bfs(M,(o,o),[0,-lookahead+1,1,1])
    for i in range(side):
        for j in range(side):
            if not pairdata[i,j].reach: continue
            pairdata[i,j].lchain=[dist[i,j-k*side] for k in range(1,lookahead)]
    # right
    dist=bfs(M,(o,o),[0,0,1,lookahead])
    for i in range(side):
        for j in range(side):
            if not pairdata[i,j].reach: continue
            pairdata[i,j].rchain=[dist[i,j+k*side] for k in range(1,lookahead)]
    return pairdata

def count_corner(dist,side,radius):
    layers=(radius-dist)//side
    if (radius-dist)%2==0 and layers>=0:
        t = layers//2
        return (t+1) + (t+1)*t
    elif (radius-dist)%2==1 and layers>0:
        t = (layers-1)//2
        return 2*(t+1) + (t+1)*t
    else:
        return 0

def count_chain(chain,side,radius):
    if chain is None:
        return 0
    assert len(chain)>3
    assert chain[-1]==chain[-2]+side
    assert side%2==1
    cchain=chain[:]
    if (radius-cchain[-1])%2!=0:
        cchain.append(cchain[-1]+side)
    if cchain[-1]<=radius:
        return (len(cchain)+1)//2 + (radius-cchain[-1])//(2*side)
    else:
        res=0
        for x in chain:
            if x<=radius and (radius-x)%2==0:
                res+=1
        return res

def part2(N,data=None):
    """solve part 2"""
    M=readdata(data)
    pairdata = load_pair_info(M)
    total = 0
    side=len(M)
    #DIST=bfs(M,(side//2,side//2),box='inf',radius=N)
    #atotal=0
    # for i,j in DIST:
    #     if DIST[i,j]%2==N%2:
    #         atotal+=1
    for i in range(side):
        for j in range(side):
            if not pairdata[i,j].reach:
                continue
            if pairdata[i,j].here%2 == N%2 and pairdata[i,j].here<=N:
                total+=1
            total += count_corner(pairdata[i,j].tl,side,N)
            total += count_corner(pairdata[i,j].bl,side,N)
            total += count_corner(pairdata[i,j].tr,side,N)
            total += count_corner(pairdata[i,j].br,side,N)
            total += count_chain(pairdata[i,j].tchain,side,N)
            total += count_chain(pairdata[i,j].lchain,side,N)
            total += count_chain(pairdata[i,j].rchain,side,N)
            total += count_chain(pairdata[i,j].bchain,side,N)
    print(total)

if __name__ == "__main__":
    #part1(6,EXAMPLE)
    part1(64)
    # part2examples(EXAMPLE)
    # part2(6,EXAMPLE)
    # part2(10,EXAMPLE)
    # part2(50,EXAMPLE)
    # part2(100,EXAMPLE)
    # part2(500,EXAMPLE)
    # part2(1000,EXAMPLE)
    # part2(5000,EXAMPLE)
    part2(26501365)
