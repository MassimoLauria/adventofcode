from itertools import product,permutations

# bottom level first, then ascending
example  = ["ADCA", "BCBD"]
exercise = ["CCAB", "DBDA"]

example2  = ["ADCA", "DBAC", "DCBA", "BCBD"]
exercise2 = ["CCAB", "DBAC", "DCBA", "DBDA"]

# a configuration is a sequence of 15 integers
#
# A are 1; B are 2; C are 3; D are 4
# 0 is unoccupied
#
# in the configuration we have (part1)
# pos 0,1,2,3 for the bottom level
# pos 4,5,6,7 for the top level
# pos 8-14 for the 7 usable positions in the hall way

# in the configuration we have (part2)
# pos 0,1,2,3   for the bottom level
# pos 4,5,6,7   for the second level from below
# pos 8,9,10,11 for the third level from below
# pos 12,13,14,15 for the top level from below
# pos 16-22 for the 7 usable positions in the hall way
  
#
# configuration values
#  0 - final
#  positive integer - minimum cost to final
#  None - stall
CONFS={ }
#
# PATHS[(i,j)] = positions traversed going from i to j and cost
PATHS={}

def initial_configuration(data):
    conf=[0]*(7+4*len(data))
    for i in range(4):
        for j in range(len(data)):
            c = data[j][i]
            conf[i+4*j]=ord(c)-ord('A')+1
    return tuple(conf)    

def printconf(conf):

    table={0:".", 1:"A",2:"B",3:"C",4:"D"}
    def c(i):
        return table[conf[i]]
    if len(conf)==15:
        text="#############\n" + \
             "".join(["#", c(8), c(9), '.', c(10), '.', c(11), '.', c(12), '.', c(13),c(14),"#\n"]) + \
             "".join(["###", c(4), "#", c(5), "#", c(6),"#", c(7),"###\n"]) +\
             "".join(["  #", c(0), "#", c(1),"#", c(2),"#", c(3), '#\n']) +\
             "  #########"
    elif len(conf)==23:
        text= "#############\n" + \
              "".join(["#", c(16), c(17), '.', c(18), '.', c(19), '.', c(20), '.', c(21),c(22),"#\n"]) + \
              "".join(["###", c(12), "#", c(13), "#", c(14),"#", c(15),"###\n"]) +\
              "".join(["  #", c(8), "#", c(9),"#", c(10),"#", c(11), '#\n']) +\
              "".join(["  #", c(4), "#", c(5), "#", c(6),"#", c(7),"#\n"]) +\
              "".join(["  #", c(0), "#", c(1),"#", c(2),"#", c(3), '#\n']) +\
              "  #########"
    else:
        raise ValueError
    print(text)    

def precompute_paths(roomsize=2):
    
    hallway=list(range(roomsize*4,roomsize*4+7))
    scheme=hallway[:]
    scheme.insert(5,3)
    scheme.insert(4,2)
    scheme.insert(3,1)
    scheme.insert(2,0)
    
    paths={}
    
    for i,j in product(range(4),hallway):
        # room i, hallway position j
        a = scheme.index(i)
        b = scheme.index(j)
        if a<b:
            c = b-a
            p =scheme[a:b+1]
        else:
            c = a-b
            p =scheme[b:a+1]
            p.reverse()
        p = [x for x in p if x>=hallway[0] ] 
        for k in range(roomsize):
            # position k in the room 0-bottom
            prefix = list(range(i+4*(k+1),i+4*roomsize,4))
            paths[(i+4*k,j)] = prefix + p[:]
            paths[(i+4*k,j)] = (paths[(i+4*k,j)],c+1+len(prefix))
        
    # descending paths
    pairs=list(paths.keys())
    for i,j in pairs:
        p,c = paths[i,j]
        p   = p[:]
        p.reverse()
        p.pop(0) # remove j
        p.append(i)
        paths[j,i] = (p,c)
    
    return paths


def costofmove(conf,i,j):
    amph=conf[i]
    assert conf[i]!=0
    p,c = PATHS[i,j]
    for x in p:
        if conf[x]!=0:
            return float('inf')
    return c * (10**(amph-1))

def search(conf):
    
    if conf in CONFS:
        return CONFS[conf]

    # Roomsize
    roomsize=(len(conf)-7) // 4
    hallway=range(4*roomsize,4*roomsize+7)
    
    moves=[]
    poppable=[]
    pushable=[]
    for i in range(4):
        
        # analyze room i
        rscore=0
        while rscore<roomsize:
            if conf[i+4*rscore]!=i+1:
                break
            rscore+=1
        rsize=rscore
        while rsize<roomsize:
            if conf[i+4*rsize]==0:
                break
            rsize+=1
        if rscore < roomsize: # room not complete
            if rscore < rsize: # wrong elements in room
                poppable.append(i+4*rsize-4)
            else:             # no wrong elements
                pushable.append(i+4*rsize)
    
    # Try all movements from room
    for dest in hallway:
        for src in poppable:
            c = costofmove(conf,src,dest)
            moves.append((src,dest,c))

    # move someone from the hallway
    for src in hallway:
        amph=conf[src]
        if amph==0:
            continue
        for dest in pushable:
            if amph-1 != dest % 4:
                continue
            c = costofmove(conf,src,dest)
            moves.append((src,dest,c))
    
    bestcost=float('inf')
    for i,j,c in moves:
        if c==float('inf') or c>bestcost:
            continue
        newconf=list(conf)
        newconf[i],newconf[j] = newconf[j],newconf[i]
        newconf = tuple(newconf)
        if newconf in CONFS:
            newcost = CONFS[newconf]
        else:
            newcost = search(newconf)
        bestcost=min(bestcost,c+newcost)
    
    CONFS[conf] = bestcost
    return CONFS[conf]
        
def solve(data):
    global CONFS
    global PATHS
    
    roomsize=len(data)
    
    start = initial_configuration(data)
    target= tuple([1,2,3,4]*roomsize+[0]*7)
    
    CONFS.clear()
    CONFS[target]=0
    
    PATHS=precompute_paths(roomsize)
    
    x = search(start)
    print(x)

def part3(roomsize):
    global CONFS
    global PATHS
    
    target= tuple([1,2,3,4]*roomsize+[0]*7)

    CONFS.clear()
    CONFS[target]=0
    
    PATHS=precompute_paths(roomsize)
    
    if roomsize==2:
        start_conf=set()
        for s in permutations("AABBCCDD"):
            start_conf.add(s)
        start_conf = [[s[:4],s[4:]] for s in start_conf]
    elif roomsize==4:
        start_conf = [["ABCD", "DBAC", "DCBA", s] for s in permutations("ABCD")]
    else:
        raise ValueError
        
    sumcost=0
    mincost=float('inf')
    not_valid=0
    i=1
    tot=len(start_conf)
    for s in start_conf:
        start = initial_configuration(s)
        if i % 10 == 0:
            print(f"Working out start conf {i} of {tot}")
            printconf(start)
        x = search(start)
        if x!=float('inf'):
            sumcost+=x
            mincost=min(x,mincost)
        else:
            not_valid+=1
        i+=1
    print("Sum:",sumcost)
    print("Min:",mincost)
    print("Invalid starts:",not_valid)



if __name__ == "__main__":
    #solve(example)  # 12521
    solve(exercise) # 14460 - part1
    #solve(example2) # 44169
    solve(exercise2) # part 1
    #part3(4)
    #part3(2)


    

    







