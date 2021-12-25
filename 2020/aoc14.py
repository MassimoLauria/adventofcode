import re
        
def readmask(mask):
    andmask=0
    ormask =0
    for c in mask:
        if c=='x' or c=='X': 
            a = 1
            o = 0
        elif c=='1':
            a = 1
            o = 1
        elif c=='0':
            a = 0
            o = 0
        else:
            assert False
        andmask = (andmask << 1) | a
        ormask  = ( ormask << 1) | o
    return andmask,ormask


def parsedata(text):
    assign=re.compile('\s*mem\[\s*(?P<address>\d+)\s*\]\s*=\s*(?P<value>\d+)')
    mask=re.compile('\s*mask\s*=\s*(?P<mask>[xX01]*)')
    I = []
    lines = text.split('\n')
    for line in lines:
        m=assign.match(line)
        if m:
            I.append(m.groupdict())
            continue
        m=mask.match(line)
        if m:
            I.append(m.groupdict())
            continue
    return I
    

def execute(code):
    mem = {}
    andmask=2^36-1
    ormask=0
    for codeline in code:
        if 'mask' in codeline:
            andmask,ormask=readmask(codeline['mask'])
        else:
            index = int(codeline['address'])
            value = int(codeline['value'])
            mem[index] = (value & andmask) | ormask
    return mem


def genxors(value,mask,bitidx=None):
    if bitidx is None:
        bitidx = len(mask) -1

    if bitidx < 0:
        yield value
        return
    
    B=mask[len(mask)-1 - bitidx]
    if B=='0':
        yield from genxors(value,mask,bitidx-1)
    elif B=='1':
        yield from genxors(value | (2**bitidx),mask,bitidx-1)
    else: # B=='X'
        yield from genxors(value,mask,bitidx-1)
        yield from genxors(value ^ (2**bitidx),mask,bitidx-1)
   
    

def execute2(code):
    mem = {}
    mask='0'*36
    
    for codeline in code:
        if 'mask' in codeline:
            mask=codeline['mask']
        else:
            base  = int(codeline['address'])
            value = int(codeline['value'])
            for address in genxors(base,mask):
                mem[address] = value
    return mem

def part1():
    with open('aoc14input.txt') as f:
        text = f.read()
    code = parsedata(text)
    mem = execute(code)
    print(sum(mem.values()))

def part2():
    with open('aoc14input.txt') as f:
        text = f.read()
    code = parsedata(text)
    mem = execute2(code)
    print(sum(mem.values()))
part1()
part2()
