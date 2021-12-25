from pprint import pprint 

example="""0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2
"""

def readdata(data=None):
    """Output the grid WxH and the lines

    coordinates of forx x,y with (0,0) on top left corner.
    """
    if data is None:
        with open("input05.txt") as f:
            data=f.read()
    data=data.splitlines()
    lines=[]
    maxx,maxy=0,0
    for l in data:
        left,right = l.split(' -> ')
        sx1,sy1 = left.split(',')
        sx2,sy2 = right.split(',')
        x1 = int(sx1)
        x2 = int(sx2)
        y1 = int(sy1)
        y2 = int(sy2)
        maxx=max(maxx,x1,x2)
        maxy=max(maxy,y1,y2)
        lines.append((x1,y1,x2,y2))
    return maxx+1,maxy+1,lines


def part1(data=None):
    gridx,gridy,lines=readdata(data)
    grid = [ [0]*gridx for _ in range(gridy) ]

    for x1,y1,x2,y2 in lines:
        if y1==y2:
            x1,x2=min(x1,x2),max(x1,x2)
            for x in range(x1,x2+1):
                grid[y1][x] +=1
        elif x1==x2:
            y1,y2=min(y1,y2),max(y1,y2)
            for y in range(y1,y2+1):
                grid[y][x1] +=1
    cnt=0  
    for x in range(gridx):
        for y in range(gridy):
            if grid[y][x]>1:
                cnt+=1    
    pprint(cnt)

def part2(data=None):
    gridx,gridy,lines=readdata(data)
    grid = [ [0]*gridx for _ in range(gridy) ]


    for x1,y1,x2,y2 in lines:
        dx = abs(x1-x2)
        dy = abs(y1-y2)
        assert dx==0 or dy==0 or dx==dy
        steps=max(dx,dy)+1

        dirx= 0 if dx==0 else (x2-x1) // abs(dx)
        diry= 0 if dy==0 else (y2-y1) // abs(dy)
        #print("C:",x1,y1,x2,y2)
        #print("Dirx,Diry", dirx,diry)
        #print("Steps", steps)
        for i in range(steps):
            x = x1+dirx*i
            y = y1+diry*i
            #print(x,y)
            grid[y][x] +=1
                
    cnt=0  
    for x in range(gridx):
        for y in range(gridy):
            if grid[y][x]>1:
                cnt+=1    
    pprint(cnt)


if __name__ == "__main__":
    part1(example)
    part1()
    part2(example)
    part2()
