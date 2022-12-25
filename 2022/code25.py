"""Advent of Code 2022 day 25
"""

from collections import deque

EXAMPLE = """
1=-0-2
12111
2=0=
21
2=01
111
20012
112
1=-1=
1-12
12
1=
122
"""

digits = { '2':2, '1':1, '0':0, '-':-1, '=':-2}

def int2s(n):
    if n==0:
        return '0'
    chars = []
    while n!=0:
        r = "{}".format(n % 5)
        n = n // 5
        if r=='3':
            r  = "="
            n += 1
        elif r=='4':
            r  = "-"
            n += 1
        chars.append(r)
    return "".join(chars[::-1])

def s2int(snafu):
    value = 0
    for c in snafu:
        value = 5*value
        value += digits[c]
    return value

def readdata(data=None):
    """Read and parse the input data"""
    if data is None:
       with open("input25.txt") as f:
            data = f.read()
    data=data.splitlines()
    if len(data[-1])==0: data.pop()
    if len(data[0])==0: data.pop(0)
    return data


def part1(data=None):
    """solve part 1"""
    SNAFUS = readdata(data)
    x =sum(s2int(n) for n in SNAFUS)
    print("part1:",int2s(x))

if __name__ == "__main__":
    part1(EXAMPLE)
    part1()
