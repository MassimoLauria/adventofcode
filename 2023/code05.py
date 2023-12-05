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
            Almanac[current][-1].append(int(data[i+1]))
            Almanac[current][-1].append(int(data[i]))
            Almanac[current][-1].append(int(data[i+2]))
            i+=3
        Almanac[current].sort()
    Almanac['chain']=chain
    return Almanac

def find_next(srcvalue,vmap):
    for sbase,dbase,length in vmap:
        if sbase<= srcvalue< sbase+length:
            return srcvalue + dbase - sbase
    return srcvalue

def next_intervals(a,b,vmap):
    intervals=[]
    N=len(vmap)
    i=0
    while i<N and a<=b:
        sbase,dbase,length = vmap[i]
        assert length>0
        if a<sbase:
            t=min(b,sbase-1)
            intervals.append((a,t))
            a = t+1
        elif a>=sbase+length:
            i+=1
        else: # sbase <= a < sbase+lenght
            ia = a
            ib = min(b,sbase+length-1)
            sa=ia + dbase - sbase
            sb=ib + dbase - sbase
            intervals.append((sa,sb))
            a = ib+1
    if a<=b:
        intervals.append((a,b))
    return intervals


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

def part2(data=None):
    """solve part 2"""
    almanac = readdata(data)
    chain = almanac['chain'][1:]
    dst_intervals=[]
    N=len(almanac['seeds'])
    for i in range(0,N,2):
        a,l = almanac['seeds'][i:i+2]
        dst_intervals.append((a,a+l-1))
    #print("seeds intervals")
    #print(dst_intervals)
    for target in chain:
        #print("Going to",target)
        src_intervals=dst_intervals
        dst_intervals=[]
        for a,b in src_intervals:
            t = next_intervals(a,b,almanac[target])
            #print(a,b,"goes to",t)
            dst_intervals.extend(t)
        #print(target,"intervals")
        #print(dst_intervals)
    #print(dst_intervals)
    print(min([a for a,b in dst_intervals]))

if __name__ == "__main__":
    part1(EXAMPLE)
    part1()
    part2(EXAMPLE)
    part2()
