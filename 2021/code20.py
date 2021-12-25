import numpy as np
from itertools import product
import matplotlib.pyplot as plt

bitarray=np.array([[8,7,6],[5,4,3],[2,1,0]],dtype='int')
    
def readdata(data=None):
    if data is None:
        with open("input20.txt") as f:
            data=f.read()

    convert ={'#':1, '.':0 }
    pattern=None
    image=[]
 
    for line in data.splitlines():
        if len(line) ==0:
            continue
        if pattern is None:
            assert len(line)==512
            pattern = [ convert[c] for c in line]
        else:
            image.append([ convert[c] for c in line])
    
    M=np.array(image,dtype="int")

    def iterationf(x):
        return pattern[x]
    iterationf = np.vectorize(iterationf)
    
    return M,iterationf

example="""
..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..###..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#..#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#......#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.....####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.......##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

#..#.
#....
##..#
..#..
..###
"""
# Step
def nextstep(Src,Dest,f):
    assert Src.shape == Dest.shape

    Dest.fill(0)
    inf=Src[0,0]
    
    s=[slice(None,-1),slice(None,None),slice(1,None)]
    c=[0,None,-1]
    
    for i,j in product(range(3),range(3)):
        Dest[s[2-i],s[2-j]] |= Src[s[i],s[j]] << bitarray[i,j]
        if c[i] is not None:
            Dest[c[i],:] |= inf << bitarray[i,j]
        if c[j] is not None:
            Dest[:,c[j]] |= inf << bitarray[i,j]
    
    Dest[:] = f(Dest)
    
def enhances(steps,data=None,speed=None):
    
    animate = speed is not None and speed>0
        
    
    M,f_iter = readdata(data)

    r,c = M.shape
    R=r+2*steps+1
    C=c+2*steps+1
    offr=(R-r) // 2
    offc=(C-c) // 2
    
    Src=np.zeros((R,C),dtype="int")
    Src[offr:offr+r,offc:offc+c] = M
    Dest=np.zeros_like(Src)

    if animate:
        im=plt.imshow(Src)
        plt.ion()
        
    for _ in range(steps):
        nextstep(Src,Dest,f_iter)
        Src,Dest=Dest,Src
        
        if animate:
            im.set_data(Src)
            plt.pause(speed)
    
    if animate:
        plt.ioff()
        plt.show()
    return Src

Sierpisńki="""
..#.....#.......................#...............................#...............................................................#...............................................................................................................................#...............................................................................................................................................................................................................................................................

...
.#.
...
"""

tablecloth="""
..#.....#.......................#...............................................................................................#...............................................................................................................................................................................................................................................................................................................................................................................................

...
.#.
...
"""

if __name__ == "__main__":
    # Part 1
    Img=enhances(2,example)
    print(np.sum(Img))
    Img=enhances(2)
    print(np.sum(Img))
    # Part 2
    Img=enhances(50,example)
    print(np.sum(Img))
    Img=enhances(50)
    print(np.sum(Img))
    # Part 3
    # enhances(63,Sierpisńki,speed=0.05)
    # enhances(63,tablecloth,speed=0.05)

