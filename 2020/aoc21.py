example='''
mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)
'''
import re


def parsefile():
    with open('aoc21input.txt') as f:
        return parsedata(line.strip() for line in f)

def parseexample():
    return parsedata(line.strip() for line in example.split('\n'))



def parsedata(lines):
    lineexp=re.compile(r'\w+')
    C=[]
    for line in lines:
        if len(line)==0:
            continue
        words=lineexp.findall(line)
        i=words.index('contains')
        ingredients=words[:i]
        allergens=words[i+1:]
        C.append((ingredients,allergens))
    return C


def bestguess(C):
    guesses={}
    for i,a in C:
        for w in a:
            if w not in guesses:
                guesses[w]=set(i)
            else:
                guesses[w].intersection_update(i)
    return guesses

def findunits(guesses):
    u=[]
    for k,v in guesses.items():
        if len(v)==1:
            u.append((k,list(v)[0]))
    return u
    
def applyunits(C,units):
    changed=False
    for a,i in units:
        #print('propagate',a,i)
        for j in range(len(C)):
            ings,alls = C[j]
            if a in alls:
                alls.remove(a)
                changed=True
            if i in ings:
                ings.remove(i)
                changed=True
    return changed        
    
def propagate(C):
    '''Try to solve the puzzle using a simple strategy

1. for each allergen take the intersection of all sets of possible ingredients
2. take (if any) all unambiguous assignment allergen-->ingredient and
   remove both from all constraints
3. repeat
'''
    assignment={}
    while True:
        guesses=bestguess(C)
        units=findunits(guesses)
        for a,i in units:
            assignment[a]=i
        if not applyunits(C,units):
            break
    return assignment
    

def occurrences(C):
    o={}
    for i,_ in C:
        for w in i:
            o[w]=o.get(w,0)+1
    return o
    

def part1and2():
    Constraints=parsefile()
    occur=occurrences(Constraints)
    sol=propagate(Constraints)
    somma=0
    for i in occur:
        somma +=occur[i]
    for i in sol.values():
        somma -=occur[i]
    print(somma)
    lista=list(sol.items())
    lista.sort()
    print(','.join(i for a,i in lista))
    
    
if __name__ == '__main__':
    part1and2()