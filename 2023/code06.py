"""Advent of Code 2023 day 06
"""

EXAMPLE = """
Time:      7  15   30
Distance:  9  40  200
"""

INPUT06 = """
Time:        55     99     97     93
Distance:   401   1485   2274   1405
"""

def readdata(data):
    """Read and parse the input data"""
    data=data.split()
    t=[]
    d=[]
    for i in range(1,len(data)//2):
        t.append(int(data[i]))
        d.append(int(data[i+len(data)//2]))
    return t,d


def part1(data):
    """solve part 1"""
    time,distance=data
    print(time,distance)

if __name__ == "__main__":
    EXAMPLE = readdata(EXAMPLE)
    INPUT06 = readdata(INPUT06)
    part1(EXAMPLE)
    part1(INPUT06)
    # part1()
    # part2()
