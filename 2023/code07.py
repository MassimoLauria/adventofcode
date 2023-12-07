"""Advent of Code 2023 day 07
"""

from collections import defaultdict

EXAMPLE = """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
"""


def readdata(data=None):
    """Read and parse the input data"""
    hands=[]
    if data is None:
       with open("input07.txt") as f:
           data = f.read()
    for line in data.splitlines():
        line=line.split()
        hands.append([0,None,line[0],int(line[1])])
    return hands


RANKS={ (1,1,1,1,1): 1,  # no pairs
        (1,1,1,2)  : 2,  # one pair
        (1,2,2)    : 3,  # two paira
        (1,1,3)    : 4,  # triple
        (2,3)      : 5,  # full house
        (1,4)      : 6,  # poker
        (5,)       : 7   # five of a kind
       }

# Rearrange chars to make string sort according to strength
symb={'A':'F','K':'E','Q':'D','J':'C','T':'B',
      '9':'9','8':'8','7':'7','6':'6','5':'5','4':'4',
      '3':'3','2':'2'}

def normalize_value1(hand):
    d=defaultdict(lambda : 0)
    for c in hand[2]:
        d[c]+=1
    hand[1]="".join(symb[c] for c in hand[2])
    hand[0]=RANKS[tuple(sorted(d.values()))]

def normalize_value2(hand):
    d=defaultdict(lambda : 0)
    for c in hand[2]:
        d[c]+=1
    jokers=d['J']
    if jokers==5:
        values=(5,)
    else:
        d.pop('J')
        values=sorted(d.values())
        values[-1]+=jokers
    hand[1]="".join(symb[c] for c in hand[2])
    hand[0]=RANKS[tuple(values)]


def part1(data=None):
    """solve part 1"""
    hands=readdata(data)
    for h in hands:
        normalize_value1(h)
    hands.sort()
    acc=0
    for i in range(len(hands)):
        acc+=(i+1)*hands[i][3]
        #print(hands[i])
    print(acc)

def part2(data=None):
    """solve part 2"""
    hands=readdata(data)
    for h in hands:
        normalize_value2(h)
    hands.sort()
    acc=0
    for i in range(len(hands)):
        acc+=(i+1)*hands[i][3]
        #print(hands[i])
    print(acc)

if __name__ == "__main__":
    part1(EXAMPLE)
    part1()
    symb['J'] = '1'
    part2(EXAMPLE)
    part2()
