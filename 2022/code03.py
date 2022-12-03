"""Advent of Code 2022 day 03
"""
from collections import defaultdict
from itertools import combinations

EXAMPLE = """vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw
"""

def init():
    Pr={}
    i=1
    offset = ord('A')-ord('a')
    for x in range(ord('a'),ord('z')+1):
        Pr[chr(x)] = i
        Pr[chr(x+offset)] = i + 26
        i+=1
    return Pr

Priority=init()

def readdata(text=None):
    """Read and parse the input data"""

    P = {}
    i=1
    offset = ord('A')-ord('a')
    for x in range(ord('a'),ord('z')+1):
        P[chr(x)] = i
        P[chr(x+offset)] = i + 26
        i+=1

    if text is None:
        with open("input03.txt") as f:
            text = f.read()

    sacks = []
    for line in text.splitlines():
        sacks.append([ P[c] for c in line])
    return sacks


def part1(sacks):
    """solve part 1"""
    score = 0
    for sack in sacks:
        size = len(sack)
        assert size % 2 == 0
        l,r = set(sack[:size//2]),set(sack[size//2:])
        x = l.intersection(r)
        score += sum(x)
    print(score)

def part2(sacks):
    assert len(sacks) % 3 == 0
    score = 0
    for i in range(0,len(sacks),3):
        common=set(sacks[i])
        common.intersection_update(sacks[i+1])
        common.intersection_update(sacks[i+2])
        score += sum(common)
    print(score)

if __name__ == "__main__":
    example = readdata(EXAMPLE)
    data = readdata()
    part1(example)
    part1(data)
    part2(example)
    part2(data)
