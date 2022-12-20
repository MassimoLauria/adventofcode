"""Advent of Code 2022 day 19
"""

EXAMPLE = """
Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.

Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian.
"""
import multiprocessing
import time
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

def solve_rec(bp,time,ore,clay,obs,geo,rore,rclay,robs,rgeo,
              Best,sofar):
    best = geo
    if time==0: return best

    if geo+rgeo*time+time*(time-1)//2 < sofar:
        return 0

    if (time,ore,clay,obs,geo,rore,rclay,robs,rgeo) in Best:
        return Best[(time,ore,clay,obs,geo,rore,rclay,robs,rgeo)]

    if ore >=bp[5] and obs >= bp[6]:
        value = solve_rec(bp,time-1,
                          ore+rore-bp[5],clay+rclay,obs+robs-bp[6],geo+rgeo,
                          rore,rclay,robs,rgeo+1,Best,sofar)
        best = max(best,value)
        sofar= max(best,sofar)

    if ore >=bp[3] and clay >= bp[4]:
        value = solve_rec(bp,time-1,
                          ore+rore-bp[3],clay+rclay-bp[4],obs+robs,geo+rgeo,
                          rore,rclay,robs+1,rgeo,Best,sofar)
        best = max(best,value)
        sofar= max(best,sofar)

    if ore >=bp[2]:
        value = solve_rec(bp,time-1,
                          ore+rore-bp[2],clay+rclay,obs+robs,geo+rgeo,
                          rore,rclay+1,robs,rgeo,Best,sofar)
        best = max(best,value)
        sofar= max(best,sofar)


    if ore >= bp[1]:
        value = solve_rec(bp,time-1,
                          ore+rore-bp[1],clay+rclay,obs+robs,geo+rgeo,
                          rore+1,rclay,robs,rgeo,Best,sofar)

        sofar= max(best,sofar)
        best = max(best,value)

    value = solve_rec(bp,time-1,
                      ore+rore,clay+rclay,obs+robs,geo+rgeo,
                      rore,rclay,robs,rgeo,Best,sofar)
    best = max(best,value)
    sofar= max(best,sofar)

    Best[(time,ore,clay,obs,geo,rore,rclay,robs,rgeo)] = best
    return best


def solve(data):
    bp,time = data
    D = {}
    return solve_rec(bp,time,0,0,0,0,1,0,0,0,D,0)

def part1(data=None):
    """solve part 1 (orrible solution using 12 processors)"""
    Time = 24
    BP =  readdata(data)
    pool = multiprocessing.Pool()
    pool = multiprocessing.Pool(processes=len(BP))
    outputs=pool.map(solve,[(bp,Time) for bp in BP])
    res = 0
    for i in range(len(BP)):
        print("BP {} opens {} geodes".format(i+1,outputs[i]))
        res += (i+1)*outputs[i]
    print("part1:",res)

def part2(data=None):
    """solve part 2"""
    Time = 32
    BP   =  readdata(data)
    pool = multiprocessing.Pool()
    pool = multiprocessing.Pool(processes=len(BP))
    if data!=EXAMPLE:
        BP=BP[:3]
    outputs=pool.map(solve,[(bp,Time) for bp in BP])
    res = 1
    for i in range(len(BP)):
        print("BP {} opens {} geodes".format(i+1,outputs[i]))
        res *= outputs[i]
    print("part2:",res)

if __name__ == "__main__":
    part1(EXAMPLE) # 33
    part1()      # 1177
    part2(EXAMPLE) # 3472
    part2()        # 62744
