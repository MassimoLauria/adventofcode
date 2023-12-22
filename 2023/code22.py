"""Advent of Code 2023 day 22
"""

EXAMPLE = """1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9
"""

def readdata(data=None):
    """Read and parse the input data"""
    if data is None:
       with open("input22.txt") as f:
            data = f.read()
    blocks=[]
    for line in data.splitlines():
        block=line.split('~')
        A=list(map(int,block[0].split(',')))
        B=list(map(int,block[1].split(',')))
        blocks.append((A,B))
    return blocks



def part1(data=None):
    """solve part 1"""
    blocks=readdata(data)
    print(blocks)


if __name__ == "__main__":
    part1(EXAMPLE)
    # part1()
    # part2()
