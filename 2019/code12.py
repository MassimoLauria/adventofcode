import numpy as np

example1=np.array([
    [-1, 0, 2],
    [2, -10, -7],
    [4, -8, 8],
    [3, 5, -1]])

example2=np.array([[-8,-10, 0],
        [5, 5, 10],
        [2, -7, 3],
        [9, -8, -3]])

exercise=np.array([[-1,7,3],
                   [12,2,-13],
                   [14,18,-8],
                   [17,4,-4]])

V=np.zeros_like(example1)
def gravity(P,V):
    for i,j in [(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)]:
         V[i]+=np.sign(P[j]-P[i])
         V[j]+=np.sign(P[i]-P[j])
        
def velocity(P,V):
    P += V

def potkin(P,V):
    p=np.sum(np.abs(P),axis=1)
    k=np.sum(np.abs(V),axis=1)
    return p,k

def printstatus(P,V):
    p,k=potkin(P,V)
    for i in range(4):
        print("{} - p:  {}\tv:  {} \tpot:{} kin:{}".format(i+1,P[i],V[i],p[i],k[i]))

def part1(P,steps=10):
    P = P.copy()
    V = np.zeros_like(P)
    #printstatus(P,V)
    for i in range(steps):
        gravity(P,V)
        velocity(P,V)
        #printstatus(P,V)
    p,k=potkin(P,V)
    print(np.dot(p,k))   

def updatedb(state,i,db):
    if state in db:
        old=db[state]
        return old,i
    else:
        db[state] = i
        return None

def part2(P):
    V = np.zeros_like(P)
    #printstatus(P,V)
    i=0
    initstatex=tuple(P[:,0])+tuple(V[:,0])
    initstatey=tuple(P[:,1])+tuple(V[:,1])
    initstatez=tuple(P[:,2])+tuple(V[:,2])
    statedbx={initstatex:0}
    statedby={initstatey:0}
    statedbz={initstatez:0}
    rx,ry,rz=None,None,None
    while True:
        gravity(P,V)
        velocity(P,V)
        i+=1
        currstatex=tuple(P[:,0])+tuple(V[:,0])
        currstatey=tuple(P[:,1])+tuple(V[:,1])
        currstatez=tuple(P[:,2])+tuple(V[:,2])
        if rx is None:
            rx=updatedb(currstatex,i,statedbx)
        if ry is None:
            ry=updatedb(currstatey,i,statedby)
        if rz is None:
            rz=updatedb(currstatez,i,statedbz)
        if rx is not None and ry is not None and rz is not None:
            break
    print(rx,ry,rz)
    print(np.lcm.reduce([rx,ry,rz]))
    
if __name__ == "__main__":
    part1(example1,steps=1000)   
    #part1(example2)
    #part1(exercise,steps=1000)
    part2(example1)
    part2(example2)
    part2(exercise)
    