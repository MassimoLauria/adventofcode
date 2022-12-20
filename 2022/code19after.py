"""Advent of Code 2022 day 19 (after some spoilers)
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

def old_solve_rec(bp,time,ore,clay,obs,geo,rore,rclay,robs,
              Best,sofar):
    best = geo
    if time==0: return best
    if time<0:  return 0

    if geo+time*(time-1)//2 < sofar:
        return 0

    if (time,ore,clay,obs,geo,rore,rclay,robs) in Best:
        return Best[(time,ore,clay,obs,geo,rore,rclay,robs)]


    if ore >=bp[5] and obs >= bp[6]:
        # NOTE: SPOILER 1 no need to create geode-opening robot. Just cash geodes
        value = solve_rec(bp,time-1,
                          ore+rore-bp[5],clay+rclay,obs+robs-bp[6],geo+time-1,
                          rore,rclay,robs,Best,sofar)
        best = max(best,value)
        sofar= max(best,sofar)

    if ore >=bp[3] and clay >= bp[4] and robs<bp[6]:
        # NOTE: SPOILER 2 wanna build robot? No need if we have enough
        # robot to refill any construction needed in one round
        # NOTE: SPOILER 2 wanna build obsidian-robot? No need if
        value = solve_rec(bp,time-1,
                          ore+rore-bp[3],clay+rclay-bp[4],obs+robs,geo,
                          rore,rclay,robs+1,Best,sofar)
        best = max(best,value)
        sofar= max(best,sofar)

    if ore >=bp[2] and rclay<bp[4]:
        # NOTE: SPOILER 2 wanna build robot? No need if we have enough
        # robot to refill any construction needed in one round
        value = solve_rec(bp,time-1,
                          ore+rore-bp[2],clay+rclay,obs+robs,geo,
                          rore,rclay+1,robs,Best,sofar)
        best = max(best,value)
        sofar= max(best,sofar)


    if ore >= bp[1] and rore<max(bp[1],bp[2],bp[3],bp[5]):
        # NOTE: SPOILER 2 wanna build ore-robot? No need if
        # we have enough robot to refill any construction needed in one round
        value = solve_rec(bp,time-1,
                          ore+rore-bp[1],clay+rclay,obs+robs,geo,
                          rore+1,rclay,robs,Best,sofar)

        sofar= max(best,sofar)
        best = max(best,value)

    value = solve_rec(bp,time-1,
                      ore+rore,clay+rclay,obs+robs,geo,
                      rore,rclay,robs,Best,sofar)
    best = max(best,value)
    sofar= max(best,sofar)

    Best[(time,ore,clay,obs,geo,rore,rclay,robs)] = best
    return best


def next_geo(bp,time,ore,clay,obs,geo,rore,rclay,robs):

    if time == 0: return geo
    if robs == 0: return geo

    while ore < bp[5] or obs < bp[6]:
        time -= 1
        ore += rore
        clay+= rclay
        obs += robs
        if time == 0:
            return geo
    # NOTE: SPOILER 1 no need to create geode-opening robot. Just cash geodes
    value = solve_rec(bp,time-1,
                      ore+rore-bp[5],clay+rclay,obs+robs-bp[6],geo+time-1,
                      rore,rclay,robs)
    return value

def next_obs(bp,time,ore,clay,obs,geo,rore,rclay,robs):

    if time  == 0: return geo
    if rclay == 0: return geo

    if obs+time*robs >= time*bp[6]:
        # no need to build more obsidian robots
        return geo

    while ore < bp[3] or clay < bp[4]:
        time -= 1
        ore += rore
        clay+= rclay
        obs += robs
        if time == 0:
            return geo
    value = solve_rec(bp,time-1,
                      ore+rore-bp[3],clay+rclay-bp[4],obs+robs,geo,
                      rore,rclay,robs+1)
    return value

def next_clay(bp,time,ore,clay,obs,geo,rore,rclay,robs):

    if time  == 0: return geo

    if clay + time * rclay>= time * bp[4]:
        # no need to build more clay robots
        return geo

    while ore < bp[2]:
        time -= 1
        ore += rore
        clay+= rclay
        obs += robs
        if time == 0:
            return geo
    value = solve_rec(bp,time-1,
                      ore+rore-bp[2],clay+rclay,obs+robs,geo,
                      rore,rclay+1,robs)
    return value

def next_ore(bp,time,ore,clay,obs,geo,rore,rclay,robs):

    if time  == 0: return geo

    if ore + time*rore >= time*max(bp[1],bp[2],bp[3],bp[5]):
        # no need to build more ore robots
        return geo

    while ore < bp[1]:
        time -= 1
        ore += rore
        clay+= rclay
        obs += robs
        if time == 0:
            return geo
    value = solve_rec(bp,time-1,
                      ore+rore-bp[1],clay+rclay,obs+robs,geo,
                      rore+1,rclay,robs)
    return value

D = {}

def solve_rec(bp,time,ore,clay,obs,geo,rore,rclay,robs):

    global D
    if (time,ore,clay,obs,geo,rore,rclay,robs) in D:
        return D[(time,ore,clay,obs,geo,rore,rclay,robs)]

    value = max([
        next_geo(bp,time,ore,clay,obs,geo,rore,rclay,robs),
        next_obs(bp,time,ore,clay,obs,geo,rore,rclay,robs),
        next_clay(bp,time,ore,clay,obs,geo,rore,rclay,robs),
        next_ore(bp,time,ore,clay,obs,geo,rore,rclay,robs)
    ])
    D[(time,ore,clay,obs,geo,rore,rclay,robs)] = value
    return value

def solve(data):
    bp,time = data
    return solve_rec(bp,time,0,0,0,0,1,0,0)

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
