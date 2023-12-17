"""Advent of Code 2023 day 17
"""

EXAMPLE = """2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533
"""

EXAMPLE2="""111111111111
999999999991
999999999991
999999999991
999999999991
"""

TURNS={ ">":"v^","<":"v^","v":"><","^":"><", "":"v>" }
DIRS={ ">":(0,1),"<":(0,-1),"v":(1,0),"^":(-1,0) }


def pqueue_make():
    return [],{}

def pqueue_priority(pq,item):
    heap,pos = pq
    idx = pos[item]
    return heap[idx][0]

def pqueue_promote(pq,pri,item):
    #assert is_pqueue(pq)
    heap,pos=pq
    if item in pos: # old element
        idx = pos[item]
        if heap[idx][0]<pri: return
        heap[idx]=(pri,item)
    else:
        idx = len(heap)
        heap.append((pri,item))
        pos[item]=idx
    # pull up promoted element
    while idx>0 and heap[(idx-1)//2][0]>pri:

        p_idx   = (idx-1)//2
        p_item  = heap[p_idx][1]

        heap[idx],heap[p_idx]=heap[p_idx],heap[idx]
        pos[item],pos[p_item]=pos[p_item],pos[item]
        idx = p_idx
    #assert is_pqueue(pq)


def is_pqueue(pq):
    L,pos=pq
    if len(L)!=len(pos):
        print("Wrong length")
        return False
    for i in range(1,len(L)):
        if L[(i-1)//2][0]>L[i][0]:
            print("Wrong order")
            return False
    for i in range(len(L)):
        if L[i][1] not in pos:
            print("Wrong elements in dict")
            return False
    return True

def pqueue_pop(pq):
    #assert is_pqueue(pq)
    if len(pq[0])==0:
        raise ValueError("Empty queue")
    heap,pos=pq
    result=heap[0]
    pos.pop(result[1])
    heap[0]  = heap[-1]
    heap.pop()
    if len(heap)==0: # no more elements
        return result
    pri,item = heap[0]
    pos[item]=0
    # push down element to demote
    idx=0
    while True:
        assert pri == heap[idx][0]
        left,right=2*idx+1,2*idx+2
        c_idx=None
        min_pri=pri
        if left<len(heap) and heap[left][0]<min_pri:
            c_idx = left
            min_pri = heap[left][0]
        if right<len(heap) and heap[right][0]<min_pri:
            c_idx = right
            min_pri = heap[right][0]
        if c_idx is None:
            break

        c_item  = heap[c_idx][1]
        heap[idx],heap[c_idx]=heap[c_idx],heap[idx]
        pos[item],pos[c_item]=pos[c_item],pos[item]
        idx = c_idx
    #assert is_pqueue(pq)
    return result


def nextpart1(M,pos,R,C):
    i,j,d = pos
    dests=[]
    for ndir in TURNS[d]:
        dr,dc = DIRS[ndir]
        nr=i
        nc=j
        dist=0
        for k in range(1,4):
            nr+=dr
            nc+=dc
            if nr<0 or nc<0 or nr>=R or nc>=C:
                break
            dist+=M[nr][nc]
            dests.append(((nr,nc,ndir),dist))
    return dests[::-1]

def nextpart2(M,pos,R,C):
    i,j,d = pos
    dests=[]
    for ndir in TURNS[d]:
        dr,dc = DIRS[ndir]
        nr=i
        nc=j
        dist=0
        for k in range(1,11):
            nr+=dr
            nc+=dc
            if nr<0 or nc<0 or nr>=R or nc>=C:
                break
            dist+=M[nr][nc]
            if k>=4:
                dests.append(((nr,nc,ndir),dist))
    return dests



def printm(M):
    for l in M:
        print("".join(str(c) for c in l))
    print()

def readdata(data=None):
    """Read and parse the input data"""
    if data is None:
       with open("input17.txt") as f:
            data = f.read()
    M=[]
    for line in data.splitlines():
        M.append([int(x) for x in line])
    return M


def dijkstra(M,nextf):
    R,C=len(M),len(M[0])
    start=(0,0,"")
    pred={start:(start,0)}
    cost={}
    PQ=pqueue_make()
    pqueue_promote(PQ,0,start)
    while len(PQ[0])>0:
        value,cur = pqueue_pop(PQ)
        cost[cur]= value
        if cur[0:2]==(R-1,C-1):
            break
        neigs=nextf(M,cur,R,C)
        for npos,dist in neigs:
            if npos in cost:
                continue
            value=cost[cur]+dist
            if npos not in pred or value<pqueue_priority(PQ,npos):
                pqueue_promote(PQ,value,npos)
                pred[npos]=cur
    return cost[cur]

def part1(data=None):
    """solve part 1"""
    M=readdata(data)
    print(dijkstra(M,nextpart1))


def part2(data=None):
    """solve part 1"""
    M=readdata(data)
    print(dijkstra(M,nextpart2))

if __name__ == "__main__":
    part1(EXAMPLE)
    part1()
    part2(EXAMPLE)
    part2(EXAMPLE2)
    part2()
