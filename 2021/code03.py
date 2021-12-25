example1="""
00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010
"""

def scan(data=None):
    if data is None:
        with open("input03.txt") as f:
            data=f.read()
    data=data.splitlines()
    data=[x for x in data if len(x)!=0]
    
    #size of the binary strings
    wordsize=len(data[0])
    rows=0
    sums=[0]*wordsize
    for line in data:
        rows+=1
        for b in range(wordsize):
            if line[b]=='1':
                sums[b]+=1
    return sums,rows

def getbitstrings(data=None):
    if data is None:
        with open("input03.txt") as f:
            data=f.read()
    return [x for x in data.splitlines() if len(x)!=0]

def binstr2num(text):
    v=0
    for b in range(len(text)):
        v *=2
        v +=int(text[b])
    return v

def part1(data=None):
    sums,rows=scan(data)
    gamma=0
    eps=0
    for b in range(len(sums)):
        gamma *=2
        eps *=2
        if sums[b]>=rows//2:
            gamma +=1
        else:
            eps +=1
    print(gamma*eps)

def split(data,bit):
    parts=[[],[]]
    for x in data:
        b = ord(x[bit])-ord('0')
        parts[b].append(x)
    if len(parts[0])<=len(parts[1]):
        return parts[0],parts[1]
    else:
        return parts[1],parts[0]

def part2(data=None):
    oxy=0
    co2=0
    
    data=getbitstrings(data)
    wordsize = len(data[0])
    least,most=data,data
    for b in range(wordsize):
        if len(least)>1:
            least,_ = split(least,b)
        _,most  = split(most,b)
    co2=binstr2num(least[0])
    oxy=binstr2num(most[0])
    print(co2*oxy)


if __name__ == "__main__":
    part1()
    part2()
        
        
        