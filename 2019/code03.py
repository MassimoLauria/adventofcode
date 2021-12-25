def parseline(line):
    d = line.split(",")
    return [ (cmd[0],int(cmd[1:])) for cmd in d]


t1=[parseline("R75,D30,R83,U83,L12,D49,R71,U7,L72"),
    parseline("U62,R66,U55,R34,D71,R55,D58,R83")]

t2=[parseline("R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51"),
    parseline("U98,R91,D20,R16,D67,R40,U7,R15,U6,R7")]

puzzleinput=[None,None]
with open("input03.txt") as f:
    puzzleinput[0]=f.readline().strip()
    puzzleinput[1]=f.readline().strip()
    puzzleinput[0]=parseline(puzzleinput[0])
    puzzleinput[1]=parseline(puzzleinput[1])
    
def segments(wire):
    r,c=0,0
    walked=0
    horizontal=[]
    vertical=[]
    for direction,length in wire:
        if direction=='R':
            horizontal.append((r,c,r,c-length,walked))
            c = c - length
        elif direction=='L':
            horizontal.append((r,c,r,c+length,walked))
            c = c + length
        elif direction=='D':
            vertical.append((r,c,r-length,c,walked))
            r = r - length
        elif direction=='U':
            vertical.append((r,c,r+length,c,walked))
            r = r + length
        walked+=length
        
    return horizontal,vertical
    
def intersections(hor,vert):
    res=[]
    for r,hstart,rr,hend,walked1 in hor:
        left,right=min(hstart,hend),max(hstart,hend)
        assert r==rr
        for vstart,c,vend,cc,walked2 in vert:
            down,up=min(vstart,vend),max(vstart,vend)
            assert c==cc
            if not left<=c<=right:
                continue
            if not down<=r<=up:
                continue
            if r==0 and c==0:
                continue
            
            steps=walked1+walked2+abs(c-hstart)+abs(r-vstart)
            res.append((r,c,steps))
    return res
                
            
    
def solve_part2(w1,w2):
    hor1,ver1=segments(w1)
    hor2,ver2=segments(w2)
    pi=intersections(hor1,ver2)
    pi.extend(intersections(hor2,ver1))
    return min(s for _,_,s in pi)
     
def solve_part1(w1,w2):
    hor1,ver1=segments(w1)
    hor2,ver2=segments(w2)
    pi=intersections(hor1,ver2)
    pi.extend(intersections(hor2,ver1))
    return min(abs(x)+abs(y) for x,y,_ in pi)
    

if __name__ == "__main__":
    print("--Part 1--")
    print("Solve example 1:",solve_part1(*t1))
    print("Solve example 2:",solve_part1(*t2))
    print("Solve input:",solve_part1(*puzzleinput))
    print("--Part 2--")
    print("Solve example 1:",solve_part2(*t1))
    print("Solve example 2:",solve_part2(*t2))
    print("Solve input:",solve_part2(*puzzleinput))
    
