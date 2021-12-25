
puzzleinput=[1,0,15,2,10,13]


def game(startseq,finalturn=2020):
    if finalturn<1:
        raise ValueError
    if finalturn<=len(startseq):
        return startseq[finalturn-1]
    
    lastsaid={}
    for i in range(len(startseq)-1):
        lastsaid[startseq[i]]=i+1
    last=startseq[-1]
    current=len(startseq)+1
    while current <= finalturn:
        if last not in lastsaid:
            lastsaid[last]=current-1
            last=0
        else:
            said=lastsaid[last]
            lastsaid[last]=current - 1
            last = current -1 - said
        current +=1
    return last
            
def part1():
    print(game(puzzleinput))
    
def part2():
    print(game(puzzleinput,30000000))

part1()
part2()