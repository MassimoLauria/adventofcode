"""Advent of Code 2022 day 02
"""

EXAMPLE = """
A Y
B X
C Z
"""

def parsedata(data=None):
    D = {'A':0,'B':1,'C':2,'X':0,'Y':1,'Z':2,}
    if data is None:
        with open("input02.txt") as f:
            data=f.read()
    L=[]
    for s in data.splitlines():
        if len(s)!=0:
            L.append((D[s[0]],D[s[2]]))
    return L

def scores1(games):
    # p1,p2, pl2 outcome
    # 0 - 1 win
    # 0 - 2 lose
    # 1 - 2 win
    # 1 - 0 lose
    # 2 - 0 win
    # 2 - 1 lose
    # pl2 - pl1 (mod 3): 1 win, 2 lose, 0 draw
    outcome = {1:6,2:0,0:3}
    s = 0
    for a,b in games:
        s += outcome[(b-a) % 3]+ (b+1)
    return s

def scores2(games):
    # p2outcome
    # 0 lose, 1 draw, 2 win
    # p2 = (p1 + p2outcome-1) (mod 3)
    outcome = {1:6,2:0,0:3}
    s = 0
    for p1,p2outcome in games:
        p2 = (p1 + p2outcome-1) % 3
        s += p2outcome*3 + p2 +1
    return s

def part1(data=None):
    """solve part 1"""
    print(scores1(parsedata(data)))

def part2(data=None):
    """solve part 2"""
    print(scores2(parsedata(data)))


if __name__ == "__main__":
    part1(EXAMPLE)
    part1()
    part2(EXAMPLE)
    part2()
