"""Advent of Code 2023 day 09
"""

EXAMPLE = """0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45
"""

def readdata(data=None):
    """Read and parse the input data"""
    if data is None:
       with open("input09.txt") as f:
            data = f.read()
    nums=[]
    for linea in data.splitlines():
        nums.append([int(x) for x in linea.split()])
    return nums

def next_value(V):
    N=len(V)
    steps=1
    all_zero=False
    value=0
    while not all_zero:
        all_zero=True
        value+=V[N-steps]
        for i in range(N-steps):
            V[i]=V[i+1]-V[i]
            if V[i]!=0: all_zero=False
        steps+=1
    return value

def part1(data=None):
    """solve part 1"""
    nums=readdata(data)
    acc=0
    size=len(nums[0])
    for x in nums:
        assert size==len(x)
        acc += next_value(x)
    print(acc)

def part2(data=None):
    """solve part 2"""
    nums=readdata(data)
    acc=0
    size=len(nums[0])
    for x in nums:
        assert size==len(x)
        acc += next_value(x[::-1])
    print(acc)


if __name__ == "__main__":
    part1(EXAMPLE)
    part1()
    part2(EXAMPLE)
    part2()
