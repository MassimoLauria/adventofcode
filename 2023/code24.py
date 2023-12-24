"""Advent of Code 2023 day 24
"""

EXAMPLE = """19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3
"""

def readdata(data=None):
    """Read and parse the input data"""
    if data is None:
       with open("input24.txt") as f:
            data = f.read()
    hail=[]
    for line in data.splitlines():
        line="".join([ (c if c.isdigit() or c in "+-" else " ") for c in list(line) ])
        hail.append([int(x) for x in line.split()])
    return hail

def solve(A,b):
    detA=A[0][0]*A[1][1]-A[0][1]*A[1][0]
    if detA==0:
        return None
    sol1=b[0]*A[1][1]-A[0][1]*b[1]
    sol2=A[0][0]*b[1]-b[0]*A[1][0]
    return (sol1/detA,sol2/detA)

def intersect1(h1,h2):
    p1x,p1y,_,v1x,v1y,_=h1
    p2x,p2y,_,v2x,v2y,_=h2
    A=[[v1x,-v2x],[v1y,-v2y]]
    b = [p2x-p1x,p2y-p1y]
    sol = solve(A,b)
    if sol is None:
        return None
    t1,t2 = sol
    if t1<=0 or t2<=0:
        return None
    return (p2x+v2x*t2,p2y+v2y*t2)


def part1(testarea,data=None):
    """solve part 1"""
    hails=readdata(data)
    N=len(hails)
    intersections=[]
    for i in range(0,N-1):
        for j in range(i+1,N):
            # print("{}, {}, {} @ {}, {}, {}".format(*hails[i]))
            # print("{}, {}, {} @ {}, {}, {}".format(*hails[j]))
            p = intersect1(hails[i],hails[j])
            if p is not None:
                intersections.append(p)
    counter=0
    for x,y in intersections:
        if testarea[0]<=x<=testarea[1] and testarea[0]<=y<=testarea[1]:
            counter+=1
    print(counter)


if __name__ == "__main__":
    part1([7,27],EXAMPLE)
    part1([200000000000000,400000000000000])
    # part2()
