from collections import defaultdict
from itertools import combinations,product
import numpy as np

test1="""
start-A
start-b
A-c
A-b
b-d
A-end
b-end
"""

test2="""
dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc
"""

test3="""
fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW
"""

def graph(data=None):
    V=set()
    E=defaultdict(lambda: list())
    if data is None:
        with open("input12.txt") as f:
            data=f.read()
    for l in data.splitlines():
        e=l.strip().split("-")
        if len(e)!=2:
            continue
        a,b = e
        V.add(a)
        V.add(b)
        E[a].append(b)
        E[b].append(a)
    return V,E
      
def visit2(V,E,s,e,forbidden,jolly):
    if s==e:
        return 1
    eg=E[s]
    p=0
    for v in eg:
        if v in forbidden:
            if not jolly and v!="start":
                p+=visit2(V,E,v,e,forbidden,True)
        elif v.lower()==v:
            p+=visit2(V,E,v,e,forbidden+[v],jolly)
        else:
            p+=visit2(V,E,v,e,forbidden,jolly)
    return p

def part1(data=None):
    V,E=graph(data)
    x=visit2(V,E,"start","end",["start"],True)
    print(x)

def part2(data=None):
    V,E=graph(data)
    x=visit2(V,E,"start","end",["start"],False)
    print(x)

if __name__ == "__main__":
    part1(test1) # 10
    part1(test2) # 19
    part1(test3) # 226
    part1()      # 3495
    part2(test1) # 36
    part2(test2) # 103
    part2(test3) # 3509
    part2()      # 94849  

