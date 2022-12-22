"""Advent of Code 2022 day 22
"""

EXAMPLE = """
        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5
"""

faces = ['>','v','<','^']
delta = [ (1,0), (0,1) , (-1,0) , (0,-1) ]


def tblr_example(x,y):
    t,b,l,r=0,0,0,0
    if y < 4:  l,r, = 8,11
    elif y<8:  l,r = 0,11
    else:      l,r = 8,15
    if x < 8:     t,b, = 4,7
    elif x < 12:  t,b = 0,11
    else:         t,b = 8,11
    return t,b,l,r

def tblr_input(x,y):
    t,b,l,r=0,0,0,0
    if y < 50:     l,r, = 50,149
    elif y < 100:  l,r = 50,99
    elif y < 150:  l,r = 0,99
    else:          l,r = 0,49
    if x < 50:     t,b, = 100,199
    elif x < 100:  t,b = 0,149
    else:          t,b = 0,49
    return t,b,l,r

def next_pos_p1e(px,py,dx,dy):
    assert abs(dx)+abs(dy)==1
    bsize = 4
    tblr  = tblr_example
    nx,ny = px+dx, py+dy
    if not ((px % bsize) in [0,bsize-1] or (py % bsize) in [0,bsize-1]):
        return nx,ny
    #print(nx,ny)
    t,b,l,r = tblr(px,py)
    #print(t,b,l,r)
    if ny<t:
        ny=b
    if ny>b:
        ny=t
    if nx<l:
        nx=r
    if nx>r:
        nx=l
    return nx,ny

def next_pos_p1(px,py,dx,dy):
    assert abs(dx)+abs(dy)==1
    bsize = 50
    tblr  = tblr_input
    nx,ny = px+dx, py+dy
    if not ((px % bsize) in [0,bsize-1] or (py % bsize) in [0,bsize-1]):
        return nx,ny
    #print(nx,ny)
    t,b,l,r = tblr(px,py)
    #print(t,b,l,r)
    if ny<t:
        ny=b
    if ny>b:
        ny=t
    if nx<l:
        nx=r
    if nx>r:
        nx=l
    return nx,ny

def readdata(data=None):
    """Read and parse the input data"""
    if data is None:
       with open("input22.txt") as f:
            data = f.read()
    L = data.splitlines()
    if len(L[0])==0:
        L.pop(0)
    path = L[-1]
    L.pop()
    assert len(L[-1])==0
    L.pop()
    L = [list(l) for l in L]
    s=0
    I = []
    i = 0
    while i < len(path):
        if path[i] in "RL":
            I.append(int(path[s:i]))
            I.append(path[i])
            s=i+1
        i+=1
    if s<i: I.append(int(path[s:i]))
    return L,I

def print_board(B):
    side=max(len(l) for l in B)
    for i,l in enumerate(B):
        s = len(l)
        try:
            s = min(l.index('.'),s)
        except ValueError:
            pass
        try:
            s = min(l.index('#'),s)
        except ValueError:
            pass
        print("{:3}".format(i),"".join(l)," "*(side-len(l)),"  ",s,len(l))

def copy_board(B):
    B2=[]
    for l in B:
        B2.append(l[:])
    return B2

def part1(data=None):
    """solve part 1"""
    B,path = readdata(data)
    next_pos = next_pos_p1e if len(B)==12 else next_pos_p1
    px,py,face = play_board(path,B,next_pos)
    print("part1:", 1000*(py+1)+(px+1)*4+face)

def part2(data=None):
    """solve part 2"""
    B,path = readdata(data)
    next_pos = next_pos_p1e if len(B)==12 else next_pos_p1
    px,py,face = play_board(path,B,next_pos)
    print("part2:", 1000*(py+1)+(px+1)*4+face)

def play_board(path,board,next_pos):
    """solve part 2"""
    tboard= copy_board(board)
    # start position
    px = board[0].index('.')
    py = 0
    face = 0
    curr_delta = delta[face]
    #print_board(tboard)
    for step in path:
        if step == 'L':
            face = (face-1) % len(faces)
            curr_delta = delta[face]
            continue
        elif step == 'R':
            face = (face+1) % len(faces)
            curr_delta = delta[face]
            continue
        # Move forward step
        for i in range(step):
            tboard[py][px] = faces[face]
            nx,ny = next_pos(px,py,curr_delta[0],curr_delta[1])
            if board[ny][nx]=="#":
                break
            else:
                assert board[ny][nx]=="."
                px,py = nx,ny
                tboard[py][px] = faces[face]
        # print_board(B2)
    return px,py,face


if __name__ == "__main__":
    part1(EXAMPLE)
    part1()
    part2(EXAMPLE)
    part2()
