from itertools import combinations
from pprint import pprint

testfield0="""
####
##..
#...
#...
"""

testfield1="""
......#.#.
#..#.#....
..#######.
.#.#.###..
.#..#.....
..#....#.#
#..#....#.
.##.#..###
##...#..#.
.#....####
"""

testfield2="""
#.#...#.#.
.###....#.
.#....#...
##.#.#.#.#
....#.#.#.
.##..###.#
..#...##..
..##....##
......#...
.####.###.
"""

testfield3="""
.#..#..###
####.###.#
....###.#.
..###.##.#
##.##.#.#.
....###..#
..#.#..#.#
#..#.#.###
.##...##.#
.....#.#..
"""

testfield4="""
.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##
"""

testfield5="""
.#....#####...#..
##...##.#####..##
##...#...#.#####.
..#.....X...###..
..#.#.....#....##
"""

def getpoints(data=None):
    
    if data is None:
        return getpoints(open("input10.txt"))
    
    if hasattr(data, "readlines"):
        data.seek(0)
        return getpoints(data.read())
    
    if not isinstance(data,str):
        raise ValueError("File or string or None are expected")
    
    lines=data.split('\n')
    lines=[l.strip() for l in lines]
    lines=[l for l in lines if len(l)>0]
    # load points
    points=[]
    R,C=len(lines),len(lines[0])
    for r in range(R):
        for c in range(C):
            if lines[r][c]=="#":
                points.append((c,r))
    return points
    


def gcd(a,b):
    a,b=abs(a),abs(b)
    a,b = min(a,b),max(a,b)
    while b>0:
        a , b = b, a % b
    return a
    

def orientedslope(x0,y0,x1,y1):
    """
    The oriented slope between points (x0,y0) and (x1,y1) is
    
    dx,dy
    
    where
    
    dx=(x1-x0), dy=(y1-y0)

    normalized so that dx,dy are coprimes
    """
    dx=x1-x0
    dy=y1-y0
    d = gcd(dx,dy)
    return (dx//d,dy//d)
    
        

def sights(observer, points):
    rays={}
    for p in points:
        if p==observer:
            continue
        r=orientedslope(*observer,*p)
        rays.setdefault(r,set())
        rays[r].add(p)
    
    return rays

def clockwiserank(line):
    """Assign a rank to lines, according to clockwise orientation
    
    - x axis is toward right
    - y axis is downward
    
    rank is made of two numbers. First depends on the orientation
    0 --> up
    1 --> up right, right, down right
    2 --> down
    3 --> down left, left, up left
    4 --> invalid
    
    second one depends on the angle and only applies to quadrant
    
    """
    x,y= line
    if y<0 and x==0: # up
        return (0,0)
    elif x>0: # right side of the y axis
        return (1,y/x)
    elif y>0 and x==0: # down
        return (2,0)
    elif x<0: # left side of the y axis
        return (3,y/x)
    else:
        return (4,0)

def part2(src=None,basepoint=None):
    points=getpoints(src)
    
    if basepoint is None:
        _,base = part1(src)
    else:
        base=basepoint
    
    # Get the lines of sight with direction
    rays = sights(base,points)
    
    # sort points on the lines of sight, last is closer so we can pop
    def minusdistancesquared(p):
        return -(p[0]-base[0])**2 - (p[1]-base[1])**2

    # sort the lines clockwise
    clock = list(rays.keys())
    clock.sort(key=clockwiserank)
    
    # targets (last in the list is closer)
    targets=[]
    totalcount=0
    for ray in clock:
        # sort points on the lines of sight, last is closer so we can pop
        asteroids=list(rays[ray]) 
        asteroids.sort(key=minusdistancesquared) 
        targets.append(asteroids)
        totalcount += len(asteroids)
    
    i=0
    shot=0
    outcome=None
    while shot<totalcount:
        if len(targets[i])>0:
            p=targets[i].pop()
            shot += 1
            if shot==200:
                outcome= p[0]*100+p[1]
        i += 1
        i %= len(targets)
    return outcome
    
    
def part1(src=None):
    points=getpoints(src)
    results=[]
    # Get results
    for o in points:
        rays = sights(o,points)
        results.append((len(rays),o))

    out=max(results)
    return out

if __name__ == "__main__":
    print("Part1:", part1()[0])
    print("Part2:", part2())
    
                


    