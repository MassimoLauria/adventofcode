example='''
mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)
'''
import networkx as nx
from networkx.algorithms.bipartite import maximum_matching
import re
from itertools import product
from contextlib import redirect_stdout
import subprocess


def parsefile():
    with open('aoc21input.txt') as f:
        return parsedata(line.strip() for line in f)

def parseexample():
    return parsedata(line.strip() for line in example.split('\n'))


Vars={}
cntr=1
def var(a,i):
    global Vars
    global cntr
    if (a,i) in Vars:
        return Vars[a,i]
    else:
        Vars[a,i]=cntr
        cntr+=1
        return Vars[a,i]
def resetvar():
    global Vars
    global cntr
    cntr=1
    Vars={}

def parsedata(lines):
    resetvar()
    G = nx.Graph()
    M = 0
    occurrences={}
    lineexp=re.compile('\w+')
    for line in lines:
        if len(line)==0:
            continue
        words=lineexp.findall(line)
        i=words.index('contains')
        ingredients=words[:i]
        allergens=words[i+1:]
        G.add_nodes_from(allergens,bipartite=0)
        G.add_nodes_from(ingredients,bipartite=1)
        for i in ingredients:
            occurrences[i] = occurrences.get(i,0) + 1
        for i,a in product(ingredients,allergens):
            G.add_edge(a,i)
            print('+1 x{}'.format(var(a,i)),end=' ')
        print(' = {};'.format(len(allergens)))
        M += 1
            
    for i in occurrences:
        for a in list(G.neighbors(i)):
            print('-1 x{}'.format(var(a,i)),end=' ')
        print(' >= -1;')
        M += 1
    for a in G.nodes():
        if a in occurrences:
            continue
        for i in list(G.neighbors(a)):
            print('+1 x{}'.format(var(a,i)),end=' ')
        print(' = 1;')
        M += 1
        
    N = len(Vars)
    return occurrences,N,M


def solve(opbfile):
    p = subprocess.Popen(['roundingsat',opbfile],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    stdoutdata = p.communicate()[0].decode('ascii').split('\n')
    data = stdoutdata[-2].split()
    #print(data)
    for i in range(1,len(data)):
        data[i] = 0 if data[i][0]=='-' else 1
    data[0]=None
    assign={}
    #print(assign)
    for k,v in Vars.items():
        assign[k]=data[v]
    return assign

def part1and2():
    f = open('aoc21part1.opb','w')
    with redirect_stdout(f):
        occur,N,M=parseexample()
    f.close()
    f = open('aoc21part1.opb','w')
    with redirect_stdout(f):
        print('* #variable= {} #constraint= {}'.format(N,M))
        occur,N,M=parseexample()
    f.close()
    assign=solve('aoc21part1.opb')
    assigned=[]
    for k,v in assign.items():
        a,i = k
        if v == 1:
            assigned.append((a,i))
            if i in occur:
                del occur[i]
    print('Part1:',sum(v for k,v in occur.items()))
    assigned.sort()
    print(assigned)
    print('Part2:',','.join(i for a,i in assigned))
    
part1and2()