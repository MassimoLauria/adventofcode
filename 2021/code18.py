from itertools import permutations
from heapq import heapify, heappop, heappush
import json

example1="""
[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]
[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]
[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]
[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]
[7,[5,[[3,8],[1,4]]]]
[[2,[2,2]],[8,[8,1]]]
[2,9]
[1,[[[9,3],9],[[9,0],[0,7]]]]
[[[5,[7,4]],7],1]
[[[[4,2],2],6],[8,7]]
"""

example2="""
[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]
"""

def parsedata(data=None):
    if data is None:
        with open("input18.txt") as f:
            data = f.read()
    for l in data.splitlines():
        if len(l)==0:
            continue
        yield json.loads(l)


def lastturn(expr,path):
    """maybe path is a sequence of L and R
    
    compute list o pair (l,c) where l is a list reference
    and c is either L or R
    
    Useful to go upward.
    """
    assert len(path)>0
    curr=expr
    for i in range(len(path)-1):
        curr=curr[0 if path[i]=='L' else 1]
    return curr,0 if path[-1]=='L' else 1


def closestnumber(expr,path,direction):
    bit = "LR".index(direction)
    otherdirection="LR"[1-bit]
    
    i=len(path)-1
    while i>=0 and path[i]==direction:
        i -= 1
    if i<0:
        return ""
    new=list(path[:i])
    new.append(direction)
    curr,_ = lastturn(expr,new)
    curr=curr[bit]
    while type(curr)==list:
        new.append(otherdirection)
        curr=curr[1-bit]
    return "".join(new)


def explode(expr,path):
    l,p = lastturn(expr,path)
    x,y = l[p]
    if type(x)!=int or type(y)!=int:
        raise ValueError("Path does not lead to a pair of integers")
    
    left=closestnumber(expr,path,"L")
    right=closestnumber(expr,path,"R")
    
    l[p]=0
    
    if len(right)>0:
        l,p=lastturn(expr,right)
        l[p] += y

    if len(left)>0:
        l,p=lastturn(expr,left)
        l[p] += x
        if l[p]>=10:
            return left


def split(expr,path):
    l,p=lastturn(expr,path)
    value=l[p]
    assert type(value)==int and value > 9
    x = value//2
    y = value-x
    l[p] = [x,y]

def magnitude(expr):
    if type(expr)==int:
        return expr
    return 3*magnitude(expr[0])+2*magnitude(expr[1])


def finddepth4(expr,bucket,path=""):
    
    if type(expr)==int:
        return

    if len(path)==4:
        bucket.append(path)
        return
    
    finddepth4(expr[0],bucket,path+"L")
    finddepth4(expr[1],bucket,path+"R")
    

def findsplits(expr,bucket,path=""):
    if type(expr)==int:
        if expr>=10:
            bucket.append(path)
        return
    
    findsplits(expr[0],bucket,path+"L")
    findsplits(expr[1],bucket,path+"R")
   
def findfirstsplit(expr):
    if type(expr)==int:
        if expr>=10:
            return ""
        else:
            return None
    
    x = findfirstsplit(expr[0])
    if x is not None:
        return "L"+x
    x = findfirstsplit(expr[1])
    if x is not None:
        return "R"+x
    return None

def repr_path(path):
    x=[]
    for l,p in path:
        x.append("L" if p==0 else "R")
    return "".join(x)

def addition(e1,e2):
    # assumption e1,e2 are reduced
    X=[e1,e2]
    
    # find initial set of nodes to explode
    exploding = [] 
    finddepth4(X,exploding)
    #print(exploding)
    for path in exploding:
        explode(X,path)
 
    p = findfirstsplit(X)
    while p is not None:
        split(X,p)
        
        maybe=None
        if len(p)>=4:
            maybe=explode(X,p)

        p = maybe
        if p is None:
            p = findfirstsplit(X)
        
    return X
    

def addition_list(exprs):
    if len(exprs)==0:
        return None
    acc = exprs[0]
    #print(acc)
    for i in range(1,len(exprs)):
        #print("+ ",exprs[i])
        acc = addition(acc,exprs[i])
        #print("= ",acc)
    return acc        
    


def test_explode():
    X = [[[[[9,8],1],2],3],4]
    explode(X,"LLLL")
    assert X == [[[[0,9],2],3],4]
    X = [7,[6,[5,[4,[3,2]]]]]
    explode(X,"RRRR")
    assert X == [7,[6,[5,[7,0]]]]
    X = [[6,[5,[4,[3,2]]]],1]
    explode(X,"LRRR")
    assert X == [[6,[5,[7,0]]],3]
    X = [[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]
    explode(X,"LRRR")   
    assert X == [[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]
    X = [[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]
    explode(X,"RRRR")
    assert X == [[3,[2,[8,0]]],[9,[5,[7,0]]]]

def test_demo():
    X = [[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]
    explode(X,"LLLL")
    assert X == [[[[0,7],4],[7,[[8,4],9]]],[1,1]]
    explode(X,"LRRL")
    assert X == [[[[0,7],4],[15,[0,13]]],[1,1]]
    split(X,"LRL")
    assert X == [[[[0,7],4],[[7,8],[0,13]]],[1,1]]
    split(X,"LRRR")
    assert X == [[[[0,7],4],[[7,8],[0,[6,7]]]],[1,1]]
    explode(X,"LRRR")
    assert X == [[[[0,7],4],[[7,8],[6,0]]],[8,1]]
    
def test_sum():
    A = [[[[4,3],4],4],[7,[[8,4],9]]]
    B = [1,1]
    X = addition(A,B)
    assert X == [[[[0,7],4],[[7,8],[6,0]]],[8,1]]
   
def test_addition_list():
    X = addition_list([[1,1],[2,2],[3,3],[4,4]])
    assert X == [[[[1,1],[2,2]],[3,3]],[4,4]]
    X = addition_list([[1,1],[2,2],[3,3],[4,4],[5,5]])
    assert X == [[[[3,0],[5,3]],[4,4]],[5,5]]
    X = addition_list([[1,1],[2,2],[3,3],[4,4],[5,5],[6,6]])
    assert X == [[[[5,0],[7,4]],[5,5]],[6,6]]
    
def part1(data=None):
    X=addition_list([p for p in parsedata(data)])
    print(magnitude(X))


def deepcopy(a):
    if type(a)==int:
        return a
    return [deepcopy(a[0]),deepcopy(a[1])]

def part2(data=None):
    List = [p for p in parsedata(data)]
    best=-1
    for a,b in permutations(List,2):
        a = deepcopy(a)
        b = deepcopy(b)
        value = magnitude(addition(a[:],b[:]))
        best = max(value,best)
    print(best)
    
    


if __name__ == "__main__":
    test_explode()
    test_demo()
    test_sum()
    test_addition_list()
    part1(example1) # 3488
    part1(example2) # 4140
    part1() # 4207
    part2(example2) # 3993
    part2() 
