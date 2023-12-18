
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

def readdata(data=None):
    if data is None:
        with open("input18.txt") as f:
            data=f.read()
    D2D={"0":"R","1":"D","2":"L","3":"U"}
    p1=[]
    p2=[]
    for line in data.splitlines():
        line=line.split()
        p1.append((line[0],int(line[1])))
        d = D2D[line[2][-2]]
        l = int(line[2][2:-2],16)
        p2.append((d,l))
    return p1,p2

def walk_space(start,movelist,Raxes,Caxes):
    space=dict()
    r,c=start
    cur=Raxes.index(r),Caxes.index(c)
    space[cur]=True
    for d,l in movelist:
        dr,dc=DELTA[d]
        r=r+l*dr
        c=c+l*dc
        while Raxes[cur[0]]!=r or Caxes[cur[1]]!=c:
            cur=cur[0]+dr,cur[1]+dc
            space[cur]=True
    return space

def print_map(space):
    NOP,T,F='.#O'
    rows=[x for (x,y) in space]
    cols=[y for (x,y) in space]
    top=min(rows)
    bottom=max(rows)
    left=min(cols)
    right=max(cols)
    for i in range(top,bottom+1):
        line=[]
        for j in range(left,right+1):
            if (i,j) not in space:
                line.append(NOP)
            elif space[i,j]:
                line.append(T)
            else:
                line.append(F)
        print("".join(line))


def flood_map(POS):
    rows=[x for (x,y) in POS]
    cols=[y for (x,y) in POS]
    assert min(rows)==0 and min(cols)==0
    R=max(rows)+1
    C=max(cols)+1
    # flood
    Q=deque([(-1,-1)])
    POS[-1,-1]=False
    while len(Q)>0:
        r,c=Q.popleft()
        if r<R and not (r+1,c) in POS:
            Q.append((r+1,c))
            POS[(r+1,c)]=False
        if r>=0 and not (r-1,c) in POS:
            Q.append((r-1,c))
            POS[(r-1,c)]=False
        if c<C and not (r,c+1) in POS:
            Q.append((r,c+1))
            POS[(r,c+1)]=False
        if c>=0 and not (r,c-1) in POS:
            Q.append((r,c-1))
            POS[(r,c-1)]=False
    # clean up border
    for r in range(R):
        assert POS[r,-1]==False
        assert POS[r,C]==False
        POS.pop((r,-1))
        POS.pop((r,C))
    for c in range(-1,C+1):
        assert POS[-1,c]==False
        assert POS[R,c]==False
        POS.pop((-1,c))
        POS.pop((R,c))
    return R,C


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

def extract_axes(start,moves):
    rows,cols=[start[0]],[start[1]]
    for d,l in moves:
        dr,dc=DELTA[d]
        nr,nc=rows[-1]+l*dr,cols[-1]+l*dc
        rows.append(nr)
        cols.append(nc)
    return compress_space(rows),compress_space(cols)


def axes_weights(axes):
    assert type(axes[0])==int
    assert type(axes[-1])==int
    weight=[1]
    for i in range(1,len(axes)):
        if type(axes[i])==tuple:
            w=axes[i][1]-axes[i][0]+1
        else:
            w=1
        weight.append(w)
    return weight

def solve(moves):
    raxes,caxes=extract_axes((0,0),moves)
    space=walk_space((0,0),moves,raxes,caxes)
    R,C = flood_map(space)
    rweights=axes_weights(raxes)
    cweights=axes_weights(caxes)
    count=0
    for i in range(R):
        for j in range(C):
            if (i,j) not in space or space[i,j]:
                count+=rweights[i]*cweights[j]
    print(count)

if __name__=="__main__":
    ex_p1,ex_p2=readdata(EXAMPLE)
    in_p1,in_p2=readdata()
    # part1
    solve(ex_p1)
    solve(in_p1)
    # part3
    solve(ex_p2)
    solve(in_p2)
