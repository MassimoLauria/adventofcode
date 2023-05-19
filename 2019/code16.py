"""Advent of Code 2019 day 16
"""

import numpy as np

BASE = np.array([0,1,0,-1])


def offset_list_of_digits(text):
    skip=int(text[:7])
    assert skip<len(text)*10000<2*skip
    return [ int(x) for x in text]


def opmatrix(n):
    M = np.zeros((n,n),dtype=np.int32)
    for i in range(n):
        for j in range(n):
            M[i,j] = BASE[((j+1)//(i+1)) % 4]
    return M

EXAMPLES = [
    #part1
    '80871224585914546619083218645595',
    '19617804207202209144916044189917',
    '69317163492948606335995924319873',
    #part2
    '03036732577212944063491565474664',
    '02935109699940807407585447034323',
    '03081770884921959731165446850517']

def readdata(data=None):
    """Read and parse the input data"""
    if data is None:
       with open("input16.txt") as f:
            data = f.read()
    return data.strip()


def part1(text,phases=100):
    """solve part 1"""
    v = np.array([ int(x) for x in text],dtype=np.int32)
    M = opmatrix(len(v))
    for _ in range(phases):
        v = np.abs(M@v) % 10
    return "".join(str(v[i]) for i in range(8))

def part2(text,phases=100):
    """solve part 2

    observe that the next vector digits at pos >= N only depend
    on the previous vector digits at pos >= N

    for our data skip < len(digit) <2*len(digit) hence the last
    digit of the fft of the vector means just sum all elements from
    position skip to the end of the previous vector.

    1. We kill all elements of pos<skip.
    2. We compute the shifted cumulative sums
       - by having [1,1,1,....] cumulative summed 99 times into B
       - output digit x is inner product between input and
         B shifted by x positions to the right
    """
    skip = int(text[:7])
    assert skip < len(text)*10000 <= 2*skip+1
    digits = [int(x) for x in text]*10000
    digits = digits[skip:]
    plen    = len(digits)

    for _ in range(phases):
        total = sum(digits)
        t  = 0
        for i in range(plen):
            t = digits[i]
            digits[i] = total % 10
            total -= t

    return "".join(str(digits[i]) for i in range(8))


if __name__ == "__main__":
    print("Example 1:",part1(EXAMPLES[0])) #  24176176
    print("Example 2:",part1(EXAMPLES[1])) #  73745418
    print("Example 3:",part1(EXAMPLES[2])) #  52432133
    print("part1    :",part1(readdata()) ) #  34841690
    print("Example 4:",part2(EXAMPLES[3])) #  84462026
    print("Example 5:",part2(EXAMPLES[4])) #  78725270
    print("Example 6:",part2(EXAMPLES[5])) #  53553731
    print("part2    :",part2(readdata()))  #  48776785
