"""Advent of Code 2023 day 25
"""

import math
from collections import defaultdict
from random import randint

EXAMPLE = """jqt: rhn xhk nvd
rsh: frs pzl lsr
xhk: hfx
cmg: qnr nvd lhk bvb
rhn: xhk bvb hfx
bvb: xhk hfx
pzl: lsr hfx nvd
qnr: nvd
ntq: jqt hfx bvb xhk
nvd: lhk
lsr: lhk
rzs: qnr cmg lsr rsh
frs: qnr lhk lsr
"""

import networkx as nx
from networkx.algorithms.flow.maxflow import minimum_cut

def readdata(data=None):
    """Read and parse the input data"""
    if data is None:
        with open("input25.txt") as f:
            data = f.read()
    G = nx.Graph()
    for line in data.splitlines():
        line=line.split()
        u=line[0][:-1]
        for v in line[1:]:
            G.add_edge(u,v,capacity=1.0)
    return G

def part1(data=None):
    G = readdata(data)
    pairs =((u,v) for u in G for v in G if u!=v)
    for u,v in pairs:
        v,part = minimum_cut(G,u,v)
        if v==3.0:
            print(len(part[0])*len(part[1]))
            break
            

if __name__=="__main__":
    part1(EXAMPLE)
    part1()