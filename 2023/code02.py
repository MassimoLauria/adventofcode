"""Advent of Code 2023 day 02
"""

import numpy as np

EXAMPLE = """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
"""

def readdata(data=None):
    """Read and parse the input data"""
    if data is None:
       with open("input02.txt") as f:
            data = f.read()
    lines=data.splitlines()
    games=[]
    for line in lines:
        line=line.split()
        if len(line)<2: continue
        gdata=[]
        for i in range(2,len(line),2):
            gdata.append((line[i+1][0],int(line[i])))
        games.append(gdata)
    # clean
    return games

def part1(data=None):
    """solve part 1"""
    mrgb={'r':12,'g':13,'b':14}
    games=readdata(data)
    acc=0
    good=True
    for gid,game in enumerate(games,start=1):
        good=True
        for c,v in game:
            if v>mrgb[c]: good=False
        if good: acc+=gid
    print(acc)

def part2(data=None):
    """solve part 1"""
    games=readdata(data)
    s=0
    for gid,game in enumerate(games,start=1):
        m={'r':0,'g':0,'b':0}
        for c,v in game:
            m[c]=max(v,m[c])
        s +=m['r']*m['g']*m['b']
    print(s)


if __name__ == "__main__":
    print(readdata(EXAMPLE))
    part1(EXAMPLE)
    part1()
    part2(EXAMPLE)
    part2()
