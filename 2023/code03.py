"""Advent of Code 2023 day 03
"""

from collections import defaultdict

EXAMPLE = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
"""

def readdata(data=None):
    """Read and parse the input data"""
    if data is None:
       with open("input03.txt") as f:
            data = f.read()
    data=data.splitlines()
    R=len(data)
    C=len(data[0])
    assert len(data[0])==len(data[-1])
    assert R*C !=0
    assert not data[-1][-1].isdigit()
    return data

def capture_from_first_digit(M,i,j):
    R,C=len(M),len(M[0])

    def ins(i,j):
        return i>=0 and i<R and j>=0 and j<C

    # find the part
    je=j+1
    while ins(i,je) and M[i][je].isdigit() : je+=1
    part=(i,j,je,int(M[i][j:je]))

    symbols=[]

    # connect it to symbols
    for a in range(j-1,je+1):
        if ins(i-1,a) and M[i-1][a]!='.':
            symbols.append((i-1,a,M[i-1][a]))
        if ins(i+1,a) and M[i+1][a]!='.':
            symbols.append((i+1,a,M[i+1][a]))
    if ins(i,j-1) and M[i][j-1]!='.':
        symbols.append((i,j-1,M[i][j-1]))
    if ins(i, je) and M[i][je ]!='.':
        symbols.append((i,je,M[i][je]))

    return part,symbols

def load_parts(data):
    data=readdata(data)
    R=len(data)
    C=len(data[0])
    parts=defaultdict(list)
    for i in range(R):
        j=0
        while j < C:
            if data[i][j].isdigit():
                part,sym=capture_from_first_digit(data,i,j)
                parts[part]=sym
                j=part[2]
            j+=1
    return parts


def part1(data=None):
    """solve part 1"""
    parts=load_parts(data)
    print(sum([p[3] for p in parts if len(parts[p])>0]))

def part2(data=None):
    """solve part 2"""
    parts=load_parts(data)
    gears=defaultdict(list)
    for part in parts:
        for sym in parts[part]:
            if sym[2]=='*':
                gears[sym].append(part)
    acc=0
    for g in gears:
        if len(gears[g])==2:
            a=gears[g][0][3]
            b=gears[g][1][3]
            acc+=a*b
    print(acc)

if __name__ == "__main__":
    part1(EXAMPLE)
    part1()
    part2(EXAMPLE)
    part2()
