

def intersectionsize(grp):
    n = len(grp)
    data = sorted(list(''.join(grp)))
    ints=[]
    i = 0
    while i+n <= len(data):
        if data[i] == data[i+n-1]:
            ints.append(data[i])
            i = i + n
        else:
            i = i + 1
    return len(ints)
            
        

def getanswers(fname):
    groups=[[]]
    g=None
    with open(fname) as f:
        for line in f:
            if line in ['\n','']:
                groups.append([])
                continue
            
            groups[-1].append(line.strip())
            
    return groups


def part1():
    A = getanswers('aoc6input.txt')
    sumunions=0
    for group in A:
        x = set()
        for answer in group:
            x.update(list(answer))
        sumunions += len(x)
    print(sumunions)

def part2():
    A = getanswers('aoc6input.txt')
    print(sum(intersectionsize(x) for x in A))
    
part1()
part2()