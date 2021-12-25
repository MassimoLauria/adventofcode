
class Game():
    
    def __init__(self,text,upto=None):

        if upto is None:
            self.greatest = len(text)
        else:
            assert upto>len(text)
            self.greatest=upto

        self.succ=list(range(1,self.greatest+2))
        
        tmp = [int(c) for c in text]
        self.current=tmp[0]
        
        for i in range(0,len(tmp)-1):
            self.succ[tmp[i]]=tmp[i+1]
            
            
        if self.greatest > len(tmp):
            self.succ[tmp[-1]]=len(tmp)+1
            self.succ[-1]=tmp[0]
        else:
            self.succ[tmp[-1]]=tmp[0]
        
    
    def gamestep(self):
        
        s=self.succ
        
        # elements to be moved
        cur=self.current
        picked = [s[cur],s[s[cur]],s[s[s[cur]]]]

        # find target
        target= cur
        while True:
            target = (target - 1)
            if target <=0:
                target = self.greatest
            if target not in picked:
                break
        
        # new current element after old current element
        s[cur]=s[picked[-1]]
        self.current=s[cur]
        # move picked element
        aftertarget=s[target]
        s[target]=picked[0]
        s[picked[-1]]=aftertarget
        
    def play(self,rounds):
        for _ in range(rounds):
            self.gamestep()
        
    def __str__(self):
        output=['({})'.format(self.current)]
        p=self.current
        while self.succ[p]!=self.current:
            p=self.succ[p]
            output.append('{}'.format(p))
        return ' '.join(output)
        
example='389125467'
gamedata='739862541'


def extractsolution1(G):
    s=G.succ
    i=1
    output=[]
    while s[i]!=1:
        i=s[i]
        output.append(i)
    return ''.join(str(v) for v in output)

def extractsolution2(G):
    d=G.succ
    a=d[1]
    b=d[d[1]]
    return a*b


def part1():
    #print('===Part1===')
    #G=Game(example)
    #G.play(10)
    #print('Example for 10 moves, solution:',extractsolution1(G))
    #G=Game(example)
    #G.play(100)
    #print('Example for 100 moves, solution:',extractsolution1(G))
    G=Game(gamedata)
    G.play(100)
    #print('Puzzle input solution:',extractsolution1(G))
    print(extractsolution1(G))

def part2():
    #print('===Part2===')
    #G=Game(example,1000000)
    #G.play(10000000)
    #print('Example for 10.000.000 moves, solution:',extractsolution2(G))
    G=Game(gamedata,1000000)
    G.play(10000000)
    #print('Puzzle input solution:',extractsolution2(G))
    print(extractsolution2(G))

part1()
part2()