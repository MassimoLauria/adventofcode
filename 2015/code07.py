"""Advent of Code 2015 day 07
"""

EXAMPLE = """
123 -> x
456 -> y
x AND y -> d
x OR y -> e
x LSHIFT 2 -> f
y RSHIFT 2 -> g
NOT x -> h
NOT y -> i
"""

MASK=(1<<16)-1

def readcircuit(data=None):
    """Read and parse the input data"""
    if data is None:
       with open("input07.txt") as f:
            data = f.read()

    ls=data.splitlines()
    C = {}
    for l in ls:
        l = l.split()
        if not (3<=len(l)<=5): continue
        wire = l[-1]
        if len(l)==3:
            C[wire]=l[0]
        elif len(l)==4: # unary operand
            C[wire]=(l[0],l[1])
        else:           # binary operand
            C[wire]=(l[1],l[0],l[2])
    return C

def ceval(C,wire=None):
    if wire is None:
        for wire in C:
            ceval(C,wire)
        return

    if type(wire)==int: #constant
        return wire

    elif type(wire)==str and wire.isdigit(): #constant
        return int(wire)

    # Wired values
    if type(C[wire])==int:
        return C[wire]
    if type(C[wire])==str:
        v = ceval(C,C[wire])
        C[wire] = v
        return C[wire]

    a = ceval(C,C[wire][1])
    b = ceval(C,C[wire][2]) if len(C[wire])>2 else None

    if C[wire][0]=='NOT':
        C[wire]=(~ a) & MASK

    elif C[wire][0]=='WIRE':
        C[wire]=a

    elif C[wire][0]=='LSHIFT':
        C[wire]=(a << b) & MASK

    elif C[wire][0]=='RSHIFT':
        C[wire]=(a >> b)

    elif C[wire][0]=='AND':
        C[wire]=(a & b)

    elif C[wire][0]=='OR':
        C[wire]=(a | b)

    return C[wire]


def part1(data=None):
    """solve part 1"""
    C = readcircuit(data)
    if 'a' in C:
        ceval(C,'a')
        print(C['a'])
    else:
        print(C)

def part2(data=None):
    """solve part 2"""
    C = readcircuit(data)
    override = ceval(C,'a')
    C = readcircuit(data)
    C['b'] = override
    value  = ceval(C,'a')
    print(value)

if __name__ == "__main__":
    part1(EXAMPLE)
    part1()
    part2()
