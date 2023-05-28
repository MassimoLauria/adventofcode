"""Advent of Code 2019 day 17
"""

from intcode import IntCode,IntCodeCPU

EXAMPLE="""#######...#####
#.....#...#...#
#.....#...#...#
......#...#...#
......#...###.#
......#.....#.#
^########...#.#
......#.#...#.#
......#########
........#...#..
....#########..
....#...#......
....#...#......
....#...#......
....#####......
"""

def readdata(data=None):
    """Read and parse the input data"""
    if data is None:
       with open("input17.txt") as f:
            data = f.read()
    return data

def make2d(D):
    newline = 10
    width = D.index(newline)
    M = [ D[i:i+width] for i in range(0,len(D),width+1) ]
    if len(M[-1])==0:
        M.pop()
    return M

def print_map(M):
    for l in M:
        print(bytes(l).decode('ascii'))
    print()

def get_intersection(M):
    diamond = [(0,-1),(0,+1),(-1,0),(+1,0)]
    empty = 46
    height = len(M)
    width  = len(M[0])
    intersections = []
    for i in range(1,height-1):
        for j in range(1,width-1):
            if M[i][j]==empty:
                continue
            isintersection = True
            for di,dj in diamond:
                isintersection = isintersection and (M[i][j] == M[i+di][j+dj])
            if isintersection:
                intersections.append((i,j))
    return intersections


def part1(data=None):
    """solve part 1"""
    code = readdata()
    if data is None:
        CPU = IntCodeCPU(code)
        CPU.run()
        scan_map = CPU.get_output()
        assert CPU.halted()
    else:
        scan_map = EXAMPLE.encode("ascii")
    scan_map = make2d(scan_map)


    #print_map(scan_map)

    intersections = get_intersection(scan_map)
    print(len(intersections))
    t = 0
    for i,j in intersections:
        t += i*j
    print(f"Part1: {t}")

def part2(data=None):
    """solve part 2"""
    code = readdata()
    assert code[0]=='1'
    code='2'+code[1:]
    CPU = IntCodeCPU(code)
    CPU.interactive()
    # while True:

    #     CPU.run()
    #     odata = CPU.get_output()
    #     if odata[-1]>255:
    #         res   = odata[-1]
    #         odata = odata[:-1]
    #         assert CPU.status=="HALT"

    #     print(bytes(odata).decode('ascii'))
    #     if CPU.status=="HALT": break

    #     CPU.flush_output()
    #     idata=input(CPU.status+" >")
    #     if len(idata)>20:
    #         print("Input must be at most 20 chars")
    #         break
    #     CPU.add_input(idata+'\n')

if __name__ == "__main__":
    #part1(EXAMPLE)
    #part1()
    part2()
