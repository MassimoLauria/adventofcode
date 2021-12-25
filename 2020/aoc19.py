import re

demo='''0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

ababbb
bababa
abbbab
aaabbb
aaaabbb'''

demo2='''42: 9 14 | 10 1
9: 14 27 | 1 26
10: 23 14 | 28 1
1: "a"
11: 42 31
5: 1 14 | 15 1
19: 14 1 | 14 14
12: 24 14 | 19 1
16: 15 1 | 14 14
31: 14 17 | 1 13
6: 14 14 | 1 14
2: 1 24 | 14 4
0: 8 11
13: 14 3 | 1 12
15: 1 | 14
17: 14 2 | 1 7
23: 25 1 | 22 14
28: 16 1
4: 1 1
20: 14 14 | 1 15
3: 5 14 | 16 1
27: 1 6 | 14 18
14: "b"
21: 14 1 | 1 14
25: 1 1 | 1 14
22: 14 14
8: 42
26: 14 22 | 1 20
18: 15 15
7: 14 5 | 1 21
24: 14 1

abbbbbabbbaaaababbaabbbbabababbbabbbbbbabaaaa
bbabbbbaabaabba
babbbbaabbbbbabbbbbbaabaaabaaa
aaabbbbbbaaaabaababaabababbabaaabbababababaaa
bbbbbbbaaaabbbbaaabbabaaa
bbbababbbbaaaaaaaabbababaaababaabab
ababaaaaaabaaab
ababaaaaabbbaba
baabbaaaabbaaaababbaababb
abbbbabbbbaaaababbbbbbaaaababb
aaaaabbaabaaaaababaa
aaaabbaaaabbaaa
aaaabbaabbaaaaaaabbbabbbaaabbaabaaa
babaaabbbaaabaababbaabababaaab
aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba'''



def parsefile():
    with open('aoc19input.txt') as f:
        return parsedata(f.read())
    

def parsedata(text):
    rules={}
    words=[]
    lines =(line for line in text.split('\n'))
    line = next(lines)
    # read rules
    while len(line.strip())!=0:
        ruleid,rest = line.split(':')
        rest=rest.split()
        if '\"a\"' in rest:
            rules[ruleid]='a'
        elif '\"b\"' in rest:
            rules[ruleid]='b'
        elif '|' in rest:
            rules[ruleid]=['('] + rest[:] + [')']
        else:
            rules[ruleid]=rest[:]
        line=next(lines)
        
    # read words
    for l in lines:
        words.append(l.strip())
    return rules,words
            
def regexp(rules,ruleid='0'):
    '''Computes the regexp corresponding to the listed specs.

For each rules computes the exact length of the matching string.
To do that we assert that rules are not looping and that each branch in
a disjunction accepts strings of the same length.
This is true for the rules in AOC19
'''
    # have to compute explicitly
    if type(rules[ruleid])==list:
        parts=[]
        rulelengthR=0
        rulelengthL=None
        for x in rules[ruleid]:
            if x in '()':
                parts.append(x)
            elif x=='|':
                parts.append(x)
                rulelengthL=rulelengthR
                rulelengthR=0
            else:
                exp,rl=regexp(rules,x)
                rulelengthR += rl
                parts.append(exp)
        if rulelengthL is not None:
            assert rulelengthL==rulelengthR
        rules[ruleid]=''.join(parts),rulelengthR
    elif type(rules[ruleid])==str:
        rules[ruleid]=rules[ruleid],len(rules[ruleid])
    else:
        pass # tuple, rule already computed

    return rules[ruleid]  #regexp,matchlength

def part1():
    rules,words=parsedata(demo)
    rules,words=parsefile()
    matcher=re.compile('^'+regexp(rules)[0]+'$')
    counter=0
    for w in words:
        if matcher.match(w) is not None:
            counter +=1
    print(counter)
    
    
def part2():
    #rules,words=parsedata(demo2)
    rules,words=parsefile()
    
    #delete the broken rules
    del rules['8']
    del rules['11']
    del rules['0']
    # instead of adding the new looping rules
    # 8: 42 | 42 8
    # 11: 42 31 | 42 11 31
    # we just ignore them (and ignore rule 0 which is affected)
    #
    # instead we observe that
    # rule 0 matches 42^a 31^b for a>b>=1
    # which is not regular
    #
    # since all matches for rule 42 and 31 have the same length,
    # we segment each word explicitly and check the matches of the segments
    
    rule42,l42=regexp(rules,ruleid='42')
    rule31,l31=regexp(rules,ruleid='31')
    assert l42==l31
    rule42=re.compile(rule42)
    rule31=re.compile(rule31)
    lseg=l42
    counter = 0
    for w in words:
        if len(w) % lseg !=0:
            continue
        segments=[w[i:i+lseg] for i in range(0,len(w),lseg)]
        i=0
        while i<len(segments) and rule42.match(segments[i]) is not None:
            i += 1
        a=i
        while i<len(segments) and rule31.match(segments[i]) is not None:
            i += 1
        b=i-a
            
        if i != len(segments):
            continue
        if a > b >= 1:
            counter += 1
    print(counter)

part1() 
part2()