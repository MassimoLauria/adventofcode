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
        a,b = beamcover(code, i, a)
        if a> 49:
            continue
        counter += min(50,b) -a

    print(f"Part1: {counter}")

def beamcover(code,x, ylb):
    if x<5:
        raise ValueError("No beam in this row")
    alpha=ylb
    # first start
    while IntCode(code,[x,alpha])[0]!=1:
        alpha+=1
    diff=1
    beta = alpha+1
    # find upper bound to end (via doubling)
    while IntCode(code,[x,beta])[0]==1:
        beta += diff
        diff *=2
    # find end (via binary search)
    lowbeta=alpha
    while beta-lowbeta>1:
        mid = (beta+lowbeta) // 2
        if IntCode(code,[x,mid])[0]==1:
            lowbeta = mid
        else:
            beta = mid
    return alpha,beta

def part2():
    """solve part 2"""
    with open("input19.txt") as f:
        code = f.read()
    N=100
    alpha,beta = beamcover(code, N, 0)
    x = (N*100 + beta * 100) // (beta-alpha) - 99  # first guess for the solution
    while True:
        blow,bhigh = beamcover(code, x, alpha*x//N )
        alow,_ = beamcover(code, x+99, blow)
        if bhigh-alow == 100:
            break
        x+=1
    print(f"Part2: {x*10000 + alow}")




if __name__ == "__main__":
    part1()
    part2()
