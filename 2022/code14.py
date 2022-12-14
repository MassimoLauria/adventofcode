"""Advent of Code 2022 day 14
"""

EXAMPLE = """
498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
"""

def readdata(data=None):
    """Read and parse the input data"""
    if data is None:
       with open("input14.txt") as f:
            data = f.read()
    data=data.split()
    L = []
    i=1
    sx,sy = data[0].split(',')
    sx,sy = int(sx),int(sy)
    while i < len(data):
        if not data[i][0].isdigit():
            dx,dy = data[i+1].split(',')
            dx,dy = int(dx),int(dy)
            L.append((min(sx,dx),min(sy,dy),
                      max(sx,dx),max(sy,dy)))
            i+=1
        else:
            dx,dy = data[i].split(',')
            dx,dy = int(dx),int(dy)
        sx,sy=dx,dy
        i+=1
    return L

def box(L):
    minx=500
    miny=0
    maxx=minx
    maxy=miny
    for sx,sy,dx,dy in L:
        minx=min(minx,sx)
        minx=min(minx,dx)
        maxx=max(maxx,sx)
        maxx=max(maxx,dx)
        miny=min(miny,sy)
        miny=min(miny,dy)
        maxy=max(maxy,sy)
        maxy=max(maxy,dy)
    return minx,miny,maxx,maxy

def printmap(tmap):
    for l in tmap:
        print("".join(l))
    print()

def createmap(L,stretch=False):
    minx,miny,maxx,maxy=box(L)
    minx-=1
    maxx+=1
    maxy+=2
    if stretch:
        maxx+=maxy
        minx-=maxy
    W=maxx-minx+1
    H=maxy-miny+1
    assert miny==0
    M = [ [' ']*W  for _ in range(H)]
    for sx,sy,dx,dy in L:
        for i in range(sy,dy+1):
            for j in range(sx,dx+1):
                M[i-miny][j-minx] = "#"
    if stretch:
        for j in range(W):
            M[-1][j]="#"
    sandx=500-minx
    M[0][sandx]="+"
    assert 0<= sandx < W
    return M,sandx


def part1(data=None):
    """solve part 1"""
    rocks = readdata(data)
    M,sandx = createmap(rocks)
    H = len(M)
    W = len(M[0])
    path = [(sandx,0)]
    px,py = path.pop()
    count=0
    while True:
        if px==0 or px==W-1 or py==H-1:
            break # particle falling down indefinitely
        if M[py+1][px]==" ":
            path.append((px,py))
            py +=1
        elif M[py+1][px-1]==" ":
            path.append((px,py))
            px -=1
            py +=1
        elif M[py+1][px+1]==" ":
            path.append((px,py))
            px +=1
            py +=1
        else:
            M[py][px]="o"
            px,py=path.pop()
            count+=1
    print("part1:",count)

def part2(data=None):
    """solve part 2"""
    rocks = readdata(data)
    M,sandx = createmap(rocks,True)
    H = len(M)
    W = len(M[0])
    path = [(sandx,0)]
    px,py = path.pop()
    count=0
    while True:
        if M[py+1][px]==" ":
            path.append((px,py))
            py +=1
        elif M[py+1][px-1]==" ":
            path.append((px,py))
            px -=1
            py +=1
        elif M[py+1][px+1]==" ":
            path.append((px,py))
            px +=1
            py +=1
        else:
            M[py][px]="o"
            count+=1
            if py==0:
                break
            px,py=path.pop()
    print("part2:",count)


if __name__ == "__main__":
    part1(EXAMPLE)
    part1()
    part2(EXAMPLE)
    part2()
