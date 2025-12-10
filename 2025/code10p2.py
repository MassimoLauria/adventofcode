"""
Advent of Code 2025 day 10
"""

from z3 import *


example = """
[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}
"""


def solve_system(line):
    comp=line.split()
    N = len(comp[0])-2
    M = len(comp)-2
    b = comp[-1][1:-1].split(',')
    b = [int(x) for x in b]
    A = [[ int(y) for y in x[1:-1].split(',')] for x in comp[1:-1]]
    Ar = [ [j for j in range(M) if i in A[j] ] for i in range(N)]
    X=[Int('x{}'.format(j)) for j in range(M)]

    pos = [x>=0 for x in X ]
    lines = [ sum(X[j] for j in Ar[i]) == b[i] for i in range(N) ]

    def test_limit(v):
        Z  = Solver()
        Z.add(pos+lines)
        Z.add([sum(X)<=v])
        return Z.check()==sat

    s = 0
    e = sum(b)
    while e-s>1:
        mid = (s+e)//2
        if test_limit(mid):
            e = mid
        else:
            s = mid
    return e


if __name__ == "__main__":
    resE=0
    for line in example.strip().splitlines():
        resE+=solve_system(line)
    print("Part2 example  :",resE)

    with open("input10.txt") as f:
        text=f.read()
        resC=0
    for line in text.strip().splitlines():
        resC+=solve_system(line)
    print("Part2 challenge:",resC)
