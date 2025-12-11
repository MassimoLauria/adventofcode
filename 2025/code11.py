
from collections import defaultdict

def DFS(G,v=None):
    visit={}
    time=0;
    if v is None:
        explore = G
    else:
        explore = [v]
    for v in explore:
        if v not in visit:
            time=DFS_r(G,v,visit,time)
    return visit

def DFS_r(G,v,visit,time):
    assert(v not in visit)
    visit[v] = [time,None]
    time+=1
    for nextv in G[v]:
        if nextv not in visit:
            time = DFS_r(G,nextv,visit,time)
        elif visit[nextv][1] is None:
            raise ValueError("Ciclic!!!",v,visit)
    visit[v][1] = time
    return time+1

def toposort(G,base=None):
    visit = DFS(G,base)
    R=[(-visit[v][1],v) for v in visit]
    R.sort()
    R=[v for (t,v) in R]
    return R

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

def part2(text):
    G = parse_graph(text)
    S = toposort(G,'svr')
    P={
        ""   : defaultdict(int),
        "d"  : defaultdict(int),
        "f"  : defaultdict(int),
        "df" : defaultdict(int)
    }
    P[""]['svr']=1
    for v in S:
        for u in G[v]:
            if u == "dac":
                P[""][u] = 0
                P["f"][u] = 0
                P["d"][u] += P[""][v] + P["d"][v]
                P["df"][u] += P["f"][v] + P["df"][v]
            elif u == "fft":
                P[""][u] = 0
                P["d"][u] = 0
                P["f"][u] += P[""][v] + P["f"][v]
                P["df"][u] += P["d"][v] + P["df"][v]
            else:
                P[""][u] += P[""][v]
                P["d"][u] += P["d"][v]
                P["f"][u] += P["f"][v]
                P["df"][u] += P["df"][v]
    return P["df"]['out']


if __name__ == "__main__":
    print("Part1 example  :",part1(example))
    with open("input11.txt") as f:
        text=f.read()
    print("Part1 challenge:",part1(text))
    print("Part2 example  :",part2(example2))
    with open("input11.txt") as f:
        text=f.read()
    print("Part2 challenge:",part2(text))
