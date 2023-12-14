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

def readdata(data=None):
    """Read and parse the input data"""
    if data is None:
       with open("input14.txt") as f:
            data = f.read()
    data=data.splitlines()
    M=[list(x) for x in data]
    return M


def part1(data=None):
    """solve part 1"""
    M=readdata(data)
    R,C = len(M),len(M[0])
    totalload=0
    for j in range(C):
        nextload=R
        i=0
        while i<R:
            if M[i][j]=='O':
                totalload+=nextload
                nextload-=1
            elif M[i][j]=='#':
                nextload=R-i-1
            i+=1
    print(totalload)
    #printm(M)


if __name__ == "__main__":
    part1(EXAMPLE)
    part1()
    # part2()
