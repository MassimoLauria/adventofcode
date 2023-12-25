"""Advent of Code 2023 day 24

Using z3! Is that cheating?
"""
import math
from collections import defaultdict
from random import randint

import z3

EXAMPLE = """19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3
"""

def readdata(data=None):
    """Read and parse the input data"""
    if data is None:
        with open("input24.txt") as f:
            data = f.read()
    hail=[]
    for line in data.splitlines():
        line="".join([ (c if c.isdigit() or c in "+-" else " ") for c in list(line) ])
        hail.append([int(x) for x in line.split()])
    return hail

def ray_intersect(h1,h2):
    p1x,p1y,_,v1x,v1y,_=h1
    p2x,p2y,_,v2x,v2y,_=h2
    A=[[v1x,-v2x],[v1y,-v2y]]
    detA=A[0][0]*A[1][1]-A[0][1]*A[1][0]
    b = [p2x-p1x,p2y-p1y]
    if detA==0:
        return None
    sol1=b[0]*A[1][1]-A[0][1]*b[1]
    sol2=A[0][0]*b[1]-b[0]*A[1][0]
    t1,t2 = (sol1/detA,sol2/detA)
    if t1<=0 or t2<=0:
        return None
    return (p2x+v2x*t2,p2y+v2y*t2)


def part1(ta,data=None):
    """solve part 1"""
    hails=readdata(data)
    N=len(hails)
    intersections=[]
    for i in range(0,N-1):
        for j in range(i+1,N):
            p = ray_intersect(hails[i],hails[j])
            if p is not None:
                intersections.append(p)
    counter=0
    for x,y in intersections:
        if ta[0]<=x<=ta[1] and ta[0]<=y<=ta[1]:
            counter+=1
    print(counter)



def three_same_X(pos,vel):
    points=[]
    N=len(pos)
    for i in range(N):
        points.append((pos[i],vel[i],i))
    points.sort()
    assert all(v!=0 for v in vel)
    # points with same coord state
    for i in range(N-2):
        if points[i][0:2]==points[i+1][0:2]:
            return (points[i][2],
                    points[i+1][2],
                    points[i+2][2])
    return None

def num_value(indexes,array):
    assert len(indexes)==3
    return len(set([array[indexes[i]] for i in [0,1,2]]))

def check_sol_axis(sp,sv,pos,vel):
    N=len(vel)
    for p,v in zip(pos,vel):
        if v==sv and p!=sv: return False
        else:
            r = (p-sp) % (v-sv)
            if r!=0: return False
    return True


def part2old(data=None):
    AOS=readdata(data)
    N=len(AOS)
    times=[0]*N
    solution=[0,0,0,0,0,0]
    SOA=list(zip(*AOS))
    # three elements have same position and velocity in X
    # but incompatible positions and velocity in Y and Z
    # hence cannot be met at the same time
    three  = three_same_X(SOA[0],SOA[3])
    assert num_value(three,SOA[0])==1
    assert num_value(three,SOA[3])==1
    assert num_value(three,SOA[1])==3
    assert num_value(three,SOA[4])==3
    assert num_value(three,SOA[2])==3
    assert num_value(three,SOA[5])==3
    y1,vy1 = SOA[1][three[0]],SOA[4][three[0]]
    y2,vy2 = SOA[1][three[1]],SOA[4][three[1]]
    y3,vy3 = SOA[1][three[2]],SOA[4][three[2]]
    assert (y1-y2) % (vy2-vy1)!=0
    assert (y1-y3) % (vy3-vy1)!=0
    assert (y2-y3) % (vy3-vy2)!=0
    # hence they must meet at three different times
    # and that give us constraints for the Y and Z

    print(sum(solution[0:3]))

def part2(data=None):
    AOS=readdata(data)
    N=len(AOS)  # N=3
          # actually you can get the solution with just 3 hails
          # but it is not faster...
    T=[z3.Int(f't{i}') for i in range(N)]
    px,vx,py,vy,pz,vz = [ z3.Int(s)
                          for s in "px vx py vy pz vz".split() ]
    solver = z3.Solver()
    for i in range(N):
        solver.add(T[i]>=0)
    for i in range(N):
        sx,sy,sz,svx,svy,svz = AOS[i]
        solver.add( sx + svx*T[i] == px + vx*T[i])
        solver.add( sy + svy*T[i] == py + vy*T[i])
        solver.add( sz + svz*T[i] == pz + vz*T[i])
    #print(solver)
    solver.check()
    m=solver.model()
    #print(m)
    print(m.evaluate(px+py+pz))


if __name__ == "__main__":
    part1([7,27],EXAMPLE)
    part1([200000000000000,400000000000000])
    part2(EXAMPLE)
    part2()
