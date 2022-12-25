"""Advent of Code 2019 day 15
"""

EXAMPLE = """
"""

from intcode import IntCode,IntCodeCPU
from collections import deque

def readdata(data=None):
    """Read and parse the input data"""
    if data is None:
       with open("input15.txt") as f:
            data = f.read()
    return [int(x) for x in data.strip().split(',')]

dirs = {"N": 1, "S": 2, "W": 3, "E": 4}
opposite = [None,2,1,4,3]
deltas = [None,(0,-1),(0,+1),(-1,0),(1,0)]
WALL = '#'
VOID = ' '
OXYG = 'E'
pict={0:WALL,1:VOID,2:OXYG}

def explore(CPU,direction):
    if type(direction)==str:
        direction = dirs[direction]
    CPU.add_input([direction])
    CPU.run()
    assert CPU.status=='WAITING'
    assert len(CPU.get_output())==1
    x = CPU.get_output()[0]
    CPU.flush_output()
    return x

def DFS(CPU,Map,sx,sy):
    stack = [(sx,sy,0)]
    while len(stack)>0:
        x,y,i = stack.pop()
#        print("Explore",x,y,"XNSWEX"[i])
        if i>=len(dirs) and len(stack)>0:
#            print("Going back to",stack[-1][:2])
            coming_from = stack[-1][2]
            scan = explore(CPU,opposite[coming_from])
            continue
        elif i>=len(dirs):
#            print("End of visit")
            continue
        i += 1
        stack.append((x,y,i))
        dx,dy = deltas[i]
        if (x+dx,y+dy) in Map:
#            print("We already know",x+dx,y+dy)
            continue
#        print("Plan to explore ",x+dx,y+dy)
        scan = explore(CPU,i)
        assert scan in pict
        Map[x+dx,y+dy] = pict[scan]
        if pict[scan]!=WALL:
            stack.append((x+dx,y+dy,0))
            continue
        #else:
        #    print("Hit a wall",x+dx,y+dy)
    return

def print_map(M,start=None):
    x = [x for x,y in M]
    y = [y for x,y in M]
    mx,my,Mx,My = min(x),min(y),max(x),max(y)
    for i in range(my,My+1):
        for j in range(mx,Mx+1):
            if (i,j)==start:
                print("S",end="")
            elif (i,j) in M and type(M[i,j])==str:
                print(M[i,j],end="")
            elif (i,j) in M and type(M[i,j])==int:
                print(M[i,j] % 10,end="")
            else:
                print(".",end="")
        print()
    print()

def BFS(Map,start,find=None):
    Q = deque([start])
    Map[start]=0
    while len(Q)>0:
        x,y = Q.popleft()
        for dx,dy in [(0,1),(1,0),(0,-1),(-1,0)]:
            if (x+dx,y+dy) not in Map: continue
            if Map[x+dx,y+dy]==WALL: continue
            if Map[x+dx,y+dy]==find: return (x+dx,y+dy,Map[x,y]+1)
            if type(Map[x+dx,y+dy])==int: continue
            Map[x+dx,y+dy] = Map[x,y]+1
            Q.appendleft((x+dx,y+dy))
    return None

def part1and2(data=None):
    """solve part 1"""
    code=readdata()
    CPU=IntCodeCPU(code)
    CPU.run()
    assert CPU.status == 'WAITING'
    Map = { (0,0) : VOID}
    px,py = (0,0)
    # DFS the space
    DFS(CPU,Map,0,0)
    TMap = Map.copy()
    #print_map(Map,start=(0,0))
    ox,oy,dist=BFS(TMap,(0,0),find=OXYG)
    print("part1:",dist)
    BFS(Map,(ox,oy))
    #print_map(Map,start=(ox,oy))
    dists = [d for d in Map.values() if type(d)==int]
    print("part2:",max(dists))


if __name__ == "__main__":
    part1and2()
