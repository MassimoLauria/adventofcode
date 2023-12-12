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

def howmany(D,pattern,lengths,p,l):
    while p<len(pattern) and pattern[p]=='.': p+=1

    if (p,l) in D:
        return D[p,l]

    if l==len(lengths):
        return 0 if "#" in pattern[p:] else 1

    if sum(lengths[l:])+len(lengths)-l-1 > len(pattern)-p:
        return 0

    start_with_dots=0
    start_with_block=0
    if pattern[p]=='?':
        start_with_dots = howmany(D,pattern,lengths,p+1,l)

    dest =p+lengths[l]
    block_compatible = dest<=len(pattern) and \
                       not ('.' in pattern[p:dest])
    if len(pattern)>dest and pattern[dest]=='#':
        block_compatible = False
    if block_compatible:
        start_with_block = howmany(D,pattern,lengths,dest+1,l+1)

    D[p,l] = start_with_dots + start_with_block
    return D[p,l]


def part1(data=None):
    """solve part 1"""
    somma=0
    for pp,ll in readdata(data):
        somma+=howmany({},pp,ll,0,0)
    print(somma)


def part2(data=None):
    """solve part 2"""
    somma=0
    for p,l in readdata(data):
        x=howmany({},'?'.join([p]*5),l*5,0,0)
        somma+=x
    print(somma)


if __name__ == "__main__":
    part1(EXAMPLE)
    part1()
    part2(EXAMPLE)
    part2()
