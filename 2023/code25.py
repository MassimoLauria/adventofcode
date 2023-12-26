"""Advent of Code 2023 day 25
"""

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
    edges=nx.minimum_edge_cut(G)
    G.remove_edges_from(edges)
    c1,c2 = list(nx.connected_components(G))
    assert len(edges)==3
    print(len(c1)*len(c2))




if __name__ == "__main__":
    part1(EXAMPLE)
    part1()
