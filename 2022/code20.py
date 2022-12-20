"""Advent of Code 2022 day 20
"""

EXAMPLE = "1 2 -3 3 -2 0 4"

def readdata(data=None):
    """Read and parse the input data"""
    if data is None:
       with open("input20.txt") as f:
            data = f.read()
    return [int(x) for x in data.split() if len(x)!=0]

def movebeforeof(link,src,tgt):
    # extract src
    p,n = link[src]
    if tgt == n: return  # nothing to move
    link[p] = (link[p][0],n)
    link[n] = (p,link[n][1])
    # insert between p(tgt) and tgt
    ptgt = link[tgt][0]
    link[ptgt] = link[ptgt][0],src
    link[tgt]  = src,link[tgt][1]
    link[src]  = ptgt,tgt

def moverelative(link,i,offset):
    if offset == 0: return
    assert offset>0
    dir = 0 if offset<0 else 1
    t   = i
    offset = -offset if offset<0 else offset+1
    for _ in range(offset):
        t = link[t][dir]
    movebeforeof(link,i,t)

def print_llist(V,link,start=0):
    print(V[start], end="")
    p = link[start][1]
    N = len(V)
    while p!=start:
        print("",V[p], end="")
        p = link[p][1]
    print()


def mixer(multiplier,rounds,data=None):
    """decrypt"""
    V = readdata(data)
    assert V.count(0)==1
    N = len(V)
    V  = [ (v*multiplier) for v in V]
    sV = [ v % (N-1) for v in V]
    zero = V.index(0)
    link = []            # link at distance -+1

    for i in range(N):
        link.append( ((i-1) % N, (i+1) %N) )
    #print_llist(V,link)
    for _ in range(rounds):
        for i in range(N):
            moverelative(link,i, sV[i])
        #print_llist(V,link)
    res = 0
    i = zero
    assert V[i]==0
    for _ in range(1000 % N): i = link[i][1]
    res += V[i]
    for _ in range(1000 % N): i = link[i][1]
    res += V[i]
    for _ in range(1000 % N): i = link[i][1]
    res += V[i]
    print(res)

def part1(data=None):
    mixer(1,1,data)

def part2(data=None):
    mixer(811589153,10,data)

if __name__ == "__main__":
    part1(EXAMPLE)
    part1()
    part2(EXAMPLE)
    part2()
