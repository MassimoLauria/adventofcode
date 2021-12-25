from pprint import pprint

example="""2199943210
3987894921
9856789892
8767896789
9899965678
"""

def parsedata(data=None):
    if data is None:
        with open("input09.txt") as f:
            data=f.read()
    Map=[None]
    for line in data.splitlines():
        Map.append([9]+[int(x) for x in line]+[9])
    R = len(Map[1])
    Map[0]=[9]*R
    Map.append([9]*R)
    return Map

def lowpoints(M):
    lp=[]
    R=len(M)
    C=len(M[0])
    for r in range(R):
        for c in range(C):
            x = M[r][c]
            if x==9:
                continue
            y = min(M[r][c-1],M[r-1][c],M[r][c+1],M[r+1][c])
            if x < y:
                lp.append((r,c))
    return lp
    

def part1(data=None):
    M=parsedata(data)
    lp = lowpoints(M)
    acc=0
    for r,c in lp:
        acc+= 1+M[r][c]
    print(acc)

def dist(x0,y0,x1,y1):
    return abs(x0-x1)+abs(y0-y1)

def propagateflow(sx,sy,M):
    queue=[(sx,sy)]
    M[sx][sy]=-1
    i=0
    while i<len(queue):
        x,y=queue[i]
        for nx,ny in [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]:
            if M[nx][ny]==9 or M[nx][ny]==-1:
                continue
            queue.append((nx,ny))
            M[nx][ny]=-1
        i += 1
    return len(queue)

def part2(data=None):
    M=parsedata(data)
    lp = lowpoints(M)
    basinsizes=[]
    for r,c in lowpoints(M):
        basinsizes.append(propagateflow(r,c,M))
    basinsizes.sort()
    print(basinsizes[-3]*basinsizes[-2]*basinsizes[-1])        

if __name__ == "__main__":
    part1(example)
    part1()
    part2(example)
    part2()
