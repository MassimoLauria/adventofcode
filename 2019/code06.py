def readdata():
    with open("input06.txt") as f:
        data=[l.strip().split(")") for l in f.readlines()]
    res={}
    for x,y in data:
        res.setdefault(x,[])
        res[x].append(y)
    return res

def countorbits(orbitaldata,root='COM'):
    "Returns (#objects,#indirect orbits)"
    if root in orbitaldata:
        children=orbitaldata[root]
    else:
        children=[] 
    objects=1
    indirect_orbits=0
    for child in children:
        o,i = countorbits(orbitaldata,child)
        objects += o
        indirect_orbits += i + o
    return objects,indirect_orbits

def orbitalparents(data):
    parent={}
    for p in data:
        for c in data[p]:
            parent[c]=p
    return parent

def smallest_transfer(data):
    parents=orbitalparents(data)
    san_address=[]
    you_address=[]
    pos='SAN'
    while pos!='COM':
        pos = parents[pos]
        san_address.append(pos)
    pos='YOU'
    while pos!='COM':
        pos = parents[pos]
        you_address.append(pos)
    san_address.reverse()
    you_address.reverse()
    i=0
    while san_address[i] == you_address[i]:
        i+=1
    return len(san_address)+len(you_address) -2*i
        
    

if __name__ == "__main__":
    data=readdata()
    print(countorbits(data,'COM')[1])  # part 1
    print(smallest_transfer(data))     # part 2