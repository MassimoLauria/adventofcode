
demo='''
.#.
..#
###
'''

with open('aoc17input.txt') as f:
    exdata=f.read()



def directions_gen3d():
    return [ (dx,dy,dz,0) for dx in [-1,0,1] for dy in [-1,0,1] for dz in [-1,0,1] if not (dx==dy==dz==0)]

def directions_gen4d():
    return [ (dx,dy,dz,dt) for dx in [-1,0,1] \
                           for dy in [-1,0,1] \
                           for dz in [-1,0,1] \
                           for dt in [-1,0,1] if not (dx==dy==dz==dt==0)]


DIRS=None
ACTIVE='#'
INACTIVE='.'

def lookat(env,pos,direction,default=INACTIVE):
    target = tuple(coord+delta for coord,delta in zip(pos,direction))
    if target not in env:
        return default
    return env[target]

def count_around(env,pos):
    actives=0
    for d in DIRS:
        if lookat(env,pos,d)==ACTIVE:
            actives += 1
    return actives

def enlarge(space,default=INACTIVE):
    for pos in list(space.keys()):
        for d in DIRS:
            target = tuple(coord+delta for coord,delta in zip(pos,d))
            if target not in space:
                space[target]=default

def createspace(text):
    D={}
    x=0
    lines=[line.strip() for line in text.split('\n') if len(line.strip())!=0]
    for x,line in enumerate(lines):
        for y,c in enumerate(line):
            D[(x,y,0,0)]=c
    return D

def nextcycle(space):
    newspace={}
    enlarge(space) 
    for pos in space:
        A=count_around(space,pos)
        if space[pos]==ACTIVE and A in [2,3]:
            newspace[pos]=ACTIVE
        elif space[pos]==INACTIVE and A==3:
            newspace[pos]=ACTIVE
    return newspace

def part1():
    global DIRS
    DIRS=directions_gen3d()
    S=[createspace(exdata)]
    for i in range(6):
        S.append(nextcycle(S[-1]))
    print(len(S[-1]))

def part2():
    global DIRS
    DIRS=directions_gen4d()
    S=[createspace(exdata)]
    for i in range(6):
        S.append(nextcycle(S[-1]))
    print(len(S[-1]))

part1()
part2()
     
     
    
   