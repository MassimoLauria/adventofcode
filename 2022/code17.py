"""Advent of Code 2022 day 17
"""

EXAMPLE = ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"

pieces=[ # reverse
    [int('0011110',2)],  #  @@@@

    [int('0001000',2),   #   @
     int('0011100',2),   #  @@@
     int('0001000',2)],  #   @

    [int('0011100',2),   #  @@@
     int('0000100',2),   #    @
     int('0000100',2)],  #    @

    [int('0010000',2),   #  @
     int('0010000',2),   #  @
     int('0010000',2),   #  @
     int('0010000',2)],  #  @

    [int('0011000',2),   #  @@
     int('0011000',2)]   #  @@
]

def readdata(data=None):
    """Read and parse the input data"""
    if data is None:
       with open("input17.txt") as f:
            data = f.read()
    return [c for c in data if c in "<>"]

def tryright(piece):
    if any([b & 0x1 for b in piece]): return piece
    return [b>>1 for b in piece]

def tryleft(piece):
    if any([b & 0x40 for b in piece]): return piece
    return [b<<1 for b in piece]


def collision(G,piece,pos):
    rows = min(len(piece),len(G)-pos)
    return any(G[pos+i] & piece[i] for i in range(rows))

def place(G,piece,pos):
    G.extend([0]*(pos+len(piece)-len(G)))
    for i in range(len(piece)):
        G[pos+i] |= piece[i]


def printchamber(chamber,piece=None,pos=-1):
    output = chamber[:]
    if piece is not None and pos>=0:
        place(output,piece,pos)
    i = len(output)-1
    tr ={ ord('0') : ord(' '),
          ord('1') : ord('#') }
    while i>=0:
        x="{:07b}".format(output[i]).translate(tr)
        print('{}{}{}'.format(i%10,x,i%10),end="")
        print("  ",repr(chr(output[i]))," ",end="")
        if output[i] == 127 and i!=0: print("<<<<<<<<")
        print()
        i-=1

def height(pit):
    # Find tallest element
    h=len(pit)-1
    while pit[h] == 0x00:
        h -= 1
    return h

def next_state(p,j,pit,jets):
    """simulate a single step

    returns a pair (p,j,pit)
    p next piece
    j next jet
    pit status
    """
    assert 0<=p<len(pieces)
    assert 0<=j<len(jets)

    # Find tallest element
    pos   = height(pit) + 4
    pit   = bytearray(pit)
    piece = pieces[p][:]
    while True:

        tmp = tryleft(piece) if jets[j] =='<' else tryright(piece)
        j = ( j + 1 ) % len(jets)

        if not collision(pit,tmp,pos):
            piece = tmp
        if not collision(pit,piece,pos-1):
            pos -= 1
        else:
            break
    place(pit,piece,pos)
    return (p+1) % 5 , j, bytes(pit)

def solve_naive(data,duration):
    "Naive simulation"
    jets = readdata(data)
    pit = bytes([127])
    j = 0
    p = 0
    for _ in range(duration):
        p,j,pit = next_state(p,j,pit,jets)
    return height(pit)

def solve_cycle_detect(data,duration):
    "Simulation with cycle detection"
    jets = readdata(data)
    MEM = 10

    Confs  = set() # visited configurations
    T      = {}    # time of first visit
    H      = {}    # height at time of first visit

    p,j,pit = (0,0,bytes([127]))  # p   - piece to drop
                                  # j   - jet to consider
                                  # pit - state of game
    T[(p,j,pit)] = 0
    H[(p,j,pit)] = 0

    t = 1
    while True:
        assert t <= duration
        # state after t rocks
        p,j,pit          = next_state(p,j,pit,jets)

        # detect the cycle
        if (p,j,pit[-MEM:]) in Confs:
            break

        Confs.add((p,j,pit[-MEM:]))
        T[(p,j,pit[-MEM:])] = t
        H[(p,j,pit[-MEM:])] = height(pit)
        t += 1

    # manage the cycle
    cycled_state   = (p,j,pit[-MEM:])
    first_height   = H[cycled_state]
    second_height  = height(pit)
    first_time     = T[cycled_state]
    second_time    = t

    # residual loops, blocks and tail
    blocks = (duration - first_time) // (second_time-first_time)
    tail   = (duration - first_time) %  (second_time-first_time)
    for _ in range(tail):
        p,j,pit = next_state(p,j,pit,jets)
        assert (p,j,pit[-MEM:]) in Confs

    return height(pit) + (second_height-first_height)*(blocks-1)

def part1(data=None):
    print("part1:",solve_naive(data,2022))

def part2(data=None):
    n=1_000_000_000_000
    print("part2:",solve_cycle_detect(data,n))

if __name__ == "__main__":
    part1(EXAMPLE)
    part1()
    part2(EXAMPLE)
    part2()
