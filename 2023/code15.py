"""Advent of Code 2023 day 15
"""

EXAMPLE = "rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"


def HASH(string):
    h=0
    for c in string:
        x = ord(c)
        assert 0<=x<128
        h+=x
        h*=17
        h%=256
    return h

def readdata(data=None):
    """Read and parse the input data"""
    if data is None:
       with open("input15.txt",encoding='ascii') as f:
            data = f.read().strip()
    return data.split(',')

def focusing_power(boxes,lenses):
    power=0
    for i in range(len(boxes)):
        for j in range(len(boxes[i])):
            power += (i+1)*(j+1)*lenses[boxes[i][j]]
    return power

def part1(data=None):
    """solve part 1"""
    print(sum([HASH(s) for s in readdata(data)]))

def part2(data=None):
    boxes=[[] for _ in range(256)]
    lenses={}
    for s in readdata(data):
        if s[-1]=="-":
            lens=s[:-1]
            if lens in lenses:
                box=HASH(lens)
                lenses.pop(lens)
                boxes[box].remove(lens)
        else:
            eq=s.find('=')
            lens=s[:eq]
            box=HASH(lens)
            if lens not in lenses:
                boxes[box].append(lens)
            lenses[lens]=int(s[eq+1:])
    #print(boxes,lenses)
    print(focusing_power(boxes,lenses))

if __name__ == "__main__":
    part1(EXAMPLE)
    part1()
    part2(EXAMPLE)
    part2()
