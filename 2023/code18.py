
from collections import deque

EXAMPLE="""R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)
"""

DELTA={ "U":(-1,0), "D":(1,0), "L":(0,-1),"R":(0,1) }

def printf(POS):
    rows=[x for (x,y) in POS]        
    cols=[y for (x,y) in POS]
    top=min(rows)
    bottom=max(rows)
    left=min(cols)
    right=max(cols)
    print(top,bottom,left,right)
    for i in range(top,bottom+1):
        for j in range(left,right+1):
            if not (i,j) in POS:
                print(".",end="")
            elif POS[i,j]==None:
                print("O",end="")
            else:
                print("#",end="")
        print()
            
    

def part1(data=None):
    if data is None:
        with open("input18.txt") as f:
            data=f.read()
    moves=[]
    for line in data.splitlines():
        line=line.split()
        moves.append((line[0],int(line[1]),line[2][2:-1]))
    POS=dict()
    cur=(0,0)
    for d,l,c in moves:
        for i in range(l):
            POS[cur]=c
            dr,dc=DELTA[d]
            cur=cur[0]+dr,cur[1]+dc
    rows=[x for (x,y) in POS]        
    cols=[y for (x,y) in POS]
    top=min(rows)-1
    bottom=max(rows)+1
    left=min(cols)-1
    right=max(cols)+1
    # flood
    Q=deque([(top,left)])
    POS[top,left]=None
    flooded=0
    while len(Q)>0:
        r,c=Q.popleft()
        flooded+=1
        if r<bottom and not (r+1,c) in POS:
            Q.append((r+1,c))
            POS[(r+1,c)]=None
        if r>top and not (r-1,c) in POS:
            Q.append((r-1,c))
            POS[(r-1,c)]=None
        if c<right and not (r,c+1) in POS:
            Q.append((r,c+1))
            POS[(r,c+1)]=None
        if c>left and not (r,c-1) in POS:
            Q.append((r,c-1))
            POS[(r,c-1)]=None
    size=(right-left+1)*(bottom-top+1)
    print(size-flooded)
    #printf(POS)
    
def part2(data=None):
    if data is None:
        with open("input18.txt") as f:
            data=f.read()
    D2D={"0":"R","1":"D","2":"L","3":"U"}
    moves=[]
    for line in data.splitlines():
        line=line.split()
        d = D2D[line[2][-2]]
        l = int(line[2][2:-2],16)
        moves.append((d,l))
    print(moves)
    
if __name__=="__main__":
    part1(EXAMPLE)
    part1()
    part2(EXAMPLE)