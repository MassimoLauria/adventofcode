"""Advent of Code 2022 day 13
"""

from functools import cmp_to_key
import ast

EXAMPLE = """
[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]
"""

def readdata(data=None):
    """Read and parse the input data"""
    if data is None:
       with open("input13.txt") as f:
            data = f.read()
    Pairs=[]
    i = 0
    data=data.splitlines()
    while i < len(data):
        if len(data[i])==0:
            i+=1
        left  = ast.literal_eval(data[i])
        right = ast.literal_eval(data[i+1])
        Pairs.append((left,right))
        i+=2
    return Pairs


def cmp(left,right):
    if type(left)==type(right)==int:
        if left<right:
            return -1
        elif left==right:
            return 0
        else:
            return 1
    if type(left)==int:
        return cmp([left],right)
    if type(right)==int:
        return cmp(left,[right])
    s = min(len(left),len(right))
    i = 0
    while(i<s):
        r = cmp(left[i],right[i])
        if r!=0:
            return r
        i += 1
    return cmp(len(left),len(right))



def part1(data=None):
    """solve part 1"""
    Pairs = readdata(data)
    res=0
    for i in range(len(Pairs)):
        if cmp(*Pairs[i])==-1:
            res += (i+1)
    print("part1:", res)

def part2(data=None):
    """solve part 2"""
    Pairs = readdata(data)
    Packets = [ [[2]], [[6]] ]
    for l,r in Pairs:
        Packets.append(l)
        Packets.append(r)
    Packets.sort(key=cmp_to_key(cmp))
    a = Packets.index([[2]])
    b = Packets.index([[6]])
    print("part2:", (a+1)*(b+1))


if __name__ == "__main__":
    part1(EXAMPLE)
    part1()
    part2(EXAMPLE)
    part2()
