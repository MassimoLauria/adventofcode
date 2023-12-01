"""Advent of Code 2023 day 01
"""

EXAMPLE = """
1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet
"""

EXAMPLE2 = """
two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen
"""


digits = { 'one':1, 'two':2, 'three':3, 'four':4, "five":5,
           'six':6, "seven":7, 'eight':8, 'nine':9}

def readdata(data=None):
    """Read and parse the input data"""
    if data is None:
       with open("input01.txt") as f:
            data = f.read()
    return data


def part1(data=None):
    """solve part 1"""
    testo=readdata(data)
    linee=testo.splitlines()
    acc=0
    for l in linee:
        dgts = [int(c) for c in l if c.isdigit()]
        if len(dgts)<1: continue
        v = dgts[0]*10 + dgts[-1]
        acc += v
    print(acc)

def findfirst(text,patterns):
    best = None
    end  = len(text)
    for k in patterns:
        pos = text.find(k,0,end)
        if pos!=-1:
            best = k
            end  = pos +len(k) - 1
    return patterns[best]

def part2(data=None):
    """solve part 2"""

    digits = { 'one':1, 'two':2, 'three':3, 'four':4, "five":5,
           'six':6, "seven":7, 'eight':8, 'nine':9}
    revdigits = {}

    testo=readdata(data)
    linee=testo.splitlines()
    # Prepare the patterns
    for i in range(1,10):
        digits[str(i)]=i
        revdigits[str(i)]=i
    # Reverse digits
    for k in digits:
        revdigits[k[::-1]] = digits[k]

    acc=0
    for l in linee:
        if len(l.strip()) == 0: continue

        A = findfirst(l,digits)
        B = findfirst(l[::-1],revdigits)
        acc += A*10 + B
    print(acc)


if __name__ == "__main__":
    part1(EXAMPLE)
    part1()
    part2(EXAMPLE2)
    part2()
