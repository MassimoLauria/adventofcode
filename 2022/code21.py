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
        a,b = b % a,a
    return b

def myeval(IS,m):
    # each value is ( a,b,c,d ) and represets (a/c x + c/d )
    if m == "humn" and m not in IS: # missing value
        IS[m]=(1,0)

    if type(IS[m])==int:  # evaluated int
        IS[m] = (0,IS[m])

    if len(IS[m]) == 2: # evaluated linear
        return IS[m]

    l,o,r = IS[m]
    lv = myeval(IS,l)
    rv = myeval(IS,r)
    if o=='+':
        IS[m] = ( lv[0]+rv[0] , lv[1]+rv[1] )
    elif o == '*':
        assert lv[0] == 0 or rv[0] == 0
        IS[m] = ( lv[1] * rv[0] + lv[0] * rv[1] , lv[1] * rv[1] )
    elif o == '-':
        IS[m] = ( lv[0]-rv[0] , lv[1]-rv[1] )
    elif o == '/':
        assert rv[0] == 0 and rv[1] != 0
        IS[m] = ( lv[0] / rv[1] , lv[1] / rv[1] )
    else:
        assert False
    return IS[m]



def part1(data=None):
    """solve part 1"""
    IS = readdata(data)
    # print(IS)
    print("part1:",myeval(IS,'root')[1])


def part2(data=None):
    """solve part 2"""
    IS = readdata(data)
    IS['root'] = IS['root'][0],'-',IS['root'][2]
    #print(IS)
    del IS['humn']
    a,b = myeval(IS,'root')
    x = -b / a
    print(a,b)
    print("part2:",int(x))

if __name__ == "__main__":
    part1(EXAMPLE)
    part1()
    part2(EXAMPLE)
    part2()
