"""Advent of Code 2022 day 19
"""

EXAMPLE = """
Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.

Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian.
"""

import re
from collections import deque
def readdata(data=None):
    """Read and parse the input data"""
    if data is None:
       with open("input19.txt") as f:
            data = f.read()

    BP = []
    for line in data.splitlines():
        if len(line)==0: continue
        nums = re.findall(r"\d+", line)
        nums = [int(x) for x in nums]
        BP.append(nums)
    return BP

rehit = 0

def solve_rec(bp,time,ore,clay,obs,geo,rore,rclay,robs,rgeo,Best):
    global rehit
    best = geo
    if time==0: return best

    if (ore,clay,obs,geo,rore,rclay,robs,rgeo) in Best:
        rehit += 1
        return Best[(ore,clay,obs,geo,rore,rclay,robs,rgeo)]

    if ore >=bp[5] and obs >= bp[6]:
        value = solve_rec(bp,time-1,
                          ore+rore-bp[5],clay+rclay,obs+robs-bp[6],geo+rgeo,
                          rore,rclay,robs,rgeo+1,Best)
        best = max(best,value)

    if ore >=bp[3] and clay >= bp[4]:
        value = solve_rec(bp,time-1,
                          ore+rore-bp[3],clay+rclay-bp[4],obs+robs,geo+rgeo,
                          rore,rclay,robs+1,rgeo,Best)
        best = max(best,value)


    if ore >=bp[2]:
        value = solve_rec(bp,time-1,
                          ore+rore-bp[2],clay+rclay,obs+robs,geo+rgeo,
                          rore,rclay+1,robs,rgeo,Best)
        best = max(best,value)


    if ore >= bp[1]:
        value = solve_rec(bp,time-1,
                          ore+rore-bp[1],clay+rclay,obs+robs,geo+rgeo,
                          rore+1,rclay,robs,rgeo,Best)

        best = max(best,value)

    value = solve_rec(bp,time-1,
                      ore+rore,clay+rclay,obs+robs,geo+rgeo,
                      rore,rclay,robs,rgeo,Best)
    best = max(best,value)

    Best[(ore,clay,obs,geo,rore,rclay,robs,rgeo)] = best
    return best

def part1(data=None):
    """solve part 1"""
    global rehit
    BP =  readdata(data)
    res  = 0
    time = 24
    for i in range(len(BP)):
        D={}
        rehit = 0
        x = solve_rec(BP[i],time,0,0,0,0,1,0,0,0,D)
        print("BP {} opens {} geodes".format(i+1,x))
        print("size",len(D))
        print("rehit",rehit)
        res += (i+1)*x
    print("part1:",res)


if __name__ == "__main__":
    part1(EXAMPLE)
    #part1()
    # part2()
