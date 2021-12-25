import numpy as np
from itertools import combinations,permutations,product
from collections import defaultdict,Counter

# Known position/orientation of scanners
POSITION=None
ORIENTATION=None
SCANNERS=None
ROTATIONS=None
DISTANCESQ=None
    
def build24rotations():
    """Build rotation matrices

    Build all 24 matrices representing 90 degrees rotations around
    the X,Y,Z axis.
    
    These are essentially all permutation
    matrices + -1,1 signs for each axis.
    
    But only 24 of these 48 are rotation matrices without
    reflection. The ones with determinant 1.
    """
    rots=[]
    for a,b,c in permutations([0,1,2]):
        for sa,sb,sc in product([1,-1],repeat=3):
            M = np.zeros((3,3),dtype='int')
            M[0,a] = sa
            M[1,b] = sb
            M[2,c] = sc
            if np.linalg.det(M)==1.0:
                rots.append(M)
    return rots
    

def loaddata(fname):
    data=[]
    prefix="--- scanner"
    with open(fname) as f:
        for l in f:
            l=l.strip()
            if len(l)==0:
                continue
            if l[0:len(prefix)]==prefix:
                data.append([])
                continue
            x,y,z=l.split(',')
            data[-1].append([int(x),int(y),int(z)])

    for i in range(len(data)):
        data[i]=np.array(data[i],dtype='int')

    return data


def setupdata(datafile="input19_test.txt"):
    global POSITION
    global ORIENTATION
    global SCANNERS
    global ROTATIONS
    global DISTANCESQ
    
    # Known position/orientation of scanners
    POSITION={}
    ORIENTATION={}
    SCANNERS=loaddata(datafile)
    ROTATIONS=build24rotations()
    DISTANCESQ=[]
    
    for s in range(0,len(SCANNERS)):
        ds=set()
        for a,b in combinations(SCANNERS[s],2):
             ds.add(np.dot(a-b,a-b))
        DISTANCESQ.append(ds)
         

def trymatch(A,B):
    # Works in the assumption that there
    # is either one solution or none.
    offsets=defaultdict(lambda:0)
    for ba in A:
        for bb in B:
            offsets[tuple(ba - bb)]+=1
    max_value = max(offsets, key=offsets.get)
    if offsets[max_value]>=12:
        return np.array(max_value)
    else:
        return None


def solve():
    POSITION[0]=np.array([0,0,0])
    queue=[0]

    while len(queue)>0:

        a = queue.pop(0)
        A = SCANNERS[a]
        DA= DISTANCESQ[a]
        
        for b in range(len(SCANNERS)):
            
            if b in POSITION:
                continue
            
            # First check if beacon sets have 66
            # distances in common
            # If not it means they do not have 12
            # overlapping points.
            DB=DISTANCESQ[b]
            rank=len(DA.intersection(DB))
            if rank<12*11//2:
                continue
            
            for rot in ROTATIONS:
                B = SCANNERS[b] @ rot
                pos = trymatch(A,B)
            
                if pos is not None:
                    # solved
                    SCANNERS[b] = B + pos
                    POSITION[b] = pos
                    queue.append(b)
                    break
                
    if len(SCANNERS) != len(POSITION):
        raise ValueError("Puzzle not trivially solvable")


def part1(fname):
    setupdata(fname)
    solve()
    N=len(SCANNERS)
    B=np.concatenate([SCANNERS[i] for i in range(N)],axis=0)
    B=np.unique(B,axis=0)
    print(len(B))

def part2():
    maxdist=-1
    N=len(SCANNERS)
    for a,b in combinations(range(N),2):
        x=POSITION[a]-POSITION[b]
        dist=abs(x[0])+abs(x[1])+abs(x[2])
        maxdist=max(dist,maxdist)
    print(maxdist)
            

if __name__ == "__main__":
    part1("input19_test.txt")
    part2()
    part1("input19.txt")
    part2()
    