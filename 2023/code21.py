"""Advent of Code 2023 day 21
"""

EXAMPLE = """...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........
"""

def printm(M):
    for x in M:
        print("".join(x))


def readdata(data=None):
    """Read and parse the input data"""
    if data is None:
       with open("input21.txt") as f:
            data = f.read()
    M = [list(x) for x in data.splitlines()]
    for r in range(len(M)):
        for c in range(len(M[0])):
            if M[r][c]=='S':
                return r,c,M

def part1(data=None):
    """solve part 1"""
    sr,sc,M=readdata(data)
    R,C=len(M),len(M[0])


if __name__ == "__main__":
    part1(EXAMPLE)
    part1()
    # part2()
