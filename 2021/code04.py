from pprint import pprint as print

ex="""7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7
"""

def makebingo(lines,t):
    return [[ int(x) for x in lines[t+i].split() ] for i in range(5)]

def scan(data=None):
    if data is None:
        with open("input04.txt") as f:
            data=f.read()
    data=data.splitlines()
    
    draws = [int(x) for x in data[0].split(",")]
    bingos = []
    for t in range(2,len(data),6):
        bingos.append(makebingo(data,t))
    return draws,bingos
    
def part1(data=None):
    draws,bingos=scan(data)
    
    where={ x:[] for x in range(100)}
    counters={}
    sums=[]
    for t in range(len(bingos)):
        for r in range(5):
            counters[(t,'r',r)]=0
        for c in range(5):
            counters[(t,'c',c)]=0
        acc=0
        for r in range(5):
            for c in range(5):
                x = bingos[t][r][c]
                where[x].append((t,r,c))
                acc+=x
        sums.append(acc)

    for draw in draws:
        for b,r,c in where[draw]:
            counters[(b,'r',r)]+=1
            counters[(b,'c',c)]+=1
            sums[b] -= draw
            if counters[(b,'r',r)]==5:
                return draw*sums[b]
            if counters[(b,'c',c)]==5:
                return draw*sums[b]
            

def part2(data=None):
    draws,bingos=scan(data)
    
    where={ x:[] for x in range(100)}
    counters={}
    sums=[]
    wins={}
    for t in range(len(bingos)):
        wins[t]=False
        for r in range(5):
            counters[(t,'r',r)]=0
        for c in range(5):
            counters[(t,'c',c)]=0
        acc=0
        for r in range(5):
            for c in range(5):
                x = bingos[t][r][c]
                where[x].append((t,r,c))
                acc+=x
        sums.append(acc)

    countdown=len(bingos)
    for draw in draws:
        for b,r,c in where[draw]:
            counters[(b,'r',r)]+=1
            counters[(b,'c',c)]+=1
            sums[b] -= draw
            if wins[b]:
                continue

            if counters[(b,'r',r)]==5 or counters[(b,'c',c)]==5:
                wins[b]=True
                countdown -=1
               
            if countdown==0:
                return draw*sums[b]
  

print(part1())
print(part2())

