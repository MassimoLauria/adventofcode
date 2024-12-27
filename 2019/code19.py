"""Advent of Code 2019 day 19
"""

from intcode import IntCode,IntCodeCPU

def part1():
    """solve part 1"""
    with open("input19.txt") as f:
        code = f.read()
    counter=0
    for i in range (50):
        for j in range(50):
            x=IntCode(code,[i,j])
            if x[0]==1:
                print('#',end="")
                counter+=1
            else:
                print('.',end="")
        print()
    print(f"Part1: {counter}")

def part2():
    """solve part 1"""
    with open("input19.txt") as f:
        code = f.read()
    counter=0
    sj=0
    ej=0
    ends=[]
    for i in range (4,1000):
        while True:
            x=IntCode(code,[i,sj])
            if x[0]==1:
                break
            sj+=1
        while True:
            x=IntCode(code,[i,ej+1])
            if x[0]==0:
                break
            sj+=1


    print(f"Part1: {counter}")




if __name__ == "__main__":
    part1()
    part2()
