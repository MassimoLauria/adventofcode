"""Advent of Code 2023 day 23
"""
from collections import defaultdict,deque

EXAMPLE = """#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#"""



def readdata(data=None):
    """Read and parse the input data"""
    if data is None:
       with open("input23.txt") as f:
            data = f.read()
    return [list(x) for x in data.splitlines()]

def neighbours(M,v):
    neiga=[]
    r,c=v
    if M[r][c]==">":
        neiga.append((r,c+1))
    elif M[r][c]=="^":
        neiga.append((r-1,c))
    elif M[r][c]=="v":
        neiga.append((r+1,c))
    elif M[r][c]=="<":
        neiga.append((r,c-1))
    elif M[r][c]==".":
        neiga.append((r,c+1))
        neiga.append((r+1,c))
        neiga.append((r-1,c))
        neiga.append((r,c-1))
    final=[]
    for x,y in neiga:
        if x<0 or x>=len(M):
            continue
        if M[x][y]=='#':
            continue
        final.append((x,y))
    return final

def crawl_path(M,u,v,end):
    length=1
    prev=u
    cur=v
    while True:
        if cur==end:
            return cur,length
        ng = neighbours(M,cur)
        if prev in ng:
            ng.remove(prev)
        if len(ng)>1:
            return cur,length
        elif len(ng)==0:
            return None,0
        else:
            prev,cur=cur,ng[0]
            length+=1


def longest(G,W,u,end,visited=None):
    if u==end: return 0
    if visited is None: visited=set()
    visited.add(u)
    size=None
    for v in G[u]:
        if v in visited:continue
        t = longest(G,W,v,end,visited)
        if t is not None:
            if size is None: size=0
            size=max(size,t+W[u,v])
    visited.remove(u)
    return size

def create_graph(M):
    start=(0,1)
    end=(len(M)-1,len(M[0])-2)
    G=defaultdict(list)
    W={}
    Q=deque()
    Q.append(start)
    while len(Q)>0:
        u=Q.popleft()
        if u in G:
            continue
        for v in neighbours(M,u):
            w,dist=crawl_path(M,u,v,end)
            if w is None:
                continue
            G[u].append(w)
            W[u,w]=dist
            #print(u,f'--{dist}-->',w)
            if w not in G:
                Q.append(w)
    return G,W,start,end

def part1(data=None):
    """solve part 1"""
    M=readdata(data)
    G,W,start,end=create_graph(M)
    #print(G)
    print(longest(G,W,start,end))

def part2(data=None):
    """solve part 1"""
    M=readdata(data)
    for row in M:
        for j in range(len(row)):
            if row[j] in "><^v":
                row[j]='.'
    G,W,start,end=create_graph(M)
    print(longest(G,W,start,end))

if __name__ == "__main__":
    part1(EXAMPLE)
    part1()
    part2(EXAMPLE)
    part2()
