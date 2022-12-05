"""Advent of Code 2022 day 05
"""

EXAMPLE="""    [D]
[N] [C]
[Z] [M] [P]
 1   2   3

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
"""


def readdata(data=None):
    """Read and parse the input data"""
    if data is None:
        with open("input05.txt") as f:
            data = f.read()
    data=data.splitlines()
    first=0
    while True:
        if data[first][:4]=="move":
            break
        first += 1

    # Load stacks
    stacknum=len(data[first-2].split())
    stacks=[[] for _ in range(stacknum+1)]
    for v in range(first-3,-1,-1):
        h = 1
        while 4*h-2 < len(data[v]):
            c = data[v][4*h-3]
            if c!=" ":
                stacks[h].append(c)
            h += 1

    # Moves
    moves=[]
    for i in range(first,len(data)):
        inst=data[i].split()
        mv = (int(inst[1]),int(inst[3]),int(inst[5]))
        moves.append(mv)
    return stacks,moves


def part1(data=None):
    """solve part 1"""
    stacks, moves = readdata(data)
    for many,src,dst in moves:
        for i in range(many):
            x = stacks[src].pop()
            stacks[dst].append(x)
    tops=[ stacks[i][-1] for i in range(1,len(stacks)) ]
    print("".join(tops))

def part2(data=None):
    """solve part 2"""
    stacks, moves = readdata(data)
    for many,src,dst in moves:
        for i in range(many):
            x = stacks[src].pop()
            stacks[0].append(x)
        for i in range(many):
            x = stacks[0].pop()
            stacks[dst].append(x)
    tops=[ stacks[i][-1] for i in range(1,len(stacks)) ]
    print("".join(tops))

if __name__ == "__main__":
    part1(EXAMPLE)
    part1()
    part2(EXAMPLE)
    part2()
