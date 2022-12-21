"""Advent of Code 2022 day 21
"""

EXAMPLE = """
root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32
"""

def readdata(data=None):
    """Read and parse the input data"""
    if data is None:
       with open("input21.txt") as f:
            data = f.read()
    IS = {}
    for line in data.splitlines():
        if len(line)==0: continue
        monkey,instr = line.split(": ")
        assert monkey not in IS
        try:
            IS[monkey] = int(instr)
        except ValueError:
            IS[monkey] = (instr[:4],instr[5],instr[7:11])
    return IS

def gdc(a,b):
    a,b = abs(a),abs(b)
    if a>b: a,b = b,a
    assert a!=0 or b!=0
    while (a!=0):
        a,b = (b % a), a
    return b

def sumQ(q,p):
    n1,d1 = q
    n2,d2 = p
    N = n1*d2 + n2*d1
    D = d1*d2
    t = gdc(N,D)
    return (N//t,D//t)

def mulQ(q,p):
    n1,d1 = q
    n2,d2 = p
    N = n1*n2
    D = d1*d2
    t = gdc(N,D)
    return (N//t,D//t)

def subQ(q,p):
    n1,d1 = q
    n2,d2 = p
    N = n1*d2 - n2*d1
    D = d1*d2
    t = gdc(N,D)
    return (N//t,D//t)

def divQ(q,p):
    n1,d1 = q
    n2,d2 = p
    N = n1*d2
    D = d1*n2
    t = gdc(N,D)
    return (N//t,D//t)

def myeval(IS,m):
    # each value is ( a,b,c,d ) and represets (a/c x + c/d )
    zero = (0,1)
    one  = (1,1)
    if m == "humn" and m not in IS: # missing value
        IS[m]=(one,zero)   # 1 x + 0

    if type(IS[m])==int:  # evaluated int
        IS[m] = ( zero , (IS[m],1))  # 0 x + IS[m]

    if len(IS[m]) == 2: # evaluated linear # qx+p
        #print(m,IS[m])
        return IS[m]

    l,o,r = IS[m]
    a1,b1 = myeval(IS,l)  # a1 x + b1
    a2,b2 = myeval(IS,r)  # a2 x + b2
    if o=='+':
        IS[m] = ( sumQ(a1,a2) , sumQ(b1,b2) )
    elif o == '*':
        assert a1 == zero or a2 == zero
        IS[m] = ( sumQ( mulQ(a1,b2), mulQ(a2,b1)) ,
                  mulQ(b1,b2) )
    elif o == '-':
        IS[m] = ( subQ(a1,a2), subQ(b1,b2))
    elif o == '/':
        assert a2 == zero and b2 != zero
        IS[m] = ( divQ(a1,b2), divQ(b1,b2))
    else:
        assert False
    #print((l,o,r),m,IS[m])
    return IS[m]



def part1(data=None):
    """solve part 1"""
    IS = readdata(data)
    #print(IS)
    a,b = myeval(IS,'root')
    assert a == (0,1)
    assert abs(b[1]) == 1 # an integer result
    print("part1:",b[0]//b[1])


def part2(data=None):
    """solve part 2"""
    zero = (0,1)
    IS = readdata(data)
    IS['root'] = IS['root'][0],'-',IS['root'][2]
    #print(IS)
    del IS['humn']
    a,b = myeval(IS,'root')
    x = divQ(subQ(zero,b),a)
    assert abs(x[1]) == 1 # an integer result
    print("part2:",x[0]//x[1])

if __name__ == "__main__":
    part1(EXAMPLE)
    part1()
    part2(EXAMPLE)
    part2()
