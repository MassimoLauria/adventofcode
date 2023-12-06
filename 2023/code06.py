"""Advent of Code 2023 day 06
"""
import math


EXAMPLE = """Time:      7  15   30
             Distance:  9  40  200"""

INPUT06 = """Time:        55     99     97     93
             Distance:   401   1485   2274   1405"""

def ways_win(time,record):
    delta = time*time - 4*(record+1)
    lower = (time - math.sqrt(delta)) / 2
    return time - 2*int(math.ceil(lower)) + 1

def part1(data):
    """solve part 1"""
    data=[x.split()[1:] for x in data.splitlines()]
    races=[ (int(data[0][i]),int(data[1][i])) for i in range(len(data[0])) ]
    print(math.prod(ways_win(t,r) for t,r in races ))

def part2(data):
    data=[x.split()[1:] for x in data.splitlines()]
    time   = int("".join(data[0]))
    record = int("".join(data[1]))
    print(ways_win(time,record))


if __name__ == "__main__":
    part1(EXAMPLE)
    part1(INPUT06)
    part2(EXAMPLE)
    part2(INPUT06)
