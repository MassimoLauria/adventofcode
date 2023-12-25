"""Advent of Code 2023 day 25
"""

import random
import math
import copy
from collections import defaultdict

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


def print_graph(G, filename):
    with open(filename, "w", encoding='utf-8') as f:
        print("graph {", file=f)
        for u, v in G.edges():
            print(f'{u}--{v}', file=f)
        print('}', file=f)


def readdata(data=None):
    """Read and parse the input data"""
    if data is None:
        with open("input25.txt") as f:
            data = f.read()
    G = nx.Graph()
    for line in data.splitlines():
        line = line.split()
        u = line[0][:-1]
        for v in line[1:]:
            G.add_edge(u, v, capacity=1.0)
    return G


def part1(data=None):
    G = readdata(data)
    pairs = ((u, v) for u in G for v in G if u < v)
    for u, v in pairs:
        v, part = minimum_cut(G, u, v)
        if v == 3.0:
            print(len(part[0]) * len(part[1]))
            break


class uf():

    def __init__(self, U):
        self.parent = {x: x for x in U}
        self.size = len(self.parent)

    def part(self, k):
        if self.parent[k] == k:
            return k
        self.parent[k] = self.part(self.parent[k])
        return self.parent[k]

    def join(self, u, v):
        pu = self.part(u)
        pv = self.part(v)
        if pu != pv:
            self.parent[pv] = pu
            self.size -= 1

    def same(self, u, v):
        return self.parent[u] == self.parent[v]

    def __len__(self):
        return self.size




if __name__ == "__main__":
    part1(EXAMPLE)
    part1()
    # Ge = readdata(EXAMPLE)
    # print_graph(Ge,'input25_example.dot')
    G = readdata()
    # print_graph(G,'input25_input.dot')
