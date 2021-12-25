
def parseexp(text):
    digit='0123456789'
    exp=[]
    stack=[exp]
    for c in text:
        if c in digit:
            stack[-1].append(int(c))
        elif c == ' ' or c=='\n':
            continue
        elif c in '+*':
            stack[-1].append(c)
        elif c == '(':
            l = []
            stack[-1].append(l)
            stack.append(l)
        elif c == ')':
            stack.pop()
        else:
            raise ValueError('Invalid char')
    assert exp == stack[-1]
    return exp

def evalflat(flat):
    # eval global
    value=flat[0]
    for i in range(2,len(flat),2):
        nvalue=flat[i]
        op = flat[i-1]
        if op=='+':
            value = value + nvalue
        elif op=='*':
            value = value * nvalue
        else:
            raise ValueError('Invalid expression')
    return value

def evalflat2(flat):
    # eval plus
    temp=[flat[0]]
    for i in range(1,len(flat),2):
        if flat[i]=='+':
            temp[-1] = temp[-1] + flat[i+1]
        else:
            temp.append(flat[i+1])
    # eval muls
    res=1
    for x in temp:
        res *= x
    return res
 
def evaluate(exp,ef=evalflat):
    if type(exp)==int:
        return exp
    elif len(exp)==0:
        raise ValueError("Emtpy Expression")
    elif len(exp)%2 != 1:
        raise ValueError("Invalid Expression")

    # evaluate nested
    flat = [evaluate(exp[0],ef=ef)]
    for i in range(2,len(exp),2):
        flat.append(exp[i-1])
        flat.append(evaluate(exp[i],ef=ef))
    return ef(flat)
        
    
def part1():
    with open('aoc18input.txt') as f:
        data=f.readlines()
    somma=0
    for e in data:
        somma += evaluate(parseexp(e))
    print(somma)

def part2():
    with open('aoc18input.txt') as f:
        data=f.readlines()
    somma=0
    for e in data:
        x = evaluate(parseexp(e),ef=evalflat2)
        somma += x
    print(somma)

part1()
part2()