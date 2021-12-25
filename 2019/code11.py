from intcode import IntCodeCPU
from collections import defaultdict



def paint(startcolor=0):
    with open("input11.txt") as f:
        code=[int(x) for x in f.read().split(',')]
   
    # up,left,down,right
    dirs=[(0,-1),(-1,0),(0,1),(1,0)]
    

    # status
    grid=defaultdict(lambda:0)
    currdir=0
    currpos=(0,0)
    grid[currpos]=startcolor

    CPU=IntCodeCPU(code)
    while True:
        #print(f"Robot at {currpos} sees {grid[currpos]}")
        CPU.add_input([grid[currpos]])
        CPU.run()
        color,turn=CPU.get_output()
        currdir = (currdir + 1 - 2*turn) % 4
        x,y = currpos
        dx,dy = dirs[currdir]
        nextpos = x+dx,y+dy
        #print(f"Robot paint {color} and moves to {nextpos}")
        grid[currpos]=color
        currpos=nextpos
        CPU.flush_output()
        
        if CPU.halted():
            #print(f"Robot at {currpos} stops")
            break
    return grid
        
def part1():
    hull=paint(startcolor=0)
    print(len(hull))

def part2():
    hull=paint(startcolor=1)
    M=[ [" "]*50 for _ in range(6)]
    for x,y in hull:
        if hull[x,y]==1:
            M[y][x]="#"
    for m in M:
        print("".join(m))
    

if __name__=="__main__":
    part1()
    part2()