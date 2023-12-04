"""Advent of Code 2023 day 04
"""


EXAMPLE ="""Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
"""

def readdata(data=None):
    """Read and parse the input data"""
    if data is None:
       with open("input04.txt") as f:
            data = f.read()
    cards=[]
    data=data.splitlines()
    for line in data:
        win=[]
        nums=[]
        line=line.split()
        i=0
        while line[i]!='|': i+=1
        win = set(line[2:i])
        nums = set(line[i+1:])
        cards.append((win,nums))
    return cards

def part1(data=None):
    """solve part 1"""
    cards = readdata(data)
    acc=0
    for w,n in cards:
        s=len(w.intersection(n))
        if s>0:
            acc+=2**(s-1)
    print(acc)

def part2(data=None):
    """solve part 2"""
    cards = readdata(data)
    copies=[1]*len(cards)
    for i in range(len(cards)):
        w,n = cards[i]
        s=len(w.intersection(n))
        for j in range(i+1,i+s+1):
            copies[j]+=copies[i]
    print(sum(copies))


if __name__ == "__main__":
    part1(EXAMPLE)
    part1()
    part2(EXAMPLE)
    part2()
