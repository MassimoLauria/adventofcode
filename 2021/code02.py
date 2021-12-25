example1="""
forward 5
down 5
forward 8
up 3
down 8
forward 2
"""

def scan1(data):
    cmds={
        "forward" : (+1,0),
        "up" : (0,-1),
        "down" : (0,+1),
        }
    h,d=0,0
    for l in data.splitlines():
        l = l.split()
        if len(l)!=2:
            continue
        cmd,value=l
        value=int(value)
        dh,dd = cmds[cmd]
        h += dh*value
        d += dd*value
    return h,d


def scan2(data):
    h,d=0,0
    aim=0
    for l in data.splitlines():
        l = l.split()
        if len(l)!=2:
            continue
        cmd,value=l
        value=int(value)
        if cmd=='down':
            aim += value
        elif cmd=='up':
            aim -= value
        elif cmd=='forward':
            h += value
            d += value*aim
    return h,d



def part1():
    with open("input02.txt") as f:
        h,d = scan1(f.read())
    print(h*d)

def part2():
    with open("input02.txt") as f:
        h,d = scan2(f.read())
    print(h*d)


if "__main__" == __name__:
    print(scan1(example1))
    print(scan2(example1))
    part1()
    part2()