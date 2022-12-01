


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
    print(max(s))


if __name__ == "__main__":
    aoc1part1()
