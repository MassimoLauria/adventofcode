"""Advent of Code 2023 day 19
"""

from collections import defaultdict
import re
from collections import deque

EXAMPLE = """px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}
"""

def readdata(data=None):
    """Read and parse the input data"""
    if data is None:
       with open("input19.txt") as f:
            data = f.read()
    xmas={ "x":0,"m":1,"a":2,"s":3 }
    data=data.splitlines()
    # parse automata
    DFA=defaultdict(list)
    DFA['A']=[]
    DFA['R']=[]
    i=0
    while len(data[i])!=0:
        b=data[i].find('{')
        state=data[i][:b]
        descs=data[i][b+1:-1].split(',')
        assert state not in DFA
        for desc in descs:
            desc=desc.split(':')
            if len(desc)==1:
                DFA[state].append(desc[0])
            else:
                desc=(xmas[desc[0][0]],desc[0][1],int(desc[0][2:]),desc[1])
                DFA[state].append(desc)
        i+=1
    # parse parts
    parts=[]
    i+=1
    while i<len(data) and len(data[i])!=0:
        numbers = re.findall(r'\d+', data[i])
        parts.append(list(map(int, numbers)))
        i+=1
    return DFA,parts


def eval(DFA,part):
    state='in'
    #print(part,":",end="")
    while True:
        #print("-->",state,end="")
        if state=='A' or state=="R":
            #print()
            return state=="A"
        for cond in DFA[state]:
            if type(cond)==str:
                state=cond
                break
            value=part[cond[0]]
            if cond[1]=='<' and value < cond[2]:
                state=cond[3]
                break
            elif cond[1]=='>' and value > cond[2]:
                state=cond[3]
                break

def eval_filter(DFA):
    accepted=0
    Q = deque()
    init_range=[range(1,4001),]*4
    #print(init_range)
    Q.append(('in',init_range))
    while len(Q)>0:
        state,space=Q.popleft()
        if state=='A':
            res=1
            for r in space:
                res*=len(r)
            accepted+=res
            continue
        if state=='R':
            continue
        spawn=[]
        for cond in DFA[state]:
            if type(cond)==str:
                spawn.append( (cond,space))
                break
            coord=cond[0]
            crange=space[coord]
            thr=cond[2]
            if cond[1]=='<':
                # split
                yes=range(crange[0],thr)
                no =range(thr,crange[-1]+1)
            elif cond[1]=='>':
                no=range(crange[0],thr+1)
                yes =range(thr+1,crange[-1]+1)
            space_yes=space[:]
            space_yes[coord]=yes
            if len(yes)>0:
                spawn.append((cond[3],space_yes))
            else:
                assert no == space[coord]
            space[coord]=no
        Q.extend(spawn)
    return accepted

def part1(data=None):
    """solve part 1"""
    DFA,parts=readdata(data)
    res=0
    for part in parts:
        if eval(DFA,part):
            res+=sum(part)
    print(res)

def part2(data=None):
    """solve part 2"""
    DFA,_=readdata(data)
    res=eval_filter(DFA)
    print(res)


if __name__ == "__main__":
    part1(EXAMPLE)
    part1()
    part2(EXAMPLE)
    part2()
