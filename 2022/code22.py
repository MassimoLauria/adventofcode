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

NOREV = False
REV   = True

example_map  = { (2,0): 'B', (0,1): 'V' , (1,1): 'W',
                 (2,1): 'R',  (2,2): 'G', (3,2): 'Y' }

example_cube_layout = {
    # from face, direction, face, direction, reverse needed?
    ('V','t') : ('B','t'  ,REV),
    ('V','b') : ('G','b' ,REV),
    ('V','r') : ('W','l' ,NOREV),
    ('V','l') : ('Y','b',REV),

    ('R','t') : ('B','b'   ,NOREV),
    ('R','b') : ('G','t'  ,NOREV),
    ('R','l') : ('W','r'  ,NOREV),
    ('R','r') : ('Y','t' ,REV),

    ('W','t') : ('B','l'   ,NOREV),
    ('W','b') : ('G','l'  ,REV),

    ('Y','l') : ('G','r'  ,NOREV),
    ('Y','r') : ('B', 'r' , REV),
}

example_planar_layout = {
    # from face, direction, face, direction, reverse needed?

    ('B','l') : ('B','r' ,NOREV),

    ('V','r') : ('W','l' ,NOREV),
    ('W','r') : ('R','l' ,NOREV),
    ('R','r') : ('V','l' ,NOREV),

    ('G','r') : ('Y','l' ,NOREV),
    ('Y','r') : ('G','l' ,NOREV),

    ('V','t') : ('V','b' ,NOREV),

    ('W','t') : ('W','b' ,NOREV),

    ('B','b') : ('R','t' ,NOREV),
    ('R','b') : ('G','t' ,NOREV),
    ('G','b') : ('B','t' ,NOREV),

    ('Y','t') : ('Y','b' ,NOREV),
}

input_map = {
    (0,2) : 'R',
    (0,3) : 'G',
    (1,0) : 'W',
    (1,1) : 'B',
    (1,2) : 'Y',
    (2,0) : 'V'
}

input_cube_layout = {
    # from face, direction, face, direction, reverse needed?
    ('B','t') : ('W','b' ,NOREV),
    ('B','b') : ('Y','t' ,NOREV),
    ('B','l') : ('R','t' ,NOREV),
    ('B','r') : ('V','b' ,NOREV),

    ('G','t') : ('R','b' ,NOREV),
    ('G','b') : ('V','t' ,NOREV),
    ('G','l') : ('W','t' ,NOREV),
    ('G','r') : ('Y','b' ,NOREV),

    ('R','r') : ('Y','l' ,NOREV),
    ('R','l') : ('W','l' ,REV),

    ('V','l') : ('W','r' ,NOREV),
    ('V','r') : ('Y','r' , REV),
}

input_planar_layout = {
    # from face, direction, face, direction, reverse needed?
    ('R','b') : ('G','t' ,NOREV),
    ('G','b') : ('R','t' ,NOREV),

    ('W','b') : ('B','t' ,NOREV),
    ('B','b') : ('Y','t' ,NOREV),
    ('Y','b') : ('W','t' ,NOREV),

    ('V','t') : ('V','b' ,NOREV),

    ('W','r') : ('V','l' ,NOREV),
    ('V','r') : ('W','l' ,NOREV),

    ('B','r') : ('B','l' ,NOREV),

    ('R','r') : ('Y','l' ,NOREV),
    ('Y','r') : ('R','l' ,NOREV),

    ('G','r') : ('G','l' ,NOREV)
}

def process_layout(layout):
    D = {}
    for f,s in layout:
        nf,ns,rev = layout[f,s]
        if (nf,ns) not in layout:
            D[nf,ns] = (f,s,rev)
    layout.update(D)

def process_map(faces_map):
    D = { name: coords for coords,name in faces_map.items() }
    faces_map.update(D)

def next_pos(px,py,face,cmap,layout,size):

    if py % size == 0 and faces[face]=='^':
        d = 't'
    elif py % size == (size-1) and faces[face]=='v':
        d = 'b'
    elif px % size == 0 and faces[face]=='<':
        d = 'l'
    elif px % size == (size-1) and faces[face]=='>':
        d = 'r'
    else:
        dx,dy = delta[face]
        return px+dx,py+dy,face

    facename = cmap[(px//size),py//size]
    nfacename,nd,rev = layout[facename,d]
    nx,ny = cmap[nfacename]
    nx*=size
    ny*=size  # top left position of the face, in the bidinentional map
    if d=='t' or d=='b':
        param = px % size
    elif d=='l' or d=='r':
        param = py % size
    if rev:
        param = size - 1 - param
    if nd in 't':
        nx += param
        nface = 1
    elif nd == 'b':
        nx += param
        ny += size-1
        nface = 3
    elif nd == 'l':
        ny += param
        nface = 0
    elif nd == 'r':
        ny += param
        nx += size-1
        nface = 2
    else:
        assert False
    return nx,ny,nface


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

def play(path,board,next_pos):
    # start position
    px = board[0].index('.')
    py = 0
    face = 0
    for step in path:
        if step == 'L':
            face = (face-1) % len(faces)
            continue
        elif step == 'R':
            face = (face+1) % len(faces)
            continue
        for i in range(step):
            nx,ny,nface = next_pos(px,py,face)
            if board[ny][nx]=="#":
                break
            else:
                assert board[ny][nx]=="."
                px,py,face = nx,ny,nface
    return 1000*(py+1)+(px+1)*4+face


if __name__ == "__main__":
    process_map(example_map)
    process_map(input_map)
    process_layout(example_planar_layout)
    process_layout(example_cube_layout)
    process_layout(input_planar_layout)
    process_layout(input_cube_layout)

    next_pos_p1e = lambda x,y,f : next_pos(x,y,f,
                                           example_map,
                                           example_planar_layout,4)
    next_pos_p1i = lambda x,y,f : next_pos(x,y,f,
                                           input_map,
                                           input_planar_layout,50)
    next_pos_p2e = lambda x,y,f : next_pos(x,y,f,
                                           example_map,
                                           example_cube_layout,4)
    next_pos_p2i = lambda x,y,f : next_pos(x,y,f,
                                           input_map,
                                           input_cube_layout,50)

    board, path = readdata(EXAMPLE)
    print("part1:",play(path, board,next_pos_p1e))

    board, path = readdata()
    print("part1:",play(path, board,next_pos_p1i))

    board, path = readdata(EXAMPLE)
    print("part2:",play(path, board,next_pos_p2e))

    board, path = readdata()
    print("part2:",play(path, board,next_pos_p2i))
