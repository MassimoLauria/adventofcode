from collections import defaultdict

example="""
aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out
"""

example2="""
svr: aaa bbb
aaa: fft
fft: ccc
bbb: tty
tty: ccc
ccc: ddd eee
ddd: hub
hub: fff
eee: dac
dac: fff
fff: ggg hhh
ggg: out
hhh: out
"""


def DFS(G,v,visit=None,time=0):
    if visit is None:
        visit={}
        time =0
    assert(v not in visit)
    visit[v] = [time,None]
    time+=1
    for nextv in G[v]:
        if nextv not in visit:
            DFS(G,nextv,visit,time)
            time = visit[nextv][1]+1
    visit[v][1] = time
    return visit

def toposort(G,base=None):
    visit = DFS(G,base)
    R=[(-visit[v][1],v) for v in visit]
    R.sort()
    R=[v for (t,v) in R]
    return R


def parse_graph(text):
    V={}
    for line in text.strip().splitlines():
        v, edges = line.split(":")
        edges = edges.split()
        V[v] = edges
    assert('out' not in V)
    V['out']=[]
    return V

def part1(text):
    G = parse_graph(text)
    S = toposort(G,"you")
    P = defaultdict(int)
    P['you']=1
    for v in S:
        for u in G[v]:
            P[u]+=P[v]
    return P['out']


def paths(G,S,points):
    inds =[S.index(p) for p in points]
    pathnum=1
    for i in range(len(inds)-1):
        st=S[inds[i]]
        en=S[inds[i+1]]
        M=defaultdict(int)
        M[st]=1
        for i in range(inds[i],inds[i+1]):
            v = S[i]
            for u in G[v]:
                M[u] += M[v]
        pathnum *= M[en]
    return pathnum

def part2(text):
    G = parse_graph(text)
    S = toposort(G,'svr')
    return paths(G,S,['svr','fft','dac','out'])


if __name__ == "__main__":
    print("Part1 example  :",part1(example))
    with open("input11.txt") as f:
        text=f.read()
    print("Part1 challenge:",part1(text))
    print("Part2 example  :",part2(example2))
    with open("input11.txt") as f:
        text=f.read()
    print("Part2 challenge:",part2(text))
