#advent 2019 - day 08

def readdata():
    with open("input08.txt") as f:
        return f.read().strip()
    
def getlayers():
    w,h=25,6
    layers=[]
    imgdata=readdata()
    stats=[]
    N=len(imgdata)
    for i in range(0,N,w*h):
        chunk=imgdata[i:i+w*h]
        layers.append(chunk)
    return layers

def part1():
    layers=getlayers()
    stats=[]
    for layer in layers:
        f0=layer.count('0')
        f1=layer.count('1')
        f2=layer.count('2')
        stats.append((f0,f1,f2))
    m0,m1,m2 = min(stats)
    return m1*m2
    
def collapselayers(layers):
    N=len(layers)
    s=len(layers[0])
    res=['X']*s
    for i in range(s):
        for d in range(N):
            if layers[d][i]!='2':
                res[i]=layers[d][i]
                break
    return "".join(res)

def view(indata):
    outdata=[]
    for c in indata:
        if c=='1':
            outdata.append("X")
        else:
            outdata.append(" ")
    for i in range(0,25*6,25):
        print("".join(outdata[i:i+25]))

def part2():
    layers=getlayers()
    res=collapselayers(layers)
    view(res)
    
    
        
if __name__=="__main__":
    print(part1())
    part2()