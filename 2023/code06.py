"""Advent of Code 2023 day 06
"""
import math


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
    races=[]
    for i in range(1,len(data)//2):
        races.append((int(data[i]),int(data[i+len(data)//2])))
    return races

def ways_win(time,record):
    Delta = time*time - 4*(record+1)
    assert Delta>0
    start = (time - math.sqrt(Delta)) / 2
    start = int(math.ceil(start))
    assert start*(time-start)>0
    return time - 2*start + 1

def part1(data):
    """solve part 1"""
    data=data.split()
    races=[]
    for i in range(1,len(data)//2):
        races.append((int(data[i]),int(data[i+len(data)//2])))
    acc=1
    for time,record in races:
        acc*=ways_win(time,record)
    print(acc)

def part2(data):
    data=data.split()
    time=[]
    record=[]
    for i in range(1,len(data)//2):
        time.append(data[i])
        record.append(data[i+len(data)//2])
    time=int("".join(time))
    record=int("".join(record))
    print(ways_win(time,record))


if __name__ == "__main__":
    part1(EXAMPLE)
    part1(INPUT06)
    part2(EXAMPLE)
    part2(INPUT06)
