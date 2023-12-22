"""Advent of Code 2023 day 22
"""

from collections import defaultdict
from collections import deque


EXAMPLE = """1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9
"""

def readdata(data=None):
    """Read and parse the input data"""
    if data is None:
       with open("input22.txt") as f:
            data = f.read()
    cubes=defaultdict(list)
    zorder=[]
    idx=0
    for line in data.splitlines():
        block=line.split('~')
        s=list(map(int,block[0].split(',')))
        e=list(map(int,block[1].split(',')))
        bid='b'+str(idx)
        idx+=1
        if s[0]!=e[0]:
            for i in range(s[0],e[0]+1):
                cubes[bid].append([i,s[1],s[2]])
        elif s[1]!=e[1]:
            for i in range(s[1],e[1]+1):
                cubes[bid].append([s[0],i,s[2]])
        else:
            for i in range(s[2],e[2]+1):
                cubes[bid].append([s[0],s[1],i])
    return cubes

def reverse(D):
    R=defaultdict(set)
    for u in D:
        for v in D[u]:
            R[v].add(u)
    return R


def whos_below_me(cubes):
    zorder=[]
    for bid,c in cubes.items():
        zorder.append((c[0][2],bid))
    zorder.sort()
    Ground=defaultdict(lambda:(0,'floor'))
    below={}
    # make the fall
    for _,bid in zorder:
        xy=[(x,y) for x,y,_ in cubes[bid]]
        height=cubes[bid][-1][2]-cubes[bid][0][2]+1
        if height>1:
            xy=[cubes[bid][0][0:2]]
        else:
            xy=[(x,y) for x,y,_ in cubes[bid]]
        landing=max(Ground[x,y][0] for x,y in xy)
        tsupport=[Ground[x,y][1] for x,y in xy if Ground[x,y][0]==landing]
        below[bid]=set([x for x in tsupport if x!='floor'])
        assert len(below[bid])<=len(cubes[bid])
        for x,y in xy:
            Ground[x,y]=(landing+height,bid)
    return below

def needed(bid,above,below):
    for a in above[bid]:
        if below[a]=={bid}:
            return True
    return False

def part1(data=None):
    """solve part 1"""
    cubes=readdata(data)
    below=whos_below_me(cubes)
    above=reverse(below)
    can_disintegrate=0
    for bid in cubes:
        if not needed(bid,above,below):
            can_disintegrate+=1
    print(can_disintegrate)

def fall(start,above,below):
    fallen=set([start])
    Q=deque(above[start])
    while len(Q)>0:
        bid=Q.popleft()
        t = below[bid].intersection(fallen)
        if len(t)==len(below[bid]):
            fallen.add(bid)
            Q.extend(above[bid])
    return len(fallen)-1

def part2(data=None):
    """solve part 2"""
    cubes=readdata(data)
    below=whos_below_me(cubes)
    above=reverse(below)
    brick_sum=sum(fall(bid,above,below) for bid in cubes)
    print(brick_sum)



if __name__ == "__main__":
    part1(EXAMPLE)
    part1()
    part2(EXAMPLE)
    part2()
