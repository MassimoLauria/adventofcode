"""Advent of Code 2022 day 17
"""

EXAMPLE = ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"

pieces=[ # reverse
    [int('00111100',2)],  #  @@@@

    [int('00010000',2),   #   @
     int('00111000',2),   #  @@@
     int('00010000',2)],  #   @

    [int('00111000',2),   #  @@@
     int('00001000',2),   #    @
     int('00001000',2)],  #    @

    [int('00100000',2),   #  @
     int('00100000',2),   #  @
     int('00100000',2),   #  @
     int('00100000',2)],  #  @

    [int('00110000',2),   #  @@
     int('00110000',2)]   #  @@
]

def readdata(data=None):
    """Read and parse the input data"""
    if data is None:
       with open("input17.txt") as f:
            data = f.read()
    return data



def printchamber(chamber):
    i = len(chamber)-1
    output=[]
    tr ={ ord('0') : ord(' '),
          ord('1') : ord('#') }
    while i>=0:
        print("{:08b}".format(chamber[i]).translate(tr))
        i-=1


def part1(data=None):
    """solve part 1"""
    jets = readdata(data)
    print(jets)
    chamber = bytearray([255]+[1]*5)
    pid = 0
    jid = 0
    pos = 0 # piece position (from bottom)
    height=1
    for _ in range(6):
        # make room in the chamber
        ph = len(pieces[pid])
        pos  = height + 3
        ceil = height + 3 + ph
        if ceil>len(chamber):
            chamber.extend([1]*(ceil-len(chamber)))
        # piece enters
        for i in range(len(pieces[pid])):
            chamber[pos+i] |= pieces[pid][i]
            height = max(height,pos+ph)
        #
        pid = (pid + 1) % len(pieces)
    printchamber(chamber)

if __name__ == "__main__":
    part1(EXAMPLE)
    # part1()
    # part2()
