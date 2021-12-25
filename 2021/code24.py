from itertools import product,combinations
from collections import defaultdict
import random

def next_z(z,i,w,params):
    """Implements steps of the ALU computation

Realizes the i-th stage of the program.
    """
    a,b,c=params[i]
    t = (z % 26) + b == w
    z = z//a
    if t:
        assert a==26 # if a==1 z ---> 26*z+something
        return z
    else:
        return 26*z+w+c
    return nz

def ALU(stdin=None,status=None):
    with open("input24.txt") as f:
        code=f.read().split()
    if status is None:
        status={ "w":0, "x": 0, "y":0, "z":0 }
    elif isinstance(status,tuple):
        status={ "w":status[0],
                 "x":status[1],
                 "y":status[2],
                 "z":status[3]}
    else:
        for c in "wxyz":
            if c not in status:
                status[c]=0    
    if type(stdin)==int:
        stdin=str(stdin)
    
    nextinput=0 # next input to read from the ALU
    pc=0
    while pc<len(code):
        if "trap" in status:
            input(str(status)+"\n" +
                  str(code[pc:pc+3])+
                  "\nnext?>")
        inst=code[pc]
        # One operand
        if inst=="inp":
            try:
                var=code[pc+1]
            except IndexError:
                raise ValueError(f"Missing operand for '{inst}' at pc={pc}")
            try:
                x=stdin[nextinput]
                status[var]=int(x)  
            except IndexError:
                raise ValueError(f"Input required for '{inst}' at pc={pc}")
            except KeyError:
                raise ValueError(f"Invalid variable '{var}' at pc={pc+1}")
            nextinput+=1
            pc+=2
            continue
        
        # Two operands
        try:
            a=code[pc+1]
            b=code[pc+2]
            vala=status[a]  # always a variable
            valb=status[b] if b in status else int(b)
        except IndexError:
            raise ValueError(f"Missing operands for '{inst}' at pc={pc}")
        except KeyError:
            raise ValueError(f"Invalid variable names at pc={pc}")
        except ValueError:
            raise ValueError(f"Value {b} at pc={pc+2} should an integer")
                
        if inst=="add":
            status[a] = vala + valb    
        elif inst=="mod":
            assert vala >= 0 and valb>0  
            status[a] = vala % valb
        elif inst=="div":
            assert valb!=0
            status[a] = vala//valb
        elif inst=="mul":
            status[a] = vala * valb    
        elif inst=="eql":
            status[a] = 1 if vala==valb else 0
        else:
            raise ValueError(f"Invalid instruction at pc={pc}")
        pc+=3
    return status

def readdata():
    codeblock=53
    inputnum=14
    code=None
    with open("input24.txt") as f:
        code=f.read().split()
    parameters=[(int(code[codeblock*i+13]),
               int(code[codeblock*i+16]),
               int(code[codeblock*i+46])) for i in range(inputnum)]
    return parameters
    
def log26(z):
    if z==0:
        return 1
    d=0
    while z>0:
        z = z//26
        d+=1
    return d
        
def solve_slow():
    params=readdata()
    stages=len(params)
    pops=[0]*stages
    pops[-1]=1 if params[-1][0]==26 else 0
    for i in range(len(params)-2,-1,-1):
        pops[i]=pops[i+1]
        if params[i][0]==26:
            pops[i]+=1
    DB={0:('','')}
    for i in range(stages):
        #print(f"Step {i:>2}: ",end="")
        NDB={}
        for z in DB:
            if z>=26**pops[i]:
                continue
            mintext,maxtext=DB[z]
            for w in "123456789":
                iw=int(w)
                nz=next_z(z,i,iw,params)
                maybe_mintext=mintext+w
                maybe_maxtext=maxtext+w
                if nz in NDB:
                    new_mintext=min(NDB[nz][0],maybe_mintext)
                    new_maxtext=max(NDB[nz][1],maybe_maxtext)
                    NDB[nz] = new_mintext,new_maxtext
                else:
                    NDB[nz]=maybe_mintext,maybe_maxtext
        DB=NDB
        #print(f" {len(DB):>10} confs.",end='')
        #print()
        
    print(DB[0][0])
    print(DB[0][1])

def solution_space(params):
    """Solves AoC 2021 part1,2

Using analysis of the problem and of the input data,
we can infer that the solutions are characterized by
7 equations between disjoint pairs of digits.

We extract the equations and produce the space of solutions."""
    for a,b,c in params:
        assert a!=1 or b>9
        assert 0<c<17
    stack=[]
    equations=[]
    i=0
    for a,b,c in params:
        if a==1:
            assert b>9 # must be a push
            stack.append((i,c))
        else:
            # an equation only involves two
            # digits
            w,coeff = stack.pop()
            equations.append((w,coeff+b,i))
        i+=1
    assert len(stack)==0
    S={}
    for eq in equations:
        w0,delta,w1=eq
        S[w0,w1]=[]        
        for v in range(9,0,-1):
            if 1<= v+delta <=9:
                #possible solution
                S[w0,w1].append((v,v+delta))
    return S      

def solve():
    """ Maximum valid number"""
    params=readdata()
    smallest=[0]*len(params)
    largest =[0]*len(params)
    S=solution_space(params)
    for e in S:
        l,r = e
        assert l<r
        smallest[l],smallest[r]=min(S[e])
        largest [l],largest [r]=max(S[e])
    smVal=0
    lgVal=0
    for i in range(len(params)):
        smVal *=10
        lgVal *=10
        assert 1<=smallest[i]<=9
        assert 1<=largest [i]<=9
        smVal +=smallest[i]
        lgVal +=largest[i]
    print(smVal)
    print(lgVal)
        
        
if __name__ == "__main__":
    #solve_slow()
    solve()
