import re

demodata='''
class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12
'''

def parsedata(data=demodata):
    '''Read data for Advent of code, exercise 16

Return a dictionary with ranges and a list of ticket specs.
First in the list is your ticket, others are nearby tickets.
'''
    lines=(l for l in data.split('\n'))
    
    # Data matching regexp
    ranges=re.compile(r'([^:]*):\s*(\d+)-(\d+)\s*or\s*(\d+)-(\d+)\s*')
    tickets = re.compile(r'\d+(,\d+)*')
    R={}
    ticketlist=[]
    for line in lines:
        m=ranges.match(line)
        if m:
            name,s1,e1,s2,e2=m.groups()
            name=name.strip()
            R[name]=[(int(s1),int(e1)),(int(s2),int(e2))]
            continue
        m=tickets.match(line)
        if m:
            ticketlist.append([int(x) for x in line.split(',')])
            continue
    return R,ticketlist
    

def goodfor(value,ranges):
    goodfields=[]
    for k in ranges:
        for r in ranges[k]:
            if r[0]<= value <=r[1]:
                goodfields.append(k)
                break
    return goodfields
    
def validticket(ticket,ranges):
    for v in ticket:
        if len(goodfor(v,ranges))==0:
            return False
    return True
    
def part1():
    with open('aoc16input.txt') as f:
        data = f.read()
    ranges,tickets=parsedata(data)
    # skip my ticket
    # sum the off range values
    total = 0 
    for i in range(1,len(tickets)):
        for v in tickets[i]:
            if len(goodfor(v,ranges))==0:
                total += v
    print(total)

    
def part2():
    with open('aoc16input.txt') as f:
        data = f.read()
    ranges,tickets=parsedata(data)
    #print(ranges)
    guesses = []
    for j in range(len(tickets[0])):
        guesses.append(set(ranges.keys()))
    
    # collect valid tickets
    valid = []
    for i in range(1,len(tickets)):
        if validticket(tickets[i],ranges):
           valid.append(tickets[i])
           
    # First round of exclusion by data       
    for j in range(len(guesses)):
        for ticket in valid:
            fields = goodfor(ticket[j],ranges)
            guesses[j].intersection_update(fields)
    
    # Unit propagation
    propagate = [guesses[j] for j in range(len(guesses)) if len(guesses[j])==1]
    i = 0
    while i < len(propagate):
        unit = propagate[i]
        for j in range(len(guesses)):
            if len(guesses[j])==1:
                continue
            guesses[j].difference_update(unit)
            if len(guesses[j])==1:
                propagate.append(guesses[j])
        i += 1
    
    
    # Collect fields with word departure
    result=1
    for j in range(len(tickets[0])):
        assert len(guesses[j])==1
        guesses[j] = list(guesses[j])[0]
        #print('{:20} -> {:3}'.format(guesses[j],tickets[0][j]))
        if 'departure' in guesses[j]:
            result *=tickets[0][j]
    print(result)
        
            
part1()
part2()
            