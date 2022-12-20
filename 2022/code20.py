"""Advent of Code 2022 day 20
"""

EXAMPLE = "1 2 -3 3 -2 0 4"

def readdata(data=None):
    """Read and parse the input data"""
    if data is None:
       with open("input20.txt") as f:
            data = f.read()
    return [int(x) for x in data.split() if len(x)!=0]

def movebeforeof(linked_list,src,tgt):
    left,right = linked_list
    # extract src
    p,n = left[src],right[src]
    if tgt == n: return  # nothing to move
    right[p] = n
    left [n] = p
    # insert between p(tgt) and tgt
    ptgt = left[tgt]
    right[ptgt] = src
    left [src]  = ptgt
    left [tgt]  = src
    right[src]  = tgt

def moverelative(linked_list,i,offset):
    _,right = linked_list
    if offset == 0: return
    assert offset>0
    target = right[i]
    for _ in range(offset):
        target = right[target]
    movebeforeof(linked_list,i,target)

def print_llist(V,linked_list,start=0):
    left,right = linked_list
    print(V[start], end="")
    p = right[start]
    N = len(V)
    while p!=start:
        print("",V[p], end="")
        p = right[p]
    print()


def mixer(multiplier,rounds,data=None):
    """decrypt"""
    V = readdata(data)
    assert V.count(0)==1
    N = len(V)
    V  = [ (v*multiplier) for v in V]
    sV = [ v % (N-1) for v in V]
    zero = V.index(0)
    left,right = [],[] # links at distance -+1
                       # a list of left links and right links

    for i in range(N):
        left.append ((i-1) %N)
        right.append((i+1) %N)
    linked_list = (left,right)
    #print_llist(V,link)
    for _ in range(rounds):
        for i in range(N):
            moverelative(linked_list,i, sV[i])
    res = 0
    i = zero
    assert V[i]==0
    for _ in range(1000 % N): i = right[i]
    res += V[i]
    for _ in range(1000 % N): i = right[i]
    res += V[i]
    for _ in range(1000 % N): i = right[i]
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
