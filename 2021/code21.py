from itertools import product
from collections import Counter
import numpy as np

MEMORY={}
OUTCOMES=Counter([i+j+k for i,j,k  in product(range(1,4),repeat=3)])

def basicsimulation(pos1,pos2,winscore=1000):
    dice = 1
    players=[pos1,pos2]
    scores=[0,0]

    p=0  # which players does play?
    tot_rolls=0
    while True:
        rolls = dice, dice % 100 + 1 , (dice + 1) % 100 + 1
        dice  = (dice + 2) % 100 + 1
        tot_rolls += 3
        players[p] =  (players[p] + sum(rolls) - 1) % 10 + 1
        scores[p] += players[p]
        #print(f"Player {p+1} rolls {rolls}, and moves to {players[p]} with score {scores[p]}")
        if scores[p]>=winscore:
            break
        p = (p+1) % 2
    #print(f"Player {p+1} won, after {tot_rolls} rolls. Final number={tot_rolls}*{scores[1-p]}={tot_rolls*scores[1-p]}")
    print(tot_rolls*scores[1-p])


def Win1(pos1,pos2,winscore1,winscore2):
    if winscore1<=0:
        return (1,0)
    elif winscore2<=0:
        return (0,1)
    
    # We know the game position
    if (pos1,pos2,winscore1,winscore2) in MEMORY:
        return MEMORY[pos1,pos2,winscore1,winscore2]
    
    # New configuration:
    # player 1 throw three dice and for every outcome
    # we see how much the new configuration score
    #
    # the intended meaning is that player 1 is the one moving,
    # hence we reverse the roles
    #
    # observe that configurations comes with weights
    p1win=0
    p2win=0
    for roll,weight in OUTCOMES.items():
        newpos1= (pos1 + roll - 1) % 10 +1
        newwinscore1=winscore1-newpos1
        if newwinscore1<=0:
            w1,w2=1,0
        elif (pos2,newpos1,winscore2,newwinscore1) in MEMORY:
            w2,w1 = MEMORY[(pos2,newpos1,winscore2,newwinscore1)]
        else:
            w2,w1 = Win1(pos2,newpos1,winscore2,newwinscore1)
        p1win += weight*w1
        p2win += weight*w2
    MEMORY[pos1,pos2,winscore1,winscore2] = p1win,p2win
    return p1win,p2win

if __name__ == "__main__":
    # part 1 - example
    basicsimulation(4,8,1000)
    # part 1 - data
    basicsimulation(4,2,1000)
    # part 2 - example
    print(max(Win1(4,8,21,21)))    
    # part 2 - data
    print(max(Win1(4,2,21,21)))
    # part 3 - data
    #print("Data:", 4,8,100,100)
    #win1,win2=Win1(4,8,100,100)
    #print(f"W1: {win1}")
    #print(f"W2: {win2}")
    #print(f"W1/Total: {win1/(win1+win2)}")
    #print("Data:", 4,8,1000,1000)
    #win1,win2=Win1(4,8,1000,1000)
    #print(f"W1: {win1}")
    #print(f"W2: {win2}")
    #print(f"W1/Total: {win1/(win1+win2)}")
    
    



