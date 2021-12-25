#from pprint import pprint as print
from itertools import combinations,product

demo='''
Tile 2311:
..##.#..#.
##..#.....
#...##..#.
####.#...#
##.##.###.
##...#.###
.#.#.#..##
..#....#..
###...#.#.
..###..###

Tile 1951:
#.##...##.
#.####...#
.....#..##
#...######
.##.#....#
.###.#####
###.##.##.
.###....#.
..#.#..#.#
#...##.#..

Tile 1171:
####...##.
#..##.#..#
##.#..#.#.
.###.####.
..###.####
.##....##.
.#...####.
#.##.####.
####..#...
.....##...

Tile 1427:
###.##.#..
.#..#.##..
.#.##.#..#
#.#.#.##.#
....#...##
...##..##.
...#.#####
.#.####.#.
..#..###.#
..##.#..#.

Tile 1489:
##.#.#....
..##...#..
.##..##...
..#...#...
#####...#.
#..#.#.#.#
...#.#.#..
##.#...##.
..##.##.##
###.##.#..

Tile 2473:
#....####.
#..#.##...
#.##..#...
######.#.#
.#...#.#.#
.#########
.###.#..#.
########.#
##...##.#.
..###.#.#.

Tile 2971:
..#.#....#
#...###...
#.#.###...
##.##..#..
.#####..##
.#..####.#
#..#.#..#.
..####.###
..#.#.###.
...#.#.#.#

Tile 2729:
...#.#.#.#
####.#....
..#.#.....
....#..#.#
.##..##.#.
.#.####...
####.#.#..
##.####...
##..#.##..
#.##...##.

Tile 3079:
#.#.#####.
.#..######
..#.......
######....
####.#..#.
.#...#.##.
#.#####.##
..#.###...
..#.......
..#.###...
'''

def parsedata(text):
    tiles={}
    tid=None
    for line in text.split('\n'):
        line=line.strip()
        if 'Tile' in line:
            tid=int(line[5:-1])
            tiles[tid]=[]
        elif len(line)==0:
            tid=None
        else:
            tiles[tid].append(list(line))
    return tiles

def parsefile():
    with open('aoc20input.txt') as f:
        return parsedata(f.read())
        

def side(tile,toward):
    # N->W->S->E, clockwise
    assert toward in 'NESW'
    if toward=='N':
        return ''.join(c for c in tile[0])
    elif toward=='E':
        return ''.join(l[-1] for l in tile)
    elif toward=='S':
        return ''.join(c for c in reversed(tile[-1]))
    elif toward=='W':
        return ''.join(l[0] for l in reversed(tile))
    
    
def enumeratematches(tiles):
    # each entry is:
    #  - which side matches?
    #  - with which tiles?
    #  - and with which side of that tile?
    #  - inverted matching?
    matches={}
    for k in tiles:
        matches[k]=[]
    for tid1,tid2 in combinations(tiles,2):
        tile1=tiles[tid1]
        tile2=tiles[tid2]
        for i,j in product('NESW','NESW'):
            s1=side(tile1,i)
            s2=side(tile2,j)
            if s1==s2[::-1]:
                matches[tid1].append((i,tid2,j,False)) 
                matches[tid2].append((j,tid1,i,False))
            elif s1==s2:
                matches[tid1].append((i,tid2,j,True)) 
                matches[tid2].append((j,tid1,i,True))
    return matches

POS=['NESW','WNES','SWNE','ESWN',
     'NWSE','ENWS','SENW','WSEN']
     
def rotateclockwise(pos,i):
    i = i % 4
    if i==0:
        return pos
    d = list(pos)
    d = d[-i:] + d[0:-i]
    return ''.join(d)
                       
def flipLR(pos):
    d=list(pos)
    d[1],d[3] = d[3],d[1]
    return ''.join(d)

def flipTB(pos):
    d=list(pos)
    d[0],d[2] = d[2],d[0]
    return ''.join(d)

def solve(i,j,o,ls,rs,inv):
    '''
    If a tile in pos i,j with orientation o
    has a side ls matching with a side rs of another tile,
    with or without inversion,
    where should I put the other tile, and in which position'''
    direction=o.index(ls) # where should I attach the tile
    if direction==0:
        ni,nj=i-1,j
    elif direction==1:
        ni,nj=i,j+1
    elif direction==2:
        ni,nj=i+1,j
    else:
        ni,nj=i,j-1
    
    # put rs on the right direction
    initialrot='NESW'.index(rs)
    targetrot='NESW'.index('SWNE'[direction])
    newpos=rotateclockwise('NESW',targetrot-initialrot)   

    # fix flip
    mustflip= (4 <=POS.index(o) < 8) ^ inv
    if direction in [0,2] and mustflip:
        newpos=flipLR(newpos)
    elif direction in [1,3] and mustflip:
        newpos=flipTB(newpos)
    return (ni,nj,newpos)
              
    
def compose(matches):
    # assume 12x12 and put one of the corners top right
    # each entry is (tile,rotation,flip)
    M={}
    crns=corners(matches)
    M[0,0]=(crns[0],POS[0])
    topropagate=[(0,0)]
    while len(topropagate)>0:
        i,j=topropagate[0]
        topropagate.pop(0)
        tile,pos=M[i,j]
        for m in matches[tile]:
            mside1,mtile,mside2,inversion=m
            ni,nj,no=solve(i,j,pos,mside1,mside2,inversion)
            if (ni,nj) not in M:
               M[ni,nj] = mtile,no
               topropagate.append((ni,nj))
            _mtile,_no = M[ni,nj]
            if _mtile != mtile or _no!= no:          
                raise ValueError('Incompatible propagation')
    return M            
    

def gridcoords(grid):
    mini,maxi=0,0
    minj,maxj=0,0
    for i,j in grid:
        mini=min(mini,i)
        minj=min(minj,j)
        maxi=max(maxi,i)
        maxj=max(maxj,j)
    return (mini,minj),(maxi,maxj)


def reposition(square,pos):
    npos=POS.index(pos)
    rotation=npos % 4
    h,w=len(square),len(square[0])
    newsquare=[[None]*w for _ in range(h)]
    for i in range(h):
        for j in range(w):
            ni= i 
            nj= j
            for _ in range(rotation):
                ni,nj = nj,h-ni-1
            if npos % 2==0 and npos>=4: #flip L<->R
                nj = w-nj-1
            elif npos % 2==1 and npos>=4: #flip T<->B
                ni = h - ni - 1
            newsquare[ni][nj]=square[i][j]
    return newsquare

def printsquare(square):
    for row in square:
        print(''.join(row))

def tileintosquare(tile):
        return [list(t[1:-1]) for t in tile[1:-1]]


def paste(canvas,sprite,pos):
    pi,pj=pos
    for si in range(len(sprite)):
        for sj in range(len(sprite[0])):
            canvas[pi+si][pj+sj]=sprite[si][sj]

def extractimage(tiles,grid):
    
    tl,br=gridcoords(grid)
    tilesize=8
    
    ih,iw=(br[0]-tl[0]+1)*tilesize,(br[1]-tl[1]+1)*tilesize
    image=[[' ']*iw for _ in range(ih)]
    
    pi=0
    for i in range(tl[1],br[1]+1):
       pj=0
       for j in range(tl[0],br[0]+1):
           tid,orientation=grid[i,j]
           tile=tiles[tid]
           square=tileintosquare(tile)
           square=reposition(square,orientation)
           paste(image,square,(pi,pj))
           pj += tilesize
       pi += tilesize    
    return image


           
           
    
def corners(matches):
    '''Chech that only four tiles matches in corners
'''
    C=[]
    for k in matches:
        if len(matches[k])!=2:
            continue
        s1=matches[k][0][0]
        s2=matches[k][1][0]
        s1='NWSE'.index(s1)
        s2='NWSE'.index(s2)        
        if abs(s1-s2)==1:
            C.append(k)
    return C

def part1():
    #tiles=parsedata(demo)
    tiles=parsefile()
    matches=enumeratematches(tiles)
    grid=compose(matches)
    tl,br=gridcoords(grid)
    mini,minj=tl
    maxi,maxj=br
    #print('Grid of {}x{}'.format(maxi-mini+1,maxj-minj+1))
    prod=1
    for i,j in product([mini,maxi],[minj,maxj]):
        #print(grid[i,j])
        prod *=grid[i,j][0]
    print(prod)

SEAMONSTER=[list('                  # '),
            list('#    ##    ##    ###'),
            list(' #  #  #  #  #  #   ')]

def countchar(image):
    return sum(t.count('#') for t in image)

def howmany(image,sprite):
    H=len(image)
    W=len(image[0])
    sH=len(sprite)
    sW=len(sprite[0])
    count=0
    for i in range(H-sH):
        for j in range(W-sW):
            match=True
            for si,sj in product(range(sH),range(sW)):
                if sprite[si][sj]=='#' and image[i+si][j+sj]!='#':
                    match=False
                    break
            if match:
                count += 1
    return count

def part2():
    tiles=parsefile()
    #tiles=parsedata(demo)
    matches=enumeratematches(tiles)
    grid=compose(matches)
    I=extractimage(tiles,grid)
    #printsquare(I)
    countwaves=countchar(I)
    countmonster=countchar(SEAMONSTER)
    total=0
    for p in POS:
        NI=reposition(I,p)
        #printsquare(NI)
        found=howmany(NI,SEAMONSTER)
        #print('In orientation {} you find {} monsters'.format(p,found))
        if found>0:
            total=found
    print(countwaves-total*countmonster)

part1()
part2()