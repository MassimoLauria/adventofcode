"""Advent of Code 2023 day 20
"""

from collections import deque

LOW=False
HIGH=True
ON=True
OFF=False

TYPE_RELAY=0
TYPE_FFLOP=1
TYPE_CONJ=2

EXAMPLE = """broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a
"""
EXAMPLE2 = """broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output
"""


def readdata(data=None):
    """Read and parse the input data"""
    if data is None:
       with open("input20.txt") as f:
            data = f.read()
    data=data.splitlines()
    Circ={}
    for line in data:
        line=line.split(' -> ')
        gate=line[0]
        if gate[0]=="%": #flip flop
            typeg=TYPE_FFLOP
            outputs=line[1].split(', ')
            Circ[gate[1:]]=[typeg,OFF,outputs]
        elif gate[0]=="&": #flip flop
            typeg=TYPE_CONJ
            outputs=line[1].split(', ')
            Circ[gate[1:]]=[typeg,{},outputs]
        elif gate=="broadcaster": #flip flop
            typeg=TYPE_RELAY
            outputs=line[1].split(', ')
            Circ[gate]=[typeg,None,outputs]
    # init conjunctions
    wires=[]
    for src in Circ:
        for dest in Circ[src][2]:
            if dest not in Circ:
                continue
            elif Circ[dest][0]==TYPE_CONJ:
                Circ[dest][1][src] = LOW
    return Circ

def run_pulse(C,pulse_value):
    Q=deque()
    accumulator=0
    pulse_count ={HIGH:0,LOW:0}
    pulse_count[pulse_value]+=1
    for gate in C['broadcaster'][2]:
        Q.append(("broadcaster",pulse_value,gate))
    while len(Q)>0:
        src,pulse,dest=Q.popleft()
        #print(src,"-high->" if pulse else "-low->",dest)
        pulse_count[pulse]+=1

        if dest == 'rx' and pulse==LOW:
            accumulator += 1
        if dest not in C:
            continue
        if C[dest][0]==TYPE_FFLOP and pulse==HIGH:
            continue

        elif C[dest][0]==TYPE_FFLOP and pulse==LOW:
            C[dest][1] = not C[dest][1]
            new_pulse=HIGH if C[dest][1]==ON else LOW
        elif C[dest][0]==TYPE_CONJ:
            C[dest][1][src] = pulse
            value=all(C[dest][1].values())
            new_pulse = LOW if value else HIGH
        # send pulses
        for g in C[dest][2]:
            Q.append((dest,new_pulse,g))
    return accumulator,pulse_count[HIGH],pulse_count[LOW]


def part1(data=None):
    """solve part 1"""
    C=readdata(data)
    high,low=0,0
    for i in range(1000):
        _,h,l = run_pulse(C,LOW)
        high+=h
        low+=l
    print(high*low)

def part2(data=None):
    """solve part 1"""
    C=readdata(data)
    accumulator=0
    i=0
    while accumulator<1:
        i+=1
        accumulator,_,_ = run_pulse(C,LOW)
        print(C)
        print(accumulator)
    print(i)

if __name__ == "__main__":
    part1(EXAMPLE)
    part1(EXAMPLE2)
    part1()
    part2()
