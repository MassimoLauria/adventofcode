"""Advent of Code 2022 day 16
"""

EXAMPLE = """
Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II
"""

import networkx
import re
import math
import random
from time import time as clock
from collections import defaultdict, deque

def readdata(data=None):
    """Read and parse the input data"""
    if data is None:
       with open("input16.txt") as f:
            data = f.read()
    data=data.splitlines()
    G = defaultdict(list)
    P = {}
    for line in data:
        if len(line)==0: continue
        linfo = re.findall(r"\d+|[A-Z][A-Z]", line)
        G[linfo[0]].extend(linfo[2:])
        P[linfo[0]] = int(linfo[1])
    return G,P

def BFS(G,v):
    Q=deque()
    dist={ w:math.inf for w in G}
    dist[v]=0
    Q.append(v)
    while len(Q):
        x = Q.popleft()
        for y in G[x]:
            if dist[y]==math.inf:
                Q.append(y)
                dist[y] = dist[x]+1
    return dist

def process_graph(G,useful_nodes):
    D = {}
    for v in useful_nodes:
        dist = BFS(G,v)
        D[v] = { w: dist[w]+1 for w in useful_nodes if v!=w }
    return D

def part1(data=None):
    """solve part 1"""

    graph, pressures = readdata(data)
    useful_nodes = set(['AA']+[w for w in graph if pressures[w]>0])
    D = process_graph(graph,
                      useful_nodes)
    # never return to 'AA'
    assert pressures['AA']==0
    for v in D:
        D[v].pop('AA',1)

    best_value=0
    curr_value=0
    available = sum(pressures.values())
    endtime=30
    collected = set('AA')

    def branch(pos, time):

        nonlocal D
        nonlocal best_value,curr_value,collected
        nonlocal available

        # pos = curr_path[-1]
        #print(curr_value,curr_path,"against",best_value)
        #if curr_value>best_value:
        #    best_value,best_path = curr_value,curr_path[:]
        best_value = max(curr_value,best_value)

        # cut paths with no advantage
        if curr_value+available*(time-1) <= best_value:
            return

        # choose next to open
        options = []
        for npos in D[pos]:
            d = D[pos][npos]
            if npos in collected or d>=time:
                continue
            value = pressures[npos]*(time-d)
            options.append((value,npos))
        options.sort(reverse=True)
        for _,npos in options:

            d = D[pos][npos]

            if npos in collected or d>=time:
                continue

            collected.add(npos)
            curr_value += pressures[npos]*(time-d)
            available  -= pressures[npos]
            branch(npos, time-d)
            collected.remove(npos)
            curr_value -= pressures[npos]*(time-d)
            available  += pressures[npos]

    branch('AA', endtime)
    print("part1:", best_value)


def part2(data=None):
    """solve part 2"""

    graph, pressures = readdata(data)
    useful_nodes = set(['AA']+[w for w in graph if pressures[w]>0])
    D = process_graph(graph,useful_nodes)

    # never return to 'AA'
    assert pressures['AA']==0
    for v in D:
        D[v].pop('AA',1)

    curr_value=0
    best_value=0
    collected = set(['AA'])
    count=0
    path=[['AA'],['AA']]
    st = clock()

    def availablef(i,pos,time,collected):
        nonlocal D,pressures
        avail = 0
        for v in D:
            if v in collected:
                continue
            if i==0:
                avail += max(time-D[pos][v],26-D['AA'][v])*pressures[v]
            else:
                avail += (time-D[pos][v])*pressures[v]
        return avail

    def branch(i,pos,time):

        nonlocal D
        nonlocal best_value
        nonlocal curr_value,collected
        nonlocal count
        nonlocal path

        count+=1

        if curr_value>best_value:
            best_value = curr_value
            #print("Best {:4d} after {:10d} steps. [Clock: {}]".
            #    format(best_value,count,clock()-st))

        # cut paths with no possible gain
        if curr_value+availablef(i,pos,time,collected) <= best_value:
           return

        L = []
        for p in D[pos]:
            value = pressures[p]*(time-D[pos][p])
            if p not in collected and value>0:
                L.append( (value,D[pos][p],p) )

        L.sort(reverse=True)
        for value,d,npos in L:

            curr_value += value
            collected.add(npos)
            branch(i,npos,time-d)
            collected.remove(npos)
            curr_value -= value

        if i==0:
           branch(1,'AA',26)

    branch(0,'AA',26)
    print("part2:", best_value)





def part2alt(data=None):
    """solve part 2"""

    graph, pressures = readdata(data)
    useful_nodes = set(['AA']+[w for w in graph if pressures[w]>0])
    D = process_graph(graph,useful_nodes)

    # never return to 'AA'
    assert pressures['AA']==0
    for v in D:
        D[v].pop('AA',1)

    curr_value=0
    B = {x:1<<i for i,x in enumerate(v for v in pressures if pressures[v]>0) }
    halfjob={}

    def branch(pos,time,value,collected):

        nonlocal D
        halfjob[collected]= max(halfjob.get(collected,0),value)

        for npos in D[pos]:
            d = D[pos][npos]
            gain = pressures[npos]*(time-d)
            if B[npos] & collected or gain<=0:
                continue
            branch(npos,time-d, value+gain, collected | B[npos])

    branch('AA',26,0,0)
    print("part2alt:",
          max(v0+v1 for p0,v0 in halfjob.items()
                    for p1,v1 in halfjob.items()
                    if p0 & p1 ==0
                    ))

if __name__ == "__main__":
    part1(EXAMPLE)
    part1()
    part2(EXAMPLE)
    part2alt()
