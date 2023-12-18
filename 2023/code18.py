
from collections import deque
from collections import defaultdict

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
            elif POS[i,j]==False:
                print("O",end="")
            else:
                print("#",end="")
        print()

def lava_count(movelist,R_weights=None,C_weights=None):
    if R_weights is None:
        R_weights=defaultdict(lambda : 1)
    if C_weights is None:
        C_weights=defaultdict(lambda : 1)
    POS=dict()
    cur=(0,0)
    for d,l in movelist:
        for i in range(l):
            POS[cur]=True
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
    POS[top,left]=False
    flooded=0
    while len(Q)>0:
        r,c=Q.popleft()
        flooded+=1
        if r<bottom and not (r+1,c) in POS:
            Q.append((r+1,c))
            POS[(r+1,c)]=False
        if r>top and not (r-1,c) in POS:
            Q.append((r-1,c))
            POS[(r-1,c)]=False
        if c<right and not (r,c+1) in POS:
            Q.append((r,c+1))
            POS[(r,c+1)]=False
        if c>left and not (r,c-1) in POS:
            Q.append((r,c-1))
            POS[(r,c-1)]=False
    count=0
    for i in range(top,bottom+1):
        for j in range(left,right+1):
            if (i,j) not in POS or POS[i,j]:
                count+=R_weights[i]*C_weights[j]
    #printf(POS)
    return count


def part1(data=None):
    if data is None:
        with open("input18.txt") as f:
            data=f.read()
    moves=[]
    for line in data.splitlines():
        line=line.split()
        moves.append((line[0],int(line[1])))
    print(lava_count(moves))

def compress_space(coords):
    coords=sorted(coords)
    res=[]
    res.append(coords[0])
    for i in range(1,len(coords)):
        if coords[i]==coords[i-1]:
            continue
        delta = coords[i]-coords[i-1]-1
        if delta==1:
            res.append(coords[i-1]+1)
        elif delta>1:
            res.append((coords[i-1]+1,coords[i]-1))
        res.append(coords[i])
    return res

def moves_to_loop(moves):
    loop=[(0,0)]
    rows,cols=[0],[0]
    minrow,maxrow,mincol,maxcol=0,0,0,0
    # get the axis
    for d,l in moves:
        dr,dc=DELTA[d]
        sr,sc=loop[-1]
        nr,nc=sr+l*dr,sc+l*dc
        loop.append((nr,nc))
    return loop

def ticks_to_weights(ticks):
    W=defaultdict(lambda : 1)
    for i in range(len(ticks)):
        if type(ticks[i])==int:
            W[i]=1
        else:
            W[i]=ticks[i][1]-ticks[i][0]+1
    return W

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
    loop = moves_to_loop(moves)
    Rticks = compress_space([x for (x,y) in loop])
    Cticks = compress_space([y for (x,y) in loop])
    Rweights=ticks_to_weights(Rticks)
    Cweights=ticks_to_weights(Cticks)
    # new movelist
    shortmoves=[]
    lr,lc=0,0
    sr,sc=Rticks.index(0),Cticks.index(0)
    print("Convert")
    for d,l in moves:
        dr,dc=DELTA[d]
        lr,lc=lr+l*dr,lc+l*dc
        shortlen=0
        print(d,l,"--->",end="")
        while Rticks[sr]!=lr or Cticks[sc]!=lc:
            sr+=dr
            sc+=dc
            shortlen+=1
        print(d,shortlen)
        shortmoves.append((d,shortlen))
    # print(moves)
    # print(loop)
    # print(shortmoves)
    # print(Rweights)
    # print(Cweights)
    # print(Rticks)
    # print(Cticks)
    V=lava_count(shortmoves,Rweights,Cweights)
    print(V)

if __name__=="__main__":
    part1(EXAMPLE)
    part1()
    part2(EXAMPLE)
    part2()
