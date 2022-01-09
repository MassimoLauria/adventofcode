"""AOC 2021 day 17"""

import math
from collections import defaultdict

example = {"x": (20, 30), "y": (-10, -5)}

challenge = {"x": (281, 311), "y": (-74, -54)}

another = {'x': (352, 377), 'y': (-49, -30)}


def shoot(vx, vy, target):
    p = [(0, 0)]
    left, right = min(target['x']), max(target['x'])
    bottom, top = min(target['y']), max(target['y'])

    while True:
        x, y = p[-1]
        nx, ny = x + vx, y + vy
        vx = max(0, vx - 1)
        vy = vy - 1
        p.append((nx, ny))
        if left <= nx <= right and bottom <= ny <= top:
            return (True, p)
        if nx > right or ny < bottom:
            return (False, p)
    return p


def firsttriangular(N):
    n = math.floor((math.sqrt(1 + 8 * N) - 1) / 2)
    while n * (n + 1) < 2 * N:
        n += 1
    return n


def goody(v, bottom, top):
    assert 0 > top >= bottom
    hits = []
    p = 0
    cv = v
    t = 0
    if v > 0:
        t = 2 * v + 1
        cv = -v - 1
    while True:
        if bottom <= p <= top:
            hits.append(t)
        p += cv
        t += 1
        cv -= 1
        if p < bottom:
            break
    return hits


def goodx(v, left, right):
    assert 0 < left <= right
    if v <= 0:
        return []
    hits = []
    p = 0
    cv = v
    t = 0
    while True:
        if left <= p <= right:
            hits.append(t)
        p += cv
        cv -= 1
        t += 1
        if cv < 0:
            break
    if left <= p <= right:
        hits.append((t, "inf"))

    return hits


def score(vx, vy, target):
    box = target['x'] + target['y']
    top = max(target['y'])
    bottom = min(target['y'])

    assert top < 0
    assert vy > 0

    topy = vy * (vy + 1) // 2
    asc_steps = vy + 1

    speeddown = firsttriangular(-box[3] + topy)
    vhit = topy - speeddown * (speeddown + 1) // 2
    vhits = []
    while vhit >= bottom:
        # two steps at velocity 0
        vhits.append((asc_steps + speeddown, vhit))
        speeddown += 1
        vhit -= speeddown
    if len(vhits) == 0:
        return topy, []
    hits = []
    for i in range(len(vhits)):
        s, y = vhits[i]
        #print(f"process {vhits[i]}")
        s = min(s, vx)
        x = vx * s + s - s * (s + 1) // 2
        #print(f"process {s,x}")
        if x < box[0]:
            continue
        if x > box[1]:
            break
        hits.append((x, y))
    return topy, hits


def part1(data):
    """ Assumptions:
        shooting y>0 is always better
        shooting x<0 is always useless
        trench is below 0 vertically
        trench is above 0 horizontally
    """
    topy = 0, -1, -1
    for x in range(1, 100):
        for y in range(1, 100):
            r = score(x, y, data)
            if len(r[1]) > 0 and topy[0] < r[0]:
                topy = r[0], x, y
    print(topy[0])


def part2(data):

    bottom, top = min(data['y']), max(data['y'])
    left, right = min(data['x']), max(data['x'])

    assert bottom <= top < 0
    assert 0 < left <= right

    rangex = range(firsttriangular(left), right + 1)
    rangey = range(bottom, -bottom + 1)
    hitsx = defaultdict(lambda: [])
    hitsy = defaultdict(lambda: [])

    for v in rangey:
        for s in goody(v, bottom, top):
            hitsy[s].append(v)

    for v in rangex:
        for s in goodx(v, left, right):
            hitsx[s].append(v)

    # Expand infinities
    maxstep = max(hitsy.keys())
    toexpand = [k for k in hitsx if type(k) != int]
    for k in toexpand:
        for i in range(k[0], maxstep + 1):
            hitsx[i].extend(hitsx[k])
        hitsx.pop(k)
    output = []
    for s in hitsy:
        if s not in hitsx:
            continue
        output.extend([(vx, vy) for vx in hitsx[s] for vy in hitsy[s]])
    print(len(set(output)))


if __name__ == "__main__":
    part1(example)
    part1(challenge)
    part2(example)
    part2(challenge)
    part2(another)
