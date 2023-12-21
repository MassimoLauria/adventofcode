"""Advent of Code 2023 day 20
"""

from collections import defaultdict, deque
import math

LOW=0
HIGH=1
ON=1
OFF=0

TYPE_SPECIAL=0
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

def inputs(C):
    inputs=defaultdict(list)
    for g in C:
        for dest in C[g][2]:
            inputs[dest].append(g)
    for d in inputs:
        print(d,inputs[d])


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
            Circ[gate]=[typeg,OFF,outputs]
        elif gate[0]=="&": #conjunctions
            typeg=TYPE_CONJ
            outputs=line[1].split(', ')
            Circ[gate]=[typeg,{},outputs]
        elif gate=="broadcaster":
            typeg=TYPE_SPECIAL
            outputs=line[1].split(', ')
            Circ[gate]=[typeg,None,outputs]
        else:
            continue

        if 'rx' in outputs:
            Circ['%rx']=[TYPE_FFLOP,None,[]]
        if 'output' in outputs:
            Circ['output']=[TYPE_SPECIAL,None,[]]
    # put tags in front of gate names
    for src in Circ:
        for i in range(len(Circ[src][2])):
            dest = Circ[src][2][i]
            if "&"+dest in Circ:
                Circ[src][2][i] = "&"+dest
            elif "%"+dest in Circ:
                Circ[src][2][i] = "%"+dest

    for src in Circ:
        for dest in Circ[src][2]:
            if Circ[dest][0]==TYPE_CONJ:
                Circ[dest][1][src] = LOW
    return Circ

def reset(Circ):
    for src in Circ:
        if Circ[src][0]==TYPE_FFLOP:
            Circ[src][1]=OFF
        elif Circ[src][0]==TYPE_CONJ:
            for x in Circ[src][1]:
                Circ[src][1][x]=LOW

def dotgraph(C):
    def conv(g):
        if g[0]=="%":
            return g[1:]
        elif g[0]=="&":
            return f"A_{g[1:]}"
        else:
            return g

    print("digraph {")
    print('     rankdir="LR"')
    for gate in C:
        for dest in C[gate][2]:
            print(f"  {conv(gate)}  -> {conv(dest)};")
    print("}")

def run_pulse(C,pulse_value,monitor_node=None):
    Q=deque()
    pulse_count ={HIGH:0,LOW:0}
    if monitor_node is None:
        pulse_count[pulse_value]+=1
    for gate in C['broadcaster'][2]:
        Q.append(("broadcaster",pulse_value,gate))
    while len(Q)>0:
        src,pulse,dest=Q.popleft()
        # if src in ['&kb','&nh','&fd','&mf'] and dest[0]=='&' and pulse==LOW:
        #     print(src,"-high->" if pulse else "-low->",dest)
        # if src in ['&vn','&ph','&kt','&hn'] and pulse==HIGH:
        #     print(src,"-high->" if pulse else "-low->",dest)

        if monitor_node is None or monitor_node==src:
            pulse_count[pulse]+=1

        outs=[]
        if C[dest][0]==TYPE_FFLOP and pulse==LOW:
            C[dest][1] = 1 - C[dest][1]
            new_pulse=HIGH if C[dest][1]==ON else LOW
            outs=    C[dest][2]
        elif C[dest][0]==TYPE_CONJ:
            C[dest][1][src] = pulse
            # if dest=='&kc':
            #     print(C[dest])
            new_pulse = LOW if all(C[dest][1].values()) else HIGH
            outs=    C[dest][2]

        # send pulses
        for g in outs:
            Q.append((dest,new_pulse,g))
    return pulse_count[HIGH],pulse_count[LOW]


def part1(data=None):
    """solve part 1"""
    C=readdata(data)
    high,low=0,0
    for i in range(1000):
        h,l = run_pulse(C,LOW)
        high+=h
        low+=l
    print(high*low)

def part2(data=None):
    """solve part 2"""
    C=readdata(data)
    # Gates to monitor
    last_and="&kc"
    important_nodes=[]
    for g in C:
        if last_and in C[g][2]:
            important_nodes.append(g)
    periods=[]
    for g in important_nodes:
        reset(C)
        for i in range(1,5000):
            h,l = run_pulse(C,LOW,monitor_node=g)
            if h>0:
                periods.append(i)
                break
    print(math.lcm(*periods))


def explore_circuits(data=None):
    """solve part 1"""
    C=readdata(data)
    #dotgraph(C)
    periods=[4021,3907,4093,3797]
    print(f" ------------------ Start ----------")
    log_circuit(C)
    print(f" ------------------ Start ----------")
    for i in range(1,15001):
        run_pulse(C,LOW)
        log=False
        for p in periods:
            if i%p==0 or i%p==(p-1):
                log=True
        if log:
            log_circuit(C)
            print(f" ------------------ End of step {i} ----------")
    #values=defaultdict(list)
    #run_freq(C,(1,0))


periods=[4021,3907,4093,3797]

def log_circuit(C):
    reg1=['tn','md','hh','tc','td','bm','mr','rs','dh','lt','cq','kx',"kb"]
    reg2=['nx','dj','qm','mj','zv','tk','mc','kh','ck','sr','jh','pt',"nh"]
    reg3=['bx','jg','tv','qx','rt','kg','lg','qj','qt','gb','qs','bl',"fd"]
    reg4=['nr','jp','ps','fh','dp','bt','rz','gq','hc','hv','bz','rb',"mf"]
    show_counter(C,reg1)
    show_counter(C,reg2)
    show_counter(C,reg3)
    show_counter(C,reg4)
    print(C['&kc'][1])

def show_counter(C,reg):
    assert C["&"+reg[-1]][0]==TYPE_CONJ
    for i in range(len(reg)-1):
        assert C["%"+reg[i]][0]==TYPE_FFLOP
    for i in range(len(reg)-1):
        print(C["%"+reg[i]][1],end="")
    print("  -- &"+reg[-1]+"==",end="")
    for i in range(len(reg)-1):
        if "%"+reg[i] in C["&"+reg[-1]][1]:
            print(C["&"+reg[-1]][1]["%"+reg[i]],end="")
        else:
            print('*',end="")
    print()

if __name__ == "__main__":
    part1(EXAMPLE)
    part1(EXAMPLE2)
    part1()
    part2()
    #print(math.lcm(*periods))
