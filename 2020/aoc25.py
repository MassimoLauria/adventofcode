
example={'card': 5764801, 'door':17807724}

puzzle={'card' : 6929599, 'door': 2448427}

def isprime(N):
    i=2
    while i*i <=N:
        if N % i ==0:
            return i
        i+=1
    return 1

def factor(N):
    x=isprime(N)
    if x>1:
        return [x]+factor(N//x)
    else:
        return [N]

def binary(value):
    bits=[]
    while value!=0:
        bits.append(value%2)
        value = value//2
    bits.reverse()
    return bits
    
def expmod(base,exp,mod):
    value=1
    exp=binary(exp)
    for b in exp:
        value = value**2
        if b == 1:
            value = value * base
        value = value % mod
    return value

def pubkey(secret,subjectnumber=7):
    value=1
    mod=20201227
    
    return expmod(subjectnumber,secret,mod)
                
def bruteforce_findsecret(pubkey,subjectnumber=7):
    mod=20201227
    out=[]
    pkfactors=factor(pubkey)
    #print('Reverse {} via factors {}'.format(pubkey,pkfactors))
    for f in pkfactors:
        value=1
        l=0
        while value!=f:
            l+=1
            value= (value*subjectnumber) % mod
            #print('{}: val {}'.format(l,value))
        out.append(l)
    return sum(out) % (mod - 1)
    
def part1():
    #print('Crack example')
    #secret=bruteforce_findsecret(example['card'])
    #enc=pubkey(secret,subjectnumber=example['door'])
    #print('Encription key of example:',enc)
    #print('\nCrack puzzle')
    secret=bruteforce_findsecret(puzzle['card'])
    enc=pubkey(secret,subjectnumber=puzzle['door'])
    #print('Encription key of puzzle:',enc)
    print(enc)

part1()