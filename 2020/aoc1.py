from itertools import combinations

def readinput():
    S=set()
    with open('aoc1input.txt') as f:
        for l in f:
            num = int(l.strip())
            S.add(num)
    return S

def part2():
    tot=2020
    S = readinput()
    for a,b in combinations(S,2):
        if tot - a - b in S:
            print(a*b*(tot-a-b))
            return
        
def part1():
    tot=2020
    S = readinput()
    for a in S:
        if tot-a in S:
            print(a*(tot-a))
            return
part1()
part2()
