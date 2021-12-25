OPEN="([{<"
CLOSE=")]}>"
MATCH={}
SCORES={}
VALUES={}

example="""[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]"""


def fillmatch():
    s=[3,57,1197,25137]
    for i in range(4):
        MATCH[OPEN[i]]=CLOSE[i]
        MATCH[CLOSE[i]]=OPEN[i]
        SCORES[CLOSE[i]]=s[i]
        VALUES[CLOSE[i]]=i+1
        
def parse(text):
    stack=[]
    for c in text:
        if c in OPEN:
            stack.append(c)
        else:
            m = stack.pop()
            if c != MATCH[m]:
                return ('e',c)
    discharge=[]
    while len(stack)!=0:
        discharge.append(MATCH[stack.pop()])
    return ("i","".join(discharge))

def getdata(data=None):
    if data is None:
        with open("input10.txt") as f:
            data=f.read()
    return data.splitlines()

def part1(data=None):
    acc=0
    for l in getdata(data):
        e,r = parse(l)
        if e=='e':
             acc+=SCORES[r]
    print(acc)

def value(t):
    v=0
    for c in t:
        v*=5
        v+=VALUES[c]
    return v
    

def part2(data=None):
    completions=[]
    for l in getdata(data):
        e,r = parse(l)
        if e=='i':
             completions.append(r)
    values=[value(c) for c in completions]
    values.sort()
    print(values[len(values)//2])
    
if __name__=="__main__":
    fillmatch()
    part1(example)
    part1()
    part2(example)
    part2()
    