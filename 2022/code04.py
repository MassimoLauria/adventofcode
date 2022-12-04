"""Advent of Code 2022 day 04
"""

EXAMPLE = """2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8
"""

def readdata(data=None):
    """Read and parse the input data"""
    if data is None:
       with open("input04.txt") as f:
            data = f.read()
    for line in data.splitlines():
        line = line.translate({ord("-"):","})
        yield [int(x) for x in line.split(',')]


def part1(data):
    """solve part 1"""
    score = 0
    for x1,y1,x2,y2 in data:
        x = min(x1,x2)
        y = max(y1,y2)
        if (x,y) in [(x1,y1),(x2,y2)]:
            score +=1
    print(score)

def part2(data):
    """solve part 2"""
    score = 0
    for x1,y1,x2,y2 in data:
        if not( x1 > y2 or x2 > y1 ):
            score +=1
    print(score)

if __name__ == "__main__":
    realinput = readdata()
    example = readdata(EXAMPLE)
    part1(example)
    part1(realinput)
    realinput = readdata()
    example = readdata(EXAMPLE)
    part2(example)
    part2(realinput)
