"""Advent of Code 2019 day 17
"""

from intcode import IntCode,IntCodeCPU
from collections import defaultdict
from pprint import pprint


def part1():
    """solve part 1"""
    with open("input17.txt") as f:
        data = IntCode(f.read(),[])
    newline = 10
    empty = 46
    width  = data.index(newline) + 1
    height = len(data)  // width
    total = 0
    for i in range(0,height-1):
        for j in range(1,width-2):
            ptr = width*i+j
            res = [data[ptr+t]!=empty for t in [0,-1,+1,-width,+width]]
            if sum(res)==5:
                total += i*j
    print(f"Part1: {total}")

def get_directions(M,i,j):
    diamond = [ (-1,0), (0,1), (1,0), (0,-1) ] # clockwise
    directions = []
    empty = 46
    for di,dj in diamond:
        if not ((0<= i+di < len(M)) and (0<= j+dj < len(M[0]))): continue
        if M[i+di][j+dj]!= empty:
            directions.append((di,dj))
    return directions[:]

def turn_head(od,nd):
    """assumptions: od and nd cannot be opposite directions
    """
    odi,odj = od
    ndi,ndj = nd
    if ndi== odj and ndj==-odi: return 'R'
    if ndi==-odj and ndj== odi: return 'L'
    return None

def build_graph(M,source):
    diamond = [ (-1,0), (0,1), (1,0), (0,-1) ] # clockwise
    empty = 46
    full  = 35
    G = defaultdict(dict)
    W = defaultdict(dict)
    si,sj = source  # source

    # Start the walk
    exits = { (si,sj) : get_directions(M,si,sj) } # exit available
    ai,aj = si,sj
    while True:

        # Depart (we always depart some known vertex)
        # print(ai,aj)
        # print(exits[ai,aj])
        assert len(exits[ai,aj])>0
        di,dj = exits[ai,aj].pop()            # leave via some direction
        if len(exits[ai,aj])==0:
            exits.pop((ai,aj))
        departure = ((ai,aj),(di,dj))
        # print("Leave", departure)

        # Walk the degree two vertices
        walk=[1]
        bi,bj = ai+di,aj+dj
        dirs = get_directions(M,bi,bj)
        while len(dirs)==2:
            dirs.remove((-di,-dj))
            od    = di,dj
            di,dj = dirs[0]
            turn = turn_head(od,(di,dj))
            if turn is not None:
                walk.extend([turn,0])
            walk[-1] += 1
            bi,bj = bi+di,bj+dj
            dirs = get_directions(M,bi,bj)

        # Arrival
        arrival = (bi,bj),(-di,-dj)
        G[departure[0]][departure[1]] = arrival
        W[departure[0]][departure[1]] = walk[:]
        G[arrival[0]][arrival[1]] = departure
        W[arrival[0]][arrival[1]] = []
        for w in walk[::-1]:
            if w == 'L':
                W[arrival[0]][arrival[1]].append('R')
            elif w == 'R':
                W[arrival[0]][arrival[1]].append('L')
            else:
                W[arrival[0]][arrival[1]].append(w)

        # print("Arriving", arrival)

        if (bi,bj) not in exits:  # an unknown vertex
            exits[bi,bj] = dirs
        exits[bi,bj].remove((-di,-dj))   # used to arrive
        if len(exits[bi,bj])==0:
            exits.pop((bi,bj))

        # if the current vertex has exit we continue, otherwise we
        # pick another one with exits.
        if (bi,bj) in exits:
            assert len(exits[bi,bj])>0
            ai,aj = bi,bj
        elif len(exits)>0:
            ai,aj = next(iter(exits))
        else:
            return G,W
        # print("next departure", (ai,aj))


def expand_walk(G,W,walk):
    assert len(walk)>=5
    assert len(walk) % 3 == 2
    data = []
    for i in range(1,len(walk)-1,3):
        od,v,nd = walk[i-1],walk[i],walk[i+1]
        odi,odj = od
        turn = turn_head((-odi,-odj),nd)
        if turn is not None:
            data.append(turn)
        data.extend(W[v][nd])
    return (data)

def enumerate_eulerian_walks(G,W,source,walk=None,unused=None):
    if walk is None:
        walk = [(1,0),source] # arrival from below
    if unused is None:
        unused = { (s,sdir) for s in G for sdir in G[s]}

    # End of recursion
    if len(unused)==0:
        yield ",".join(str(x) for x in expand_walk(G,W,walk))
        return

    # Try to make the walk longer, if possible
    s = walk[-1]
    for sdir in G[s]:
        if (s,sdir) not in unused:
            continue
        u,udir = G[s][sdir]
        assert (u,udir) in unused
        unused.remove((s,sdir))
        unused.remove((u,udir))
        walk.append(sdir)
        walk.append(udir)
        walk.append(u)
        yield from enumerate_eulerian_walks(G,W,source,walk,unused)
        unused.add((s,sdir))
        unused.add((u,udir))
        walk.pop()
        walk.pop()
        walk.pop()


def apply_walk(orig,p):
    clone = [l[:] for l in orig]
    code ="""
    A
    {}
    L,R
    L,R
    """.format(p)
    _,M,A,B,C,_ = code.splitlines()
    F = { 'M':M.strip().split(","),
        'A':A.strip().split(","), 'B':B.strip().split(","), 'C': C.strip().split(",")}
    print(F)
    starting_points = [(28,12,0)]
    directions = [ (-1,0), (0,1), (1,0), (0,-1) ]
    for ai,aj,dirs in starting_points:
        for f in F['M']:
            actions = F[f]
            for i in range(len(actions)):
                a = actions[i]
                if a=='L':
                    dirs = (dirs + 3) % 4
                elif a=='R':
                    dirs = (dirs + 1) % 4
                else:
                    n = int(a)
                    di,dj = directions[dirs]
                    for i in range(n):
                        clone[ai][aj] = ord(f)
                        ai,aj = ai+di,aj+dj
        clone[ai][aj] = ord("^>v<"[dirs])
    for i in range(len(clone)):
        print(bytes(orig[i]).decode('ascii'),end="")
        print("     ",end="")
        print(bytes(clone[i]).decode('ascii'))
    print(p)

def part2(data=None):
    """solve part 2"""

    # read and clean data
    with open("input17.txt") as f:
        raw = IntCode(f.read(),[])
    newline = 10
    width = raw.index(newline) + 1
    raw.pop() # get rid of last newline
    land = [ raw[i:i+width-1] for i in range(0,len(raw),width) ]

    # make the graph
    source = (28,12)
    G,W = build_graph(land,source)

    # Find walks
    cnt=0
    for w in enumerate_eulerian_walks(G,W,source):
        cnt+=1
        apply_walk(land,w)
        print(w)
    print(cnt)

    # go to I/O mode
    # assert code[0]=='1'
    # code='2'+code[1:]
    # CPU = IntCodeCPU(code)
    #CPU.interactive()

    # while True:

    #     CPU.run()
    #     odata = CPU.get_output()
    #     if odata[-1]>255:
    #         res   = odata[-1]
    #         odata = odata[:-1]
    #         assert CPU.status=="HALT"

    #     print(bytes(odata).decode('ascii'))
    #     if CPU.status=="HALT": break

    #     CPU.flush_output()
    #     idata=input(CPU.status+" >")
    #     if len(idata)>20:
    #         print("Input must be at most 20 chars")
    #         break
    #     CPU.add_input(idata+'\n')

if __name__ == "__main__":
    part1()
    part2()
