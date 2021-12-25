import re

def readinput():
    with open('aoc2input.txt') as data:
        fmt=re.compile('(\d+)-(\d+)\s(\w)\s*:\s*(\w+)')
        for line in data:
            A,B,char,passwd=fmt.findall(line)[0]
            A=int(A)
            B=int(B)
            yield A,B,char,passwd
            
def testpwd1(A,B,char,text):
    return A <= text.count(char) <= B
 
def testpwd2(A,B,char,text):
    return  (text[A-1]==char) ^ (text[B-1]==char)
 

def part1():
    goodpwd = 0
    for t in readinput():
        if testpwd1(*t):
            goodpwd +=1
    print(goodpwd)
    
def part2():
    goodpwd = 0
    for t in readinput():
        if testpwd2(*t):
            goodpwd +=1
    print(goodpwd)
    
part1()
part2()
        