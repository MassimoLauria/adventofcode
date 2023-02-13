"""Advent of Code 2015 day 01
"""

EXAMPLE = """
"""

def readdata(data=None):
    """Read and parse the input data"""
    if data is None:
       with open("input01.txt") as f:
            data = f.read()
    return data


def part1(data=None):
    """solve part 1"""
    data=readdata().strip()
    A  = data.count('(')
    B  = data.count(')')
    print(A-B)

def part2(data=None):
    """solve part 1"""
    data=readdata().strip()
    cnt=0
    vals = [ -1 if c==')' else +1 for c in data ]
    i = 0
    for v in vals:
        cnt += v
        i   += 1
        if cnt==-1:
            break
    print(i)



if __name__ == "__main__":
    part1()
    part2()
