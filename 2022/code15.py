"""Advent of Code 2022 day 15
"""

EXAMPLE = """
Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3
"""

import random
from collections import defaultdict

def total(intervals,el):
    ttotal = 0
    i=0
    for a,b in intervals:
        ttotal += b-a+1
        while i < len(el) and el[i] < a:
            i+=1
        while i < len(el) and a <= el[i]:
            i+=1
            ttotal -= 1
    return ttotal

def readdata(data=None):
    B=set()
    S={}
    """Read and parse the input data"""
    if data is None:
       with open("input15.txt") as f:
            data = f.read()
    for line in data.splitlines():
        if len(line)==0:
            continue
        sx,sy,bx,by = [int(n) for n in re.findall(r"-?\d+", line)]
        B.add((bx,by))
        S[sx,sy] = (bx,by)
    return S,B

def covered_interval(S,y):
    Covered=[]
    for sx,sy in S:
        bx,by = S[sx,sy]
        w = abs(bx-sx)+abs(by-sy)-abs(sy-y)
        if w>=0:
            Covered.append([sx-w,sx+w])
    Covered.sort()
    # join the intervals
    Joined=[]
    a,b=Covered[0]
    for c,d in Covered:
        if c>b+1:
            Joined.append((a,b))
            a,b = c,d
        else:
            b = max(b,d)
    Joined.append((a,b))
    return Joined


def part1(y,data=None):
    """solve part 1"""
    S,B = readdata(data)
    b_on_y = [bx for bx,by in B if by==y]
    b_on_y.sort()
    Intervals = covered_interval(S,y)
    print("part1:", total(Intervals,b_on_y))

def part2(topy,data=None):
    """solve part 2"""
    S,B = readdata(data)
    rx=-1
    ry=-1
    for y in range(topy+1):
        Intervals = covered_interval(S,y)
        if len(Intervals)>1:
            ry = y
            rx = Intervals[0][1]+1
            break
    print("part2:",4000000*rx+ry)

def part2alt(gridsize,data=None):
    """solve part 2"""
    S,B = readdata(data)
    Disks= {}
    rx = 0
    ry = 0
    for x,y in S:
        bx,by = S[x,y]
        Disks[x,y] = abs(bx-x)+abs(by-y)
    XFree = [[0,gridsize]]*(gridsize+1)
    YFree = [[0,gridsize]]*(gridsize+1)
    print("part2:",4000000*rx+ry)

if __name__ == "__main__":
    part1(10,EXAMPLE)
    part1(2000000)
    part2(20,EXAMPLE)
    part2alt(20,EXAMPLE)
    part2alt(4000000,EXAMPLE)
