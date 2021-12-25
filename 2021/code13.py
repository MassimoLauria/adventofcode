from collections import defaultdict

test="""
6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5
"""

def parsedata(data=None):
    prefixx="fold along x="
    prefixy="fold along y="
    if data is None:
        with open("input13.txt") as f:
            data=f.read()
    data=data.splitlines()
    
    P=[]
    F=[]
    for l in data:
        if "," in l:
            x,y=l.split(',')
            P.append((int(x),int(y)))
        elif "y=" in l:
            F.append(('y',int(l.split('=')[1])))
        elif "x=" in l:
            F.append(('x',int(l.split('=')[1])))
    return P,F

def foldy(P,folds):
    XtoY=defaultdict(lambda:[])
    for x,y in P:
        XtoY[x].append(y)
    for x in XtoY:
        ys=XtoY[x]
        for _,fy in folds:
            nys=[]
            for y in ys:
                if y<fy:
                    nys.append(y)
                else:
                    nys.append(2*fy-y)
            nys=list(set(nys))
            ys=nys
        XtoY[x]=ys
    nP=[]
    for x,ys in XtoY.items():
        for y in ys:
            nP.append((x,y))
    return nP

def part1(data=None):
    P,F=parsedata(data)
    #print(P,F)
    if F[0][0]=='y':
        print(len(foldy(P,F[:1])))
    else:
        rP=[(y,x) for x,y in P]
        print(len(foldy(rP,F[:1])))
    
def drawpoints(P):
    print()
    maxx=max(x for x,y in P)
    maxy=max(y for x,y in P)
    M =[[' ']*(maxx+1) for _ in range(maxy+1)]
    for x,y in P:
        M[y][x]='#'
    for l in M:
        print("".join(l))
    print()
    

def part2(data=None):
    P,F=parsedata(data)
    FX=[f for f in F if f[0]=='x']
    FY=[f for f in F if f[0]=='y']
    P = foldy(P,FY)
    P1=[(y,x) for x,y in P]
    P2= foldy(P1,FX)
    P3=[(x,y) for y,x in P2]
    drawpoints(P3)

if __name__ == "__main__":
    part1(test)
    part1()
    part2(test)
    part2()
    
    