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
        if output[i] == 127 and i!=0: print("<<<<<<<<",end="")
        print("  ",chr(output[i])," ")
        i-=1

def part1(duration,data=None):
    """solve part 1"""
    jets = readdata(data)
    #print(len(jets))
    #print(len(pieces))
    pit = bytearray([127])
    pos = 0    # piece position (from bottom)
    highest=0  # position of highest block
    j = 0

    for i in range(duration):
        piece = pieces[i % len(pieces)][:]
        pos   = highest + 4
        while True:

            jet = jets[j]
            j = (j + 1) % len(jets)

            if jet=='<':
                tmp = tryleft(piece)
            else:
                assert jet=='>'
                tmp = tryright(piece)

            if not collision(pit,tmp,pos):
                piece = tmp

            if not collision(pit,piece,pos-1):
                pos -= 1
            else:
                break
        place(pit,piece,pos)
        highest = max(highest,pos+len(piece)-1)

    # printchamber(chamber)
    print("part1:",highest)

if __name__ == "__main__":
    part1(2022,EXAMPLE)
    part1(2022)
    # part2()
