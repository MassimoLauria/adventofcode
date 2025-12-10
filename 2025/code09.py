from PIL import Image, ImageDraw

example = """
7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3
"""

def parse(text):
    EX = [ s.split(',') for s in text.split() ]
    EX = [(int(a),int(b)) for (a,b) in EX]
    return EX

def readdata():
    with open("input09.txt",encoding="utf-8") as f:
        t=f.read()
    return parse(t)


def rectsize(p,q):
    return (abs(p[0]-q[0])+1)*(abs(p[1]-q[1])+1)

def part1(P):
    max=0; t=0
    for i in range(len(P)-1):
        for j in range(i+1,len(P)):
            t = rectsize(P[i],P[j])
            if t>max: max=t
    return max


def draw():
    P = readata()

    def line(i,j,color='red'):
        rs = P[i]
        re = P[j]
        ps = rs[0]//50,rs[1]//50
        pe = re[0]//50,re[1]//50
        draw.line([ps,pe],fill=color)

    def rect(i,j,color='blue'):
        rs = P[i]
        re = P[j]
        x0 = min(rs[0]//50,re[0]//50)
        x1 = max(rs[0]//50,re[0]//50)
        y0 = min(rs[1]//50,re[1]//50)
        y1 = max(rs[1]//50,re[1]//50)
        draw.rectangle([(x0,y0),(x1,y1)],fill=color)

    def point(i,color='white'):
        x,y = P[i][0]/50,P[i][1]/50
        draw.ellipse((x-1,y-1,x+1,y+1),fill=color)

    X=[a//50 for (a,b) in P]
    Y=[b//50 for (a,b) in P]
    w = max(X)+10
    h = max(Y)+10
    img = Image.new("RGB", (w, h), "black")
    # create  rectangleimage
    draw = ImageDraw.Draw(img)
    for i in range(len(P)):
        line(i-1,i)
        point(i)
    # green point
    point(0)
    img.show()

def part2(P):
    #drawranked(P)
    # 249 is the top    point in the wedge (lower y value)
    # 248 is the bottom point in the wedge (higher y value)
    N=len(P)
    maxvalue = 0
    if len(P)<250:
        seq=range(len(P))
    else:
        seq=[248,249]
    for i in seq:
        for j in range(len(P)):
            if j==i: continue
            size= rectsize(P[i],P[j])
            if size < maxvalue: continue
            invalid=False
            #print("Considering:",P[i],P[j])
            for k in range(len(P)):
                if k==i or k==j: continue
                if inside(P,i,j,k):
            #        print("-- invalidated by",P[k-1],P[k])
                    invalid = True
                    break
            if not invalid:
                maxpair=(i,j)
                maxvalue= size
    i,j=maxpair
    return maxvalue


def inside(P,i,j,k):
    c1=P[i]; c2=P[j]
    sl=P[k-1];el=P[k]
    lx=min(c1[0],c2[0])
    rx=max(c1[0],c2[0])
    ty=min(c1[1],c2[1])
    by=max(c1[1],c2[1])
    if (sl[0]<=lx and el[0]<=lx) or (sl[0]>=rx and el[0]>=rx):
        return False
    if (sl[1]<=ty and el[1]<=ty) or (sl[1]>=by and el[1]>=by):
        return False
    return True

print("Part1 example:   ",part1(parse(example)))
print("Part1 challenge: ",part1(readdata()))
print("Part2 example:   ",part2(parse(example)))
print("Part2 challenge: ",part2(readdata()))
#print("Part2 challenge: ",part2b(readdata()))
