inputfile="input01.txt"
text="""
199
200
208
210
200
207
240
269
260
263
"""
def readdata(data=None):
    if data is None:
        data=open(inputfile)
        return data.read().split()
    elif isinstance(data,str):
        return data.split()
    return None

def inc(seq):
    acc=0
    for i in range(1,len(seq)):
        if seq[i]>seq[i-1]:
            acc+=1
    return acc

def part1(data=None):
    values=[int(x) for x in readdata(data)]
    print(inc(values))
    
def part2(data=None):
    values=[int(x) for x in readdata(data)]
    msum=[sum(values[0:3])]
    for i in range(1,len(values)-2):
        datum = msum[-1]
        datum +=values[i+2]
        datum -=values[i-1]
        msum.append(datum)
    print(inc(msum))
    
if __name__=="__main__":
    part1()
    part2()