from itertools import product

test="""
5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526
"""

data="""
4585612331
5863566433
6714418611
1746467322
6161775644
6581631662
1247161817
8312615113
6751466142
1161847732
"""

def makematrix(text):
    lines=text.splitlines()
    M=[ [ int(c) for c in lines[i]  ] for i in range(1,len(lines)) ]
    return M

def printmatrix(M):
    R=len(M)
    C=len(M[0])
    for l in M:
        print("".join(str(x) for x in l))
    print("-"*C)

def flash(M,x,y):
    R=len(M)
    C=len(M[0])
    flashes=[]
    M[x][y]=0
    for nx,ny in product([x-1,x,x+1],[y-1,y,y+1]):
        if nx<0 or nx>=R:
            continue
        if ny<0 or ny>=C:
            continue
        if M[nx][ny]==0:
            continue
        M[nx][ny]+=1
        if M[nx][ny]>9:
            flashes.append((nx,ny))
    return flashes
        

def nextiteration(M):
    counter=0
    R=len(M)
    C=len(M[0])
    queue=[]
    for i,j in product(range(R),range(C)):
        M[i][j] += 1
        if M[i][j]>9:
            queue.append((i,j))
    t = 0
    while t<len(queue):
        x,y=queue[t]
        if M[x][y]==0:
            t +=1
            continue
        l = flash(M,x,y)
        counter +=1
        queue.extend(l)
        t+=1
    return counter

def iterate(M,t):
    for _ in range(t):
        x = nextiteration(M)
    return x

def part1(data):
    M=makematrix(data)
    cnt=0
    for i in range(100):
        cnt+= nextiteration(M)
    print(cnt)

def part2(data):
    M=makematrix(data)
    R=len(M)
    C=len(M[0])
    i=0
    while True:
        i+=1
        r = nextiteration(M)
        if r == R*C:
            break
    print(i)
    
if __name__ == "__main__":
    part1(test)
    part1(data)
    part2(test)
    part2(data)