 
def readdata():
    with open('aoc9input.txt') as f:
        for line in f:
            yield(int(line))


def sumoftwo(data,num):
    for i in range(len(data)-1):
        for j in range(1,len(data)):
            if data[i]+data[j] == num:
                return True
    return False

def part1():
    prev25=[]
    src=readdata()
    for i in range(25):
        prev25.append(next(src))
    i=0
    while True:
        try:
            x = next(src)
        except StopIteration:
            return None
        
        if not sumoftwo(prev25,x):
            return x
        else:
            prev25[i]=x
            i = (i+1) % 25
    
def part2():
    weakness=part1()
    ns = list(readdata())
    size = len(ns)
    for i in range(size-1):
        ssum=ns[i]
        mmin=ns[i]
        mmax=ns[i]
        for j in range(i+1,size):
            ssum += ns[j]
            if ssum > weakness:
                break

            if mmin>ns[j]:
                mmin = ns[j]
            if mmax<ns[j]:
                mmax = ns[j]
                
            if ssum==weakness:
                return mmin+mmax
            
print(part1())
print(part2())
