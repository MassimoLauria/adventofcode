"""Advent of Code 2023 day 14
"""

EXAMPLE = """O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....
"""

def printm(M):
    for l in M:
        print("".join(l))
    print()

def mhash(M):
    return tuple([''.join(l) for l in M])

def tilt(M,direction):
    R,C = len(M),len(M[0])
    if direction=='north':
        outerrange=range(C)
        innerrange=range(R)
        delta=+1
        coords=lambda o,i: (i,o)
    elif direction=='south':
        outerrange=range(C)
        innerrange=range(R-1,-1,-1)
        coords=lambda o,i: (i,o)
        delta=-1
    elif direction=='west':
        outerrange=range(R)
        innerrange=range(C)
        coords=lambda o,i: (o,i)
        delta=+1
    elif direction=='east':
        outerrange=range(R)
        innerrange=range(C-1,-1,-1)
        coords=lambda o,i: (o,i)
        delta=-1
    else:
        return

    for o in outerrange:
        fallpoint=innerrange[0]
        for i in innerrange:
            r,c = coords(o,i)
            if M[r][c]=='O':
                fr,fc=coords(o,fallpoint)
                M[r][c]='.'
                M[fr][fc]='O'
                fallpoint = fallpoint+delta
            elif M[r][c]=='#':
                fallpoint = i+delta

def readdata(data=None):
    """Read and parse the input data"""
    if data is None:
       with open("input14.txt") as f:
            data = f.read()
    data=data.splitlines()
    M=[list(x) for x in data]
    return M

def part1(data=None):
    M=readdata(data)
    tilt(M,'north')
    print(totalload(M))

def cycle(M):
    tilt(M,'north')
    tilt(M,'west')
    tilt(M,'south')
    tilt(M,'east')

def totalload(M):
    total=0
    R,C = len(M),len(M[0])
    for i in range(R):
        for j in range(C):
            if M[i][j]=='O':
                total+=(R-i)
    return total

def part2(data=None):
    """solve part 2"""
    CONFs={}
    M=readdata(data)
    CONFs[mhash(M)]=0
    for i in range(1,10**9+1):
        cycle(M)
        t=mhash(M)
        if t in CONFs:
            loopstart=CONFs[t]
            loopend=i
            break
        else:
            CONFs[t] = i
    loopsize=loopend-loopstart
    #print("Loop detected",loopstart,loopend)
    # for x in range(100):
    #     for i in range(loopsize):
    #         cycle(M)
    #     t2=mhash(M)
    #     assert t==t2
    cyclestodo=(10**9 - loopstart) % loopsize
    for i in range(cyclestodo):
        cycle(M)
    print(totalload(M))


if __name__ == "__main__":
    part1(EXAMPLE)
    part1()
    part2(EXAMPLE)
    part2()
