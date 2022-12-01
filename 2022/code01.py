text="""
1000
2000
3000

4000

5000
6000

7000
8000
9000

10000
"""

def parsedata(data=None):
    if data is None:
        with open("input01.txt") as f:
            data=f.read()
    M=[]
    return data.splitlines()


def get_numbers(data=None):
    cal = [[]]
    for l in parsedata(data):
        if len(l) == 0:
            if  len(cal[-1])!=0:
                cal.append([])
        else:
            cal[-1].append(int(l))
    return cal

def aoc1part1(data=None):
    s=[]
    for x in get_numbers(data):
        s.append(sum(x))
    return max(s)

def aoc1part2(data=None):
    v = 0
    s = [-1,-1,-1]
    for l in parsedata(data)+['']:
        if len(l) != 0:
            v += int(l)
            continue
        if v==0:
            continue
        if v > s[0]:
            s.insert(0,v)
        elif v > s[1]:
            s.insert(1,v)
        elif v > s[2]:
            s.insert(2,v)
        else:
            s.append(v)
        s.pop()
        v = 0
    return sum(s)

if __name__ == "__main__":
    print(aoc1part1(text))
    print(aoc1part1())
    print(aoc1part2(text))
    print(aoc1part2())
