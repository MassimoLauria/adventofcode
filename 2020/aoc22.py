
from collections import deque

example='''
Player 1:
9
2
6
3
1

Player 2:
5
8
4
7
10
'''

def parsedata(text):
    lines=text.split('\n')
    p1 = deque()
    p2 = deque()
    pl=None
    for line in lines:
        
        if line=='':
            continue

        if 'Player 1' in line:
            pl=p1
            continue
        
        if 'Player 2' in line:
            pl=p2
            continue
        
        pl.append(int(line))
    return p1,p2
    
def parseexample():
    return parsedata(example)

def parsefile():
    with open('aoc22input.txt') as f:
        return parsedata(f.read())

def copyprefix(D,n):
    return deque(list(D)[:n])


def signature(d1,d2):
    return tuple(d1)+('*',)+tuple(d2)

def play(p1,p2,recursive):
    DB = {}
    p=[None,p1,p2]
    while len(p[1])!=0 and len(p[2])!=0:

        roundsignature=signature(p[1],p[2])
        
        if roundsignature in DB:
            return 1 # 1 is winner
        else:
            DB[roundsignature]=True
            
        cards=[None,p[1].popleft(), p[2].popleft()]
    
        if recursive and cards[1]<=len(p[1]) and cards[2]<=len(p[2]):
            winner=play(copyprefix(p[1],cards[1]),
                        copyprefix(p[2],cards[2]),
                        recursive=recursive)
        elif cards[1]>cards[2]:
            winner=1
        else:
            winner=2
     
        p[winner].append(cards[winner])
        p[winner].append(cards[3-winner]) # 2 if winner is 1, 1 if winner is 2
        
    if len(p[1])==0:
        return 2
    else:
        return 1

def score(deck):
    N=len(deck)
    s=0
    while len(deck)!=0:
        s += N*deck.popleft()
        N -= 1
    return s
    

def main(recursive):
    p1,p2=parsefile()
    winner=play(p1,p2,recursive=recursive)
    
    if winner==1:
        wplay=p1
    else:
        wplay=p2

    #print('Player {} wins with score {}'.format(winner,score(wplay)))
    print(score(wplay))


def part1():
    main(recursive=False)

def part2():
    main(recursive=True)
       
part1()
part2()