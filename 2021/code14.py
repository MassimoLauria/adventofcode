from collections import Counter

example="""
NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C
"""



"""
Status: s,e,count
 s = initial char
 e = ending char
 count= pair --> occurences number map
 transitions = pair --> additional char map
"""

def parsedata(data=None):
    if data is None:
        with open("input14.txt") as f:
            data=f.read()
    init=None
    T={}
    for l in data.splitlines():
        if len(l)==0:
            continue
        if "->" in l:
            left,right=l.split("->")
            left=left.strip()
            right=right.strip()
            T[left]=right
        else:
            init=l.strip()
    return init,T

def iter(S,T):
    D=Counter()
    for pair in S:
        x,y = pair
        c = T[pair]
        D[x+c]+=S[pair]
        D[c+y]+=S[pair]
    return D

def solve(steps,data=None):
    # read the input
    initial,transformations=parsedata(data)

    # initial count of adiacent pairs of letters
    pairs=Counter()
    for i in range(len(initial)-1):
        pairs[initial[i:i+2]]+=1

    # reproduce
    for i in range(steps):
        pairs = iter(pairs,transformations)

    # count the letters
    count=Counter()
    count[initial[0]]+=1
    for xy in pairs:
        count[xy[1]]+=pairs[xy]
    
    rank=count.most_common()
    print(rank[0][1]-rank[-1][1])
    
    

if __name__ == "__main__":
    # part 1
    solve(10,example)
    solve(10)
    # part 2
    solve(40,example)
    solve(40)
    
    
            
    