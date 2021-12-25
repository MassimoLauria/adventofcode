

def readdata():
    with open('aoc13input.txt') as f:
        timestamp=int(f.readline())
        busdata=[]
        for bus in f.readline().strip().split(','):
            if bus!='x':
                busdata.append(int(bus))
    return timestamp,busdata

def part1():
    timestamp,busdata=readdata()
    waitingtime=[x - (timestamp % x) if (timestamp % x)!=0 else 0 for x in busdata]
    wt,bid = min(zip(waitingtime,busdata))
    print(wt*bid)

    
def readdata2():
    with open('aoc13input.txt') as f:
        f.readline()
        busdata=[]
        for bus in f.readline().strip().split(','):
            if bus!='x':
                busdata.append(int(bus))
            else:
                busdata.append(None)
    return busdata


def cleandata(lista):
    for n in lista:
        if n is None:
            continue
        i=2
        while i**2 <= n:
            if n % i == 0:
                raise ValueError('{} is composite'.format(n))
            i+=1
    data=[]
    for i in range(len(lista)):
        if lista[i] is not None:
            data.append((lista[i],i))
    return data    

def solve(base,goal,mod):
    truegoal = goal % mod
    for i in range(mod):
        if (i*base) % mod == truegoal:
            #print('solve({},{},{})-->{}'.format(base,goal,mod,i*base))
            return i*base
    raise ValueError

def part2():
    data=cleandata(readdata2())    
    N=1
    risultato=0
    for bus,_ in data:
        N*=bus
    
    for bus,order in data:
        risultato += solve(N//bus,-order,bus)
        
    print(risultato % N)

part1() 
part2()