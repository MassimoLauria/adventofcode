def readdata():
    D=[0]
    with open('aoc10input.txt') as f:
        for line in f:
            D.append(int(line))
    D.sort()
    D.append(D[-1]+3)
    return D
            
def part1():
    try:
        D=readdata()
    
        diff=[0,0,0,0]
        for i in range(1,len(D)):
            delta = D[i]-D[i-1]
            diff[delta] += 1
        print(diff[1]*diff[3])
    except IndexError:
        print('impossible to connect them all')

def part2():
    D=readdata()
    
    C=[0]*len(D)
    
    # C[i] memorizza i percorsi dall'adattatore i incluso al device
    C[-1] = 1
    i = len(C)-2
    while i>=0:
        j=i+1
        while j<len(D) and D[j]<=D[i]+3:
            j +=1
        C[i] =sum(C[t] for t in range(i+1,j))
        i = i - 1
    print(C[0])

part1()
part2()