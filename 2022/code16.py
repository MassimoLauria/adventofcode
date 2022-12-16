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

import re
import math
import random
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
    useful_nodes = set([w for w in graph if pressures[w]>0])
    useful_nodes.add('AA')

    D = process_graph(graph,
                      useful_nodes)

    # never return to 'AA'
    if pressures['AA']==0:
        for v in D:
            if 'AA' in D[v]:
                D[v].pop('AA')

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
    useful_nodes = set([w for w in graph if pressures[w]>0])
    useful_nodes.add('AA')

    D = process_graph(graph,
                      useful_nodes)
    # never return to 'AA'
    if pressures['AA']==0:
        for v in D:
            if 'AA' in D[v]:
                D[v].pop('AA')
    best_value=0
    curr_value=0
    available = sum(pressures.values())
    collected = set(['AA'])
    p0,p1=[],[]

    def availablef(pos,time,collected):
        nonlocal D,pressures
        avail = 0
        for v in D:
            if v in collected:
                continue
            avail += max( (time[0]-D[pos[0]][v])*pressures[v],
                          (time[1]-D[pos[1]][v])*pressures[v] )
        return avail

    def branch(pos,time):

        nonlocal D
        nonlocal best_value
        nonlocal curr_value,collected
        nonlocal available
        nonlocal p0,p1


        #print(pos,time,curr_value)
        #print(p0,p1)

        if curr_value>best_value:
            best_value = max(curr_value,best_value)


        # cut paths with no advantage
        if curr_value+availablef(pos,time,collected) <= best_value:
            return

        # choose next to open
        # g = []
        # for i in [0,1]:
        #     for npos in D[pos[i]]:
        #         if npos in collected or D[pos[i]][npos]>=time[i]:
        #             continue
        #         g.append((i,npos))
        for npos in D:

            if npos in collected or npos=="AA":
                continue

            d = D[pos[0]][npos]
            if time[0]>d:
                curr_value += pressures[npos]*(time[0]-d)
                collected.add(npos)
                p0.append(npos)
                branch((npos,pos[1]), (time[0]-d,time[1]) )
                collected.remove(npos)
                p0.pop()
                curr_value -= pressures[npos]*(time[0]-d)

            d = D[pos[1]][npos]
            if time[1]>d:
                curr_value += pressures[npos]*(time[1]-d)
                p1.append(npos)
                collected.add(npos)
                branch((pos[0],npos), (time[0],time[1]-d) )
                collected.remove(npos)
                p1.pop()
                curr_value -= pressures[npos]*(time[1]-d)

    branch(['AA','AA'], [26,26])
    print("part2:", best_value)


if __name__ == "__main__":
    part1(EXAMPLE)
    part1()
    part2(EXAMPLE)
    part2()
