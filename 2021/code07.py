from math import ceil,floor

example="16,1,2,0,4,2,7,1,2,14"


def readdata(data=None):
    if data is None:
        with open("input07.txt") as f:
            data=f.read()
    return [int(x) for x in data.split(",")]

def linearcost(x,pos):
    acc=0
    for t in pos:
        acc += abs(x-t)
    return acc


def quadraticcost(x,pos):
    def f(n): return (n*n+n)//2
    acc=0
    for t in pos:
        acc += f(abs(x-t))
    return acc

def part1(data=None):
    pos=readdata(data)
    pos.sort()
    minp,maxp=min(pos),max(pos)
    costs=[(linearcost(x,pos),x) for x in range(minp,maxp+1)]
    print(min(costs))
    
def part2(data=None):
    """My solution was the stupid one,

but analysis would give you the best results within mean(positions) -1 and +1.
"""
    pos=readdata(data)
    mean = sum(pos)/len(pos)
    minp,maxp=ceil(mean-1.0),floor(mean+1.0)
    costs=[(quadraticcost(x,pos),x) for x in range(minp,maxp+1)]
    print(min(costs))
    
if __name__ == "__main__":
    part1(example)
    part1()
    part2(example)
    part2()