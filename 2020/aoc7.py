# examples of rules
'''
light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags.
'''

def readdata():
    contains={}    
    with open('aoc7input.txt') as f:
        for line in f:
            rule = line.split()
            color=rule[0]+' '+rule[1]
            
            if color not in contains:
                contains[color] = []
                        
            if rule[4]=='no':
                continue
            
            for i in range(4,len(rule),4):
                cnum=int(rule[i])
                ccolor=rule[i+1]+' '+rule[i+2]
                
                contains[color].append((cnum,ccolor))
    return contains

def invert(D):
    contained={}
    for bag,subitems in D.items():
        for _,ccolor in subitems:
            if ccolor not in contained:
                contained[ccolor]=[]
            contained[ccolor].append(bag)
    return contained


def part1():
    Outside = invert(readdata())

    Sol  = set()
    NSol = set(Outside['shiny gold'])
    while len(NSol)>0:
        T = NSol
        Sol.update(NSol)
        NSol=set()
        for sol in T:
            if sol in Outside:
                NSol.update(Outside[sol])
        NSol = NSol - Sol
    print(len(Sol))    
    
def navigate(Contains,color):
    res = 0
    if color not in Contains:
        return res
    for num,subcol in Contains[color]:
        res += num*(1+navigate(Contains,subcol))
    return res
    
def part2():
    Contains = readdata()
    print(navigate(Contains,'shiny gold'))
    
part1()
part2()
