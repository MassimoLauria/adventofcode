"""Advent of Code 2023 day 10
"""

NEIG={
    '|':( 1, 0,-1, 0),
    '-':( 0, 1, 0,-1),
    'L':(-1, 0, 0, 1),
    'J':(-1, 0, 0,-1),
    '7':( 1, 0, 0,-1),
    'F':( 1, 0, 0, 1),
    '.':(0,0,0,0),
    'S':(0,0,0,0)
}

def type_of_S(M,r,c):
    assert M[r][c]=='S'
    dirs=[]
    if M[r-1][c] in '|F7': dirs.append('n')
    if M[r+1][c] in '|LJ': dirs.append('s')
    if M[r][c+1] in '-J7': dirs.append('e')
    if M[r][c-1] in '-LF': dirs.append('w')
    assert len(dirs)==2
    dirs="".join(sorted(dirs))
    return {"ns":'|', "ew":'-','en':'L',
            "sw":'7', "nw":'J','es':'F' }[dirs]

def findS(M):
    # search S
    R,C=len(M),len(M[0])
    for r in range(R):
        for c in range(C):
            if M[r][c]=='S':
                return r,c


EXAMPLE = """..F7.
.FJ|.
SJ.L7
|F--J
LJ...
"""

EXAMPLE2=""".F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ...
"""

EXAMPLE3="""FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L
"""




def printm(data,pos=None):
    if pos is None:
        for x in data:
            print("".join(x))
        return
    r,c=pos
    R,C=len(data),len(data[0])
    mr=max(0,r-2)
    mc=max(0,c-2)
    Mr=min(R,r+3)
    Mc=min(C,c+3)
    for i in range(mr,Mr):
        print("".join(data[i][mc:Mc]))

def zoom_map(M):
    zoom={
        '|':("| ","| "),
        '-':("--","  "),
        'L':("L-","  "),
        'J':("J ","  "),
        'F':("F-","| "),
        '7':("7 ","| "),
        '.':(". ","  ")
    }
    R,C=len(M),len(M[0])
    NM=[[' ']*(2*C+1) for _ in range(2*R+1)]
    for i in range(R):
        for j in range(C):
            assert M[i][j]!='S'
            top,bot=zoom[M[i][j]]
            NM[2*i+1][2*j+1]=top[0]; NM[2*i+1][2*j+2]=top[1]
            NM[2*i+2][2*j+1]=bot[0]; NM[2*i+2][2*j+2]=bot[1]
    return NM

def readdata(data=None):
    """Read and parse the input data"""
    if data is None:
       with open("input10.txt") as f:
            data = f.read()
    return [list(x) for x in data.splitlines()]

def nextpos(M,history,current):
    r,c = current
    s = M[r][c]
    m1 = r+NEIG[s][0],c+NEIG[s][1]
    m2 = r+NEIG[s][2],c+NEIG[s][3]
    if m1==history:
        return m2
    else:
        return m1


def part1(data=None):
    """solve part 1"""
    M=readdata(data)
    R,C=len(M),len(M[0])
    sr,sc = findS(M)
    A=(0,0)
    B=(0,0)
    underS=type_of_S(M,sr,sc)
    neig=NEIG[underS]
    A = sr+neig[0],sc+neig[1]
    B = sr+neig[2],sc+neig[3]
    hB=hA=(sr,sc)
    dist=1
    while abs(A[0]-B[0]) + abs(A[1] - B[1])>1:
        # move A
        nA = nextpos(M,hA,A)
        hA,A = A, nA
        # move B
        nB = nextpos(M,hB,B)
        hB,B = B, nB
        dist+=1
    print(dist)

def flood(M):
    R,C=len(M),len(M[0])
    Q=[(0,0)]
    M[0][0]='X'
    idx=0
    while idx<len(Q):
        r,c=Q[idx]
        for d in [(+1, 0),(-1, 0),( 0,-1),( 0,+1)]:
            nr=r+d[0]
            nc=c+d[1]
            if nr<0 or nr>=R:
                continue
            if nc<0 or nc>=C:
                continue
            if M[nr][nc]=='X':
                continue
            M[nr][nc]='X'
            Q.append((nr,nc))
        idx+=1

def part2(data=None):
    """solve part 2"""
    M=readdata(data)
    R,C=len(M),len(M[0])
    sr,sc = findS(M)
    M[sr][sc]=type_of_S(M,sr,sc)
    Z=zoom_map(M)
    sr,sc = 2*sr+1,2*sc+1
    #printm(Z)
    FLOOD=[[' ']*(len(Z[0])) for _ in range(len(Z))]
    for i in range(1,len(Z),2):
        for j in range(1,len(Z[0]),2):
            FLOOD[i][j] = '.'
    hpos = sr,sc
    neig = NEIG[Z[sr][sc]]
    cpos = sr+neig[0],sc+neig[1]
    FLOOD[sr][sc]="X"
    while cpos!=(sr,sc):
        # move
        assert FLOOD[cpos[0]][cpos[1]] in '. '
        FLOOD[cpos[0]][cpos[1]]='X'
        npos = nextpos(Z,hpos,cpos)
        hpos,cpos = cpos, npos
    #printm(FLOOD)
    flood(FLOOD)
    #printm(FLOOD)
    cnt=0
    for i in range(len(Z)):
        for j in range(len(Z[0])):
            if FLOOD[i][j]=='.':
                cnt+=1
    print(cnt)

if __name__ == "__main__":
    part1(EXAMPLE)
    part1()
    part2(EXAMPLE2)
    part2(EXAMPLE3)
    part2()
