example='''
sesenwnenenewseeswwswswwnenewsewsw
neeenesenwnwwswnenewnwwsewnenwseswesw
seswneswswsenwwnwse
nwnwneseeswswnenewneswwnewseswneseene
swweswneswnenwsewnwneneseenw
eesenwseswswnenwswnwnwsewwnwsene
sewnenenenesenwsewnenwwwse
wenwwweseeeweswwwnwwe
wsweesenenewnwwnwsenewsenwwsesesenwne
neeswseenwwswnwswswnw
nenwswwsewswnenenewsenwsenwnesesenew
enewnwewneswsewnwswenweswnenwsenwsw
sweneswneswneneenwnewenewwneswswnese
swwesenesewenwneswnwwneseswwne
enesenwswwswneneswsenwnewswseenwsese
wnwnesenesenenwwnenwsewesewsesesew
nenewswnwewswnenesenwnesewesw
eneswnwswnwsenenwnwnwwseeswneewsenese
neswnwewnwnwseenwseesewsenwsweewe
wseweeenwnesenwwwswnew
'''

def parseexample():
    for line in example.split():
        yield line
        
def parsefile():
    with open('aoc24input.txt') as f:
        yield from f.read().split()
        
        
def counttotalblacks(grid):
    count=0
    for _,isblack in grid.items():
        if isblack:
            count += 1
    return count
            
# axial hexagonal coordinates
DIRS={ 'e'  : (1, 0), 'w'  : (-1,0),
       'se' : (1,-1), 'ne' : ( 0,1),
       'sw' : (0,-1), 'nw' : (-1,1)  }
            
def walkgrid(text):
    L=len(text)
    i=0
    x,y=0,0
    while i<L:
        if text[i] in 'ew':
            dx,dy=DIRS[text[i]]
            i +=1
        else:
            dx,dy=DIRS[text[i:i+2]]
            i +=2
        x,y = x+dx,y+dy
    return x,y
        
def expandaroundblack(grid):
    newgrid={}
    for x,y in grid:
        newgrid[x,y]=grid[x,y]
        if not grid[x,y]:
            continue
        for dx,dy in DIRS.values():
            if (x+dx,y+dy) not in newgrid:
                newgrid[x+dx,y+dy]=False
    return newgrid
                
def countblacks(grid,x,y):
    count = 0
    for dx,dy in DIRS.values():
        if grid.get((x+dx,y+dy),False):
            count += 1
    return count
    
    
def nextstep(grid):
    grid=expandaroundblack(grid)
    newgrid={}
    for x,y in grid:
        b = countblacks(grid,x,y)
        if grid[x,y]: #black tile...
            if b==1 or b==2:
                newgrid[x,y]=True   #..stays black
        else:
            if b==2:
                newgrid[x,y]=True   #..becomes black
    return newgrid
            
        
def part1():
    tilegrid={}
    for line in parsefile():
        tx,ty=walkgrid(line)
        tilegrid[tx,ty] = not tilegrid.get((tx,ty),False)
    print(counttotalblacks(tilegrid))
    
    
def part2():
    # Init phase
    tilegrid={}
    for line in parsefile():
        tx,ty=walkgrid(line)
        tilegrid[tx,ty] = not tilegrid.get((tx,ty),False)
    for i in range(1,101):
        tilegrid=nextstep(tilegrid)
    #print('Day {}:'.format(100),counttotalblacks(tilegrid))
    print(counttotalblacks(tilegrid))
    
part1()
part2()