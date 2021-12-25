from pprint import pprint as print

"""
---0---
|     |
1     3
|     |
---2---
|     |
4     6
|     |
---5---
"""




example="""be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce
"""

INV_LENGTH={2: [1], 3 : [7], 4 : [4], 5 : [2, 3, 5], 6:[0,6,9], 7:[8]}
LEDS={
    (0,1,3,4,5,6) :0,
    (3,6) : 1,
    (0,2,3,4,5) : 2,
    (0,2,3,5,6) : 3,
    (1,2,3,6) : 4,
    (0,1,2,5,6) : 5,
    (0,1,2,4,5,6) : 6,
    (0,3,6) : 7,
    (0,1,2,3,4,5,6) : 8,
    (0,1,2,3,5,6) : 9
    }

def parsedata(data=None):
    if data is None:
        with open("input08.txt") as f:
            data=f.read()
    entries=[]
    for x in data.splitlines():
        ls,rs=x.split("|")
        entries.append((sorted(ls.split(),key=len),rs.split()))
    return entries        
        
def part1(data=None):
    entries=parsedata(data)
    cnt=0
    for _,rs in entries:
        for x in rs:
            if len(INV_LENGTH[len(x)])==1:
                cnt+=1
    print(cnt)
    
def rectset(D,left,right):
    for l in left:
        D[l] = set(right)
    for r in right:
        D[r] = set(left)
    
def rectupdate(D,left,right):
    for l in left:
        D[l].intersection_update(right)
    for r in right:
        D[r].intersection_update(left)
    notleft = set(range(7)).difference(set(left))
    notright = set("abcdefg").difference(set(right))
    for l in notleft:
        D[l].intersection_update(notright)
    for r in notright:
        D[r].intersection_update(notleft)
    

def solve(entry):
    D={}
    rectset(D,range(7),"abcdefg")
    # leds of digit 1
    digits1=entry[0]
    rectupdate(D,[3,6],digits1)
    # leds of digit 7
    digits7=entry[1]
    rectupdate(D,[0,3,6],digits7)
    # leds of digit 4
    digits4=entry[2]
    rectupdate(D,[1,2,3,6],digits4)
    # leds of digit 2,3,5 have the three horizontal bars in common
    # the top one is known, we can disambiguate the other two
    common235=set(entry[3])
    common235.intersection_update(entry[4])
    common235.intersection_update(entry[5])
    rectupdate(D,[0,2,5],common235)
    # need to disambiguate led 3 and 7, using digit 0,6,9
    common069=set(entry[6])
    common069.intersection_update(entry[7])
    common069.intersection_update(entry[8])
    rectupdate(D,[0,1,5,6],common069)
    # solutions
    S={}
    for x in "abcdefg":
        assert len(D[x])==1
        S[x] = list(D[x])[0]
    return S

def evaldigit(S,chars):
    on=[]
    for c in chars:
        on.append(S[c])
    on=tuple(sorted(on))
    return LEDS[on]

def evalrightpart(S,part):
    acc=0
    for s in part:
        acc *=10
        acc += evaldigit(S,s)
    return acc

def part2(data=None):
    entries=parsedata(data)
    total=0
    for entry in entries:
        left=entry[0]
        right=entry[1]
        S=solve(left)
        total += evalrightpart(S,right)
    print(total)
    
    
    
if __name__ == "__main__":
    part1(example)
    part1()
    part2(example)
    part2()