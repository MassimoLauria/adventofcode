"""Advent of Code 2023 day 12
"""

EXAMPLE = """???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1
"""

def readdata(data=None):
    """Read and parse the input data"""
    if data is None:
       with open("input12.txt") as f:
            data = f.read()
    patterns=[]
    for line in data.splitlines():
        line=line.split()
        pattern = line[0]
        lengths = [int(x) for x in line[1].split(',')]
        patterns.append((pattern,tuple(lengths)))
    return patterns

def howmany(D,pattern,lengths):
    dots=0
    while dots<len(pattern) and pattern[dots]=='.': dots+=1
    pattern = pattern[dots:]

    if (pattern,lengths) in D:
        return D[pattern,lengths]

    if len(lengths)==0:
        return 0 if "#" in pattern else 1

    if sum(lengths)+len(lengths)-1 > len(pattern):
        return 0

    start_with_dots=0
    start_with_block=0
    if pattern[0]=='?':
        start_with_dots = howmany(D,pattern[1:],lengths)
    bsize=lengths[0]
    block_compatible = bsize<=len(pattern) and \
                       not ('.' in pattern[:bsize])
    if len(pattern)>bsize and pattern[bsize]=='#':
        block_compatible = False
    if block_compatible:
        start_with_block = howmany(D,pattern[bsize+1:],lengths[1:])

    D[pattern,lengths] = start_with_dots + start_with_block
    return D[pattern,lengths]


def part1(data=None):
    """solve part 1"""
    D={}
    somma=0
    for p,l in readdata(data):
        somma+=howmany(D,p,l)
    print(somma)


def part2(data=None):
    """solve part 1"""
    D={}
    somma=0
    for p,l in readdata(data):
        x=howmany(D,'?'.join([p]*5),l*5)
        somma+=x
        #print(x)
    print(somma,len(D))


if __name__ == "__main__":
    part1(EXAMPLE)
    part1()
    part2(EXAMPLE)
    part2()
