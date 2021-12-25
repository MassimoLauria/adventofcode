import numpy as np
from itertools import product
import matplotlib.pyplot as plt


palette = np.array([[255,   0,   0],   # red
                    [  0, 255,   0],   # green
                    [255, 255, 255]])  # white
example="""
v...>>.vv>
.vv>>.vv..
>>.>v>...v
>>v>>.>.v.
v>v.vv.v..
>.>>..v...
.vv..>.>v.
v.v..>>v.v
....v..v.>
"""

def readdata(data=None):
    if data is None:
        with open("input25.txt") as f:
            data=f.read()
    convert={".":0, ">":1, "v":2}
    SC={}
    i=0
    R=-1
    C=-1
    for line in data.splitlines():
        if len(line)==0:
            continue
        for j,c in enumerate(line):
            if c==">":
                SC[(i,j)]=">"
            elif c=="v":
                SC[(i,j)]="v"
        C=max(C,len(line))
        i+=1
    R=i
    return SC,R,C

def printdata(SC,R,C):
    M=[["."]*C for _ in range(R)]
    for i,j in SC:
        M[i][j] = SC[i,j]
    for m in M:
        print("".join(m))
    print()

def showdata(SC,R,C):
    palette  =np.array([
            [255,  0,  0],  # red
            [  0,255,  0],  # green
            [255,255,255]]) # white
    M=np.zeros((R,C),dtype="int8")
    convert={">": 1, "v":2}
    for i,j in SC:
        M[i,j] = convert[SC[i,j]]
    return palette[M]

def nextstep(SC,R,C):
    mods1=[]
    for i,j in SC:
        if SC[i,j]=="v":
            continue
        assert SC[i,j]==">"
        if (i,(j+1) % C) not in SC:
           mods1.append((i,j))
    for i,j in mods1:
        SC[i,(j+1) % C]=">"
        SC.pop((i,j))
    mods2=[]
    for i,j in SC:
        if SC[i,j]==">":
            continue
        assert SC[i,j]=="v"
        if ((i+1) % R,j) not in SC:
           mods2.append((i,j))
    for i,j in mods2:
        SC[(i+1) % R,j]="v"
        SC.pop((i,j))
    if len(mods1)+len(mods2)==0:
        return False
    return True


def part1(data=None,animate=False):
    M,r,c=readdata(data)
    i=0
    L=len(M)
    if animate:
        img=plt.imshow(showdata(M,r,c))
        plt.ion()
    while True:
        f=nextstep(M,r,c)
        i+=1
        if not f:
            break
        if animate:
            img.set_data(showdata(M,r,c))
            plt.pause(0.03)
    if animate:
        plt.ioff()
        plt.show()
    print(i)

if __name__ == "__main__":
    part1(example)
    part1()
