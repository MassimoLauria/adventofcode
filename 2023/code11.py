"""Advent of Code 2023 day 11
"""

EXAMPLE = """...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....
"""

def readdata(data=None):
    """Read and parse the input data"""
    if data is None:
        with open("input11.txt") as f:
            data = f.read()
    data=data.splitlines()
    R=[0]*len(data[0])
    C=[0]*len(data)
    for i in range(len(data)):
        for j in range(len(data[0])):
            if data[i][j]=='#':
                R[i]+=1
                C[j]+=1
    return R,C

def distances_line(V,empty_space):
    N=sum(V)
    before=0
    total=0
    for i in range(len(V)):
        if V[i]==0:
            total+= empty_space*before*(N-before)
        else:
            total+= before*(N-before)
            before+=V[i]
    return total

def part12(empty_space,data=None):
    R,C=readdata(data)
    assert sum(R)==sum(C)
    totalr = distances_line(R,empty_space)
    totalc = distances_line(C,empty_space)
    print(totalr+totalc)


if __name__ == "__main__":
    part12(2,EXAMPLE,)
    part12(2,)
    part12(10,EXAMPLE)
    part12(100,EXAMPLE)
    part12(1000000)
