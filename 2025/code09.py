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
    
def part1(P):
    max=0; t=0
    for i in range(len(P)-1):
        for j in range(i+1,len(P)):
            t = (abs(P[i][0]-P[j][0])+1)*(abs(P[i][1]-P[j][1])+1)
            if t>max: max=t
    return max

def part2(P):
    X=[a for (a,b) in P]
    Y=[b for (a,b) in P]
    X.sort()
    Y.sort()
    Xrank={}
    Yrank={}
    for i,v in enumerate(X):
        Xrank[v]=i
    for i,v in enumerate(Y):
        Yrank[v]=i
    w, h = len(Xrank),len(Yrank)
    img = Image.new("RGB", (5*w, 5*h), "black")
    # create  rectangleimage
    draw = ImageDraw.Draw(img)
    for i in range(len(P)):
        s=P[i-1]
        e=P[i]
        rs = Xrank[s[0]],Yrank[s[1]]
        re = Xrank[e[0]],Yrank[e[1]]
        ps = 2*rs[0],2*rs[1]
        pe = 2*re[0],2*re[1]
        if abs(re[0]-rs[0])>100:
            print("Long line at step ",i)
            draw.line([ps,pe],fill='magenta')
        else:
            draw.line([ps,pe],fill='red')
        draw.ellipse((ps[0]-1,ps[1]-1,ps[0]+1,ps[1]+1),fill='white')
    # green point
    s = P[0]
    ps = 2*Xrank[s[0]],2*Yrank[s[1]]
    draw.ellipse((ps[0]-2,ps[1]-2,ps[0]+2,ps[1]+2),fill='green')
    img.show()
        
    
part2(readdata())
    
    


print("Part1 example:   ",part1(parse(example)))
print("Part1 challenge: ",part1(readdata()))

