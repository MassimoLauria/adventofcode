
testcode=[('F',10),('N',3),('F',7),('R',90),('F',11)]

def readcode():
    I=[]
    with open('aoc12input.txt') as f:
        for line in f:
            op=line[0]
            arg=int(line[1:])
            if op in 'LR':
                if arg % 90 !=0:
                    raise ValueError('Impossible rotation')
            I.append((op,arg))
    return I

def normalize(code):
    ncode=[]
    for op,arg in code:
        if op=='S':
            ncode.append(('N',-arg))
        elif op=='W':
            ncode.append(('E',-arg))
        elif op=='L':
            ncode.append(('R',360-arg))
        else:
            ncode.append((op,arg))
    return ncode

def rot90(x,y):
    return (y,-x)

# x coordinates is West East (positive is East)
# y coordinate is North South (positive is North)
# code is normalized by normalize
def execute1(code):
    facing=(+1,0)
    
    x,y=0,0
    for op,arg in code:
        if op=='N':
            y += arg
        elif op=='E':
            x += arg
        elif op=='F':
            dx,dy=facing
            x += arg*dx
            y += arg*dy
        elif op=='R':
            for _ in range(arg//90):
                facing = rot90(*facing)
        else:
            raise ValueError('code is not normalized')
        #print(x,y,end=' -- ')
        #print('face',facing[fid])
    return x,y

def execute2(code):
    sx,sy=0 ,0
    wx,wy=10,1    

    for op,arg in code:
        if op=='N':
            wy += arg
        elif op=='E':
            wx += arg
        elif op=='F':
            sx += arg*wx
            sy += arg*wy
        elif op=='R':
            for _ in range(arg//90):
                wx,wy = rot90(wx,wy)
        else:
            raise ValueError('code is not normalized')
        #print(x,y,end=' -- ')
        #print('face',facing[fid])
    return sx,sy


def part1():
    code=normalize(readcode())
    pos=execute1(code)
    mdist=abs(pos[0])+abs(pos[1])
    print(mdist)


def part2():
    code=normalize(readcode())
    pos=execute2(code)
    mdist=abs(pos[0])+abs(pos[1])
    print(mdist)
    
part1()    
part2()
