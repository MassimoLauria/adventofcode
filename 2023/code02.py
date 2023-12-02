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
        if line.isspace() or len(line)==0: continue
        line=line.replace(',',' ')
        s=line.find(":")
        segments=line[s+1:].split(';')
        segments=[s.split() for s in segments]
        games.append(segments)
    # clean
    for game in games:
        for j in range(len(game)):
            round = game[j]
            rgb=[0,0,0]
            for i in range(0,len(round),2):
                if round[i+1]=='red': rgb[0]=int(round[i])
                if round[i+1]=='green': rgb[1]=int(round[i])
                if round[i+1]=='blue': rgb[2]=int(round[i])
            game[j] = rgb
    return games

def part1(data=None):
    """solve part 1"""
    mr,mg,mb=12,13,14
    games=readdata(data)
    acc=0
    for gid,game in enumerate(games,start=1):
        good=True
        for r,g,b in game:
            if r>mr or g>mg or b>mb:
                good=False
        if good: acc+=gid
    print(acc)

def part2(data=None):
    """solve part 1"""
    games=readdata(data)
    s=0
    for gid,game in enumerate(games,start=1):
        mr = max(r for r,_,_ in game)
        mg = max(g for _,g,_ in game)
        mb = max(b for _,_,b in game)
        s +=mr*mg*mb
    print(s)


if __name__ == "__main__":
    part1(EXAMPLE)
    part1()
    part2(EXAMPLE)
    part2()
