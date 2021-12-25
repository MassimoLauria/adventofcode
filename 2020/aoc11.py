test='''L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL'''

testgrid=[list(row) for row in test.split()]


def readgrid():
    grid=[]
    with open('aoc11input.txt') as f:
        for line in f:
            grid.append(list(line.strip()))
    return grid

def printgrid(G):
    for row in G:
        print(''.join(row))

def emptygrid(template):
    H=len(template)
    W=len(template[0])
    empty=[]
    for _ in range(H):
        empty.append([' ']*W)
    return empty
    

def evolve1(G,i,j):
    
    if G[i][j]=='.':
        return '.'
    
    H,W=len(G),len(G[0])    
    
    minx=max(0  , j-1)
    maxx=min(W-1, j+1)
    
    miny=max(0  , i-1)
    maxy=min(H-1, i+1)
    
    people=0
    for x in range(minx,maxx+1):
        for y in range(miny,maxy+1):
            
            if G[y][x]=='#':
                people +=1
        
    if people>=5:
        return 'L'
    elif people==0:
        return '#'
    else:
        return G[i][j]

def look(G,pos,d):
    H,W = len(G),len(G[0])
    
    r,c = pos[0]+d[0],pos[1]+d[1]
    while 0 <= r < H and 0<= c < W:
        if G[r][c]=='#':
            return '#'
        elif G[r][c]=='L':
            return 'L'
        r += d[0]
        c += d[1]
    return 'L'
    
    
    
def evolve2(G,i,j):
    
    if G[i][j]=='.':
        return '.'
    
    seen=0
    for dire in [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]:
        if look(G,(i,j),dire)=='#':
            seen +=1
        
    if seen>=5:
        return 'L'
    elif seen==0:
        return '#'
    else:
        return G[i][j]

    
def countseats(G):
    seats=0
    for row in G:
        seats += row.count('#')
    return seats

                
def gridstep(old,new,raycast=False):
    H,W =len(old),len(old[0])
    change=False
    for i in range(H):
        for j in range(W):
            if raycast:
                new[i][j]=evolve2(old,i,j)
            else:
                new[i][j]=evolve1(old,i,j)
            if new[i][j]!=old[i][j]:
                change=True
    return change

def part1():
    A=readgrid()
    B=emptygrid(A)
    while gridstep(A,B):
        A,B = B,A                
    print(countseats(A))

def part2():
    A=readgrid()
    B=emptygrid(A)
    #printgrid(A)
    #print()
    while gridstep(A,B,raycast=True):
        A,B = B,A
        #printgrid(A)
        #print()
    print(countseats(A))

part1()
part2()