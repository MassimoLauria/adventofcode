
def readsource():
    code=[]
    with open('aoc8input.txt') as f:
        for srcline in f:
            op,arg = srcline.split()
            arg=int(arg)
            code.append([op,arg])
    return code

def execute(code):
    PC=0
    visited=[False]*len(code)
    acc=0
    while PC<len(code):
        if visited[PC]:
            return acc,True
        
        visited[PC]=True
        op = code[PC][0]
        arg= code[PC][1]
        
        if op == 'jmp':
            PC += arg
        elif op=='acc':
            acc += arg
            PC  += 1
        else:
            PC  += 1
    return acc,False
            
        
def part1():
    code=readsource()
    x,loop=execute(code)
    assert loop
    print(x)
    
    
def part2():
    code=readsource()
    for i in range(len(code)):
        
        if code[i][0]=='acc':
            continue

        if code[i][0]=='jmp':
            code[i][0]='nop'
        elif code[i][0]=='nop':
            code[i][0]='jmp'
    
        res,loop = execute(code)
        
            
        if code[i][0]=='jmp':
            code[i][0]='nop'
        elif code[i][0]=='nop':
            code[i][0]='jmp'
        
        if not loop:
            print(res)
part1()   
part2()