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
from collections import defaultdict

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


def part1(data=None):
    """solve part 1"""
    graph, pressures = readdata(data)
    print(graph)
    print(pressures)
    best_value=0
    curr_value=0
    available = sum(pressures.values())
    Open = set()
    path = ['AA']
    def branch():
        nonlocal best_value,path,curr_value,Open,graph
        pos = path[-1]
        rtime = 31-len(path)-len(Open)
        if rtime<=0:
            return curr_value
        # do not open
        for v in graph[pos]:
            path.append(v)
            best_value = max(best_value,branch())
            path.pop()
        # open (if possible)
        if pressures[pos]==0 or pos in Open:
            return best_value

        Open.add(pos)
        curr_value += pressures[pos]*(rtime-1)

        for v in graph[pos]:
            path.append(v)
            best_value = max(best_value,branch())
            path.pop()
        Open.remove(pos)
        return best_value
    print(branch())


if __name__ == "__main__":
    part1(EXAMPLE)
    # part1()
    # part2()
