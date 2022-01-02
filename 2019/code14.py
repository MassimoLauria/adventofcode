"""Advent of Code 2019 day 14
"""
from collections import defaultdict

EXAMPLE2 = """
157 ORE => 5 NZVS
165 ORE => 6 DCFZ
44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL
12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ
179 ORE => 7 PSHF
177 ORE => 5 HKGWZ
7 DCFZ, 7 PSHF => 2 XJWVT
165 ORE => 2 GPVTF
3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT
"""

EXAMPLE1 = """
9 ORE => 2 A
8 ORE => 3 B
7 ORE => 5 C
3 A, 4 B => 1 AB
5 B, 7 C => 1 BC
4 C, 1 A => 1 CA
2 AB, 3 BC, 4 CA => 1 FUEL
"""

EXAMPLE3 = """
2 VPVL, 7 FWMGM, 2 CXFTF, 11 MNCFX => 1 STKFG
17 NVRVD, 3 JNWZP => 8 VPVL
53 STKFG, 6 MNCFX, 46 VJHF, 81 HVMC, 68 CXFTF, 25 GNMV => 1 FUEL
22 VJHF, 37 MNCFX => 5 FWMGM
139 ORE => 4 NVRVD
144 ORE => 7 JNWZP
5 MNCFX, 7 RFSQX, 2 FWMGM, 2 VPVL, 19 CXFTF => 3 HVMC
5 VJHF, 7 MNCFX, 9 VPVL, 37 CXFTF => 6 GNMV
145 ORE => 6 MNCFX
1 NVRVD => 8 CXFTF
1 VJHF, 6 MNCFX => 4 RFSQX
176 ORE => 6 VJHF
"""

EXAMPLE4 = """
171 ORE => 8 CNZTR
7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL
114 ORE => 4 BHXH
14 VRPVC => 6 BMBT
6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL
6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT
15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW
13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW
5 BMBT => 4 WPTQ
189 ORE => 9 KTJDG
1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP
12 VRPVC, 27 CNZTR => 2 XDBXC
15 KTJDG, 12 BHXH => 5 XCVML
3 BHXH, 2 VRPVC => 7 MZWV
121 ORE => 7 VRPVC
7 XCVML => 6 RJRHP
5 BHXH, 4 VRPVC => 5 LTCX
"""


def process(data):
    """Produces three dict

    value = how many are produced by the reaction
    deps  = which materials are needed
    reqs  = in which material this is a requirement
    """
    value = {}
    deps = defaultdict(lambda: [])
    reqs = defaultdict(lambda: [])

    for target in data:
        if target in value:
            raise ValueError
        v = data[target][0]
        value[target] = v
        for i in range(1, len(data[target])):
            nc, nr = data[target][i]
            deps[target].append((nc, nr))
            reqs[nr].append(target)
    return value, deps, reqs


def readdata(data=None):
    """Read and parse the input data"""
    if data is None:
        with open("input14.txt") as f:
            data = f.read()
    DEPS = {}
    for line in data.splitlines():
        if "=>" not in line:
            continue
        left, right = line.split('=>')
        value, target = right.split()
        DEPS[target] = [int(value)]
        for req in left.split(','):
            nreq, treq = req.split()
            DEPS[target].append((int(nreq), treq))
    return DEPS


def solvefor(value, deps, reqs, needed=1):
    """solve for how much fuel"""
    queue = ["FUEL"]
    need = defaultdict(lambda: 0)
    need["FUEL"] = needed
    reqs = {k: reqs[k].copy() for k in reqs}
    while len(queue) > 0:
        tgt = queue.pop(0)
        mult = (need[tgt] - 1) // value[tgt] + 1
        for nc, nr in deps[tgt]:
            need[nr] += nc * mult
            reqs[nr].remove(tgt)
            if len(reqs[nr]) == 0 and nr != "ORE":
                queue.append(nr)
    return need["ORE"]


def part1(data=None):
    """solve part 1"""
    data = readdata(data)
    value, deps, reqs = process(data)
    res = solvefor(value, deps, reqs, 1)
    print(res)


def part2(data=None):
    """solve part 2"""
    data = readdata(data)
    value, deps, reqs = process(data)

    totalore = 1000000000000
    # find top and botton
    bottom = -1
    top = 0
    res = 0
    while res < totalore:
        bottom = top
        top = top * 2 + 1
        res = solvefor(value, deps, reqs, top)
    while bottom < top - 1:
        mid = (top + bottom) // 2
        res = solvefor(value, deps, reqs, mid)
        if res < totalore:
            bottom = mid
        elif res > totalore:
            top = mid
        else:
            break
    print(bottom)


if __name__ == "__main__":
    # part1(EXAMPLE1)
    # part1(EXAMPLE2)
    # part1(EXAMPLE3)
    # part1(EXAMPLE4)
    part1()
    # part2(EXAMPLE2)
    # part2(EXAMPLE3)
    # part2(EXAMPLE4)
    part2()
