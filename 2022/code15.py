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
import re
import math
from collections import defaultdict


def dist(p,q):
    return abs(p[0]-q[0])+abs(p[1]-q[1])

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
    """(x,y)ve part 1"""
    S,B = readdata(data)
    b_on_y = [bx for bx,by in B if by==y]
    b_on_y.sort()
    Intervals = covered_interval(S,y)
    print("part1:", total(Intervals,b_on_y))

def part2(gridsize,data=None):
    """(x,y)ve part 2"""
    sensors,_ = readdata(data)
    signal = {s: dist(s,sensors[s]) for s in sensors }
    energy = {}
    # make a grid of point aligned with sensors
    xt = sorted(list(set([0,gridsize] + [x for x,y in signal])))
    yt = sorted(list(set([0,gridsize] + [y for x,y in signal])))
    # energy of signal at each grid point
    for x in xt:
        for y in yt:
            energy[x,y]=max([signal[s] - dist(s,(x,y))
                             for s in signal])
            if energy[x,y]<0:
                print("part2:",4000000*x+y)
                return
    # find uncovered rectangle
    for i in range(len(xt)-1):
        for j in range(len(yt)-1):

            lx,hx,ly,hy = xt[i], xt[i+1], yt[j], yt[j+1]
            max_distance = hx-lx + hy-ly  # max distance in rectangle

            # test if rectangle is not covered
            if energy[lx,ly]+energy[hx,hy]+1 < max_distance and \
               energy[lx,hy]+energy[hx,ly]+1 < max_distance:
                x1, x2 , y1, y2 =(xt[i],xt[i+1],yt[j],yt[j+1])
                break

    # only one strip is uncovered diagonally
    e1 = energy[x1,y1]
    e2 = energy[x2,y1]
    x = (x1 + x2 + e1 - e2) // 2
    y = x1 + y1 + e1 + 1 - x
    assert dist((x,y),(x1,y1)) == energy[x1,y1]+1
    assert dist((x,y),(x1,y2)) == energy[x1,y2]+1
    assert dist((x,y),(x2,y1)) == energy[x2,y1]+1
    assert dist((x,y),(x2,y2)) == energy[x2,y2]+1
    print("part2:",4000000*x+y)



if __name__ == "__main__":
    part1(10,EXAMPLE)
    part1(2000000)
    part2(20,EXAMPLE)
    part2(4000000)
