
def readdata():
    with open("day2.txt") as f:
        text=f.read()
    data=text.split(",")
    return [int(x) for x in data]

def execute(code):
    i = 0
    while code[i]!=99:
        opcode=code[i]
        a=code[code[i+1]]
        b=code[code[i+2]]
        dest=code[i+3]
        if opcode==1:
            code[dest]=a+b
        elif opcode==2:
            code[dest]=a*b
        i+=4
    return

def runcode(code,i1,i2):
    X=code[:]
    X[1]=i1
    X[2]=i2
    execute(X)
    return X[0]
    
if __name__=="__main__":
    desiredoutput=19690720
    code = readdata()
    print(runcode(code,12,2))
    memsize=len(code)
    for a in range(memsize):
        for b in range(memsize):
            if runcode(code,a,b)==19690720:
                print(a*100+b)
        
            
        
    