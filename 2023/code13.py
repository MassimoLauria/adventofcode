"""Advent of Code 2023 day 13
"""

EXAMPLE = """
#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#
"""

def into_int(block):
    nums=[]
    for line in block:
        i=0
        for c in line:
            i = i<<1 | (c=='#')
        nums.append(i)
    return nums

def transpose(block):
    R=len(block)
    C=len(block[0])
    T=[['']*R for _ in range(C)]
    for j in range(C):
        T[j]="".join(block[i][j] for i in range(R))
    return T

def printb(block):
    for l in block:
        print(l)

def readdata(data=None):
    """Read and parse the input data"""
    if data is None:
       with open("input13.txt") as f:
            data = f.read()
    blocks=[[]]
    for line in data.splitlines():
        if len(line)==0:
            if len(blocks[-1])!=0: blocks.append([])
        else:
            blocks[-1].append(line)
    blockpairs=[]
    for block in blocks:
        r=into_int(block)
        c=into_int(transpose(block))
        blockpairs.append((block,r,c))
    return blockpairs

def diff_bits(X,Y):
    if X==Y: return 0
    diff=X^Y
    diff=diff & (diff-1)
    if diff==0: return 1
    return 32


def find_reflection(seq,bit_switches):
    for pos in range(1,len(seq)):
        bits=0
        i=0
        while bits<=bit_switches and (pos-1-i>=0) and (pos+i<len(seq)):
            bits+=diff_bits(seq[pos-1-i],seq[pos+i])
            i+=1
        if bits==bit_switches:
            return pos


def part12(bit_switches,data=None):
    """solve part 1 ans 2"""
    pairs=readdata(data)
    somma=0
    i=0
    for block,hor,vert in pairs:
        #print("------------------------Block:",i)
        x = find_reflection(hor,bit_switches)
        y = find_reflection(vert,bit_switches)
        assert x is not None or y is not None
        assert x is None or y is None
        # if x is not None: assert verify_hor(block,x,bit_switches)
        # if y is not None: assert verify_vert(block,y,bit_switches)
        # assert x is None or y is None
        # assert (x is not None) or (y is not None)
        i+=1
        if x is not None:
            somma+=100*x
        else:
            somma+=y
    print(somma)


if __name__ == "__main__":
    part12(0,EXAMPLE)
    part12(0)
    part12(1,EXAMPLE)
    part12(1)
