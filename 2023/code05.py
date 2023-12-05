"""Advent of Code 2023 day 05
"""

EXAMPLE = """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
"""

from collections import defaultdict

def readdata(data=None):
    """Read and parse the input data"""
    if data is None:
       with open("input05.txt") as f:
            data = f.read()
    data=data.split()
    Almanac=defaultdict(list)
    chain=['seeds']
    assert data[0]=="seeds:"
    i=1
    while data[i].isdigit():
        Almanac['seeds'].append(int(data[i]))
        i+=1
    while i<len(data):
        current=data[i]
        p=current.find("-to-")
        assert p>0
        current=current[p+4:]
        chain.append(current)
        i+=2
        while i<len(data) and data[i].isdigit():
            assert i+2<len(data) and data[i+2].isdigit()
            Almanac[current].append([])
            Almanac[current][-1].append(int(data[i]))
            Almanac[current][-1].append(int(data[i+1]))
            Almanac[current][-1].append(int(data[i+2]))
            i+=3
    Almanac['chain']=chain
    return Almanac

def find_next(srcvalue,vmap):
    for dbase,sbase,length in vmap:
        if sbase<= srcvalue< sbase+length:
            return srcvalue + dbase - sbase
    return srcvalue

def part1(data=None):
    """solve part 1"""
    almanac = readdata(data)
    chain = almanac['chain'][1:]
    minloc=None
    for seed in almanac['seeds']:
        v = seed
        for target in chain:
            v = find_next(v,almanac[target])
        if minloc is None: minloc=v
        minloc=min(v,minloc)
    print(minloc)

if __name__ == "__main__":
    part1(EXAMPLE)
    part1()
    # part2()
