"""Advent of Code 2019 day 16
"""

import numpy as np

BASE = np.array([0,1,0,-1])

def gdc(a,b):
    if a>b: a,b = b,a
    while (a!=0):
        a,b = (b % a), a
    return b

def lcm(a,b):
    return (a*b)//gdc(a,b)

def list_of_digits(text):
    return np.array([ int(x) for x in text],dtype=np.int32)

def opmatrix(n):
    M = np.zeros((n,n),dtype=np.int32)
    for i in range(n):
        for j in range(n):
            M[i,j] = BASE[((j+1)//(i+1)) % 4]
    return M



def next(v,vlen,i):
    #wavelet_len = 4*(i+1)
    #ip_range    = min(vlen,lcm(len(v),wavelet_len))
    #repetitions = vlen // ip_range
    #repetitions = max(repetitions,1)
    repetitions = 1
    t = i  # all positions before i are zeros
    val = 0
    while t<vlen:
        if BASE[((t+1)//(i+1)) % 4]==0:
            t += (i+1)
            continue
        val += v[t%len(v)]*BASE[((t+1)//(i+1)) % 4]
        t +=1
    return abs(val*repetitions) % 10

EXAMPLES = [
    #list_of_digits('12345678'),
    list_of_digits('80871224585914546619083218645595'),
    list_of_digits('19617804207202209144916044189917'),
    list_of_digits('69317163492948606335995924319873')]

def readdata(data=None):
    """Read and parse the input data"""
    if data is None:
       with open("input16.txt") as f:
            data = f.read()
    return list_of_digits(data.strip())


def part1(v,phases=100):
    """solve part 1"""
    #print(len(signal))
    #print(signal[0:3],"...",signal[-3:])
    M = opmatrix(len(v))
    #print(M)
    #print(v)
    for _ in range(phases):
        v = np.abs(M@v) % 10
    return "".join(str(v[i]) for i in range(8))

def part2(v,phases=100,repeat=1):
    """solve part 2"""
    #print(len(signal))
    #print(signal[0:3],"...",signal[-3:])
    # vlen = len(v)*repeat
    src = list(v)*repeat
    dst = [0]*len(src)
    return "".join(str(v[i]) for i in range(8))


def nextvec(src,dst):
    assert len(src)==len(dst)
    b = 0 - 1j
    for j in range(len(dst)):
        dst[j] = 0
        for i in range(len(src)):
            dst[j] += src[i] * (b**(3+(i+1)//(j+1)))
        dst[j] = int(abs(dst[j].real))%10


if __name__ == "__main__":
    print("Example 1:",part1(EXAMPLES[0])) #  24176176
    print("Example 2:",part1(EXAMPLES[1])) #  73745418
    print("Example 3:",part1(EXAMPLES[2])) #  52432133
    print("part1    :",part1(readdata()))  #  34841690
    #print("Example 1:",part2(EXAMPLES[0],repeat=1)) #
    #print("Example 2:",part2(EXAMPLES[1])) #
    #print("Example 3:",part2(EXAMPLES[2])) #
    #print("part2    :",part2(readdata()))  #
