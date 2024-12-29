"""Advent of Code 2019 day 19
"""

from intcode import IntCode,IntCodeCPU

def part1():
    """solve part 1"""
    with open("input19.txt") as f:
        code = f.read()
    counter=0
    for i in range (5):
        for j in range(10):
            x=IntCode(code,[i,j])
            if x[0]==1:
                counter+=1
    a,b=0,1
    for i in range (5,50):
        a,b = beamcover(code, i, a, b-a)
        if a> 49:
            continue
        counter += min(50,b) -a

    print(f"Part1: {counter}")

def beamcover(code,x, ylb, difflb):
    if x<5:
        raise ValueError("No beam in this row")
    s=ylb
    # first start
    while IntCode(code,[x,s])[0]!=1:
        s+=1
    diff=difflb
    e = s+diff
    # find upper bound to end (via doubling)
    while IntCode(code,[x,e])[0]==1:
        e+=diff
        diff *=2
    # find end (via binary search)
    le=s
    re=e
    while re-le>1:
        mid = (le+re) // 2
        if IntCode(code,[x,mid])[0]==1:
            le = mid
        else:
            re = mid
    return s,re

def part2():
    """solve part 1"""
    with open("input19.txt") as f:
        code = f.read()
    N=100
    alpha,beta = beamcover(code, N, 0, 1)
    guessx = (N*100 + beta * 100) // (beta-alpha)
    value=0
    for x in range(guessx,guessx+20):
        blow,bhigh = beamcover(code, x-99, alpha*(x-99)//N, (beta-alpha)*(x-99) //N )
        alow,ahigh = beamcover(code, x, blow, bhigh-blow)
        if bhigh-alow == 100:
            value = (x-99)*10000 + alow
            break
        # check possible solution
    print(f"Part2: {value}")




if __name__ == "__main__":
    part1()
    part2()
