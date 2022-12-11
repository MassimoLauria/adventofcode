"""Advent of Code 2022 day 11
"""

import re


EXAMPLE = """
Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1
"""

def readdata(data=None):
    """Read and parse the input data"""
    if data is None:
       with open("input11.txt") as f:
            data = f.read()
    return data

def parsedata(text):
    text=text.split()
    idx = 0
    Monkeys = []
    while True:
        try:
            idx = text.index("Monkey",idx)
        except ValueError:
            break
        idx =  text.index("items:",idx)
        idx2 = text.index("Operation:",idx)
        items = [text[i] for i in range(idx+1,idx2)]
        items[-1] = items[-1]+','
        items = [int(t[:-1]) for t in items]
        idx = idx2
        operation = (text[idx+4],text[idx+5])
        div = int(text[idx+9])
        gotrue = int(text[idx+15])
        gofalse = int(text[idx+21])
        D = { "items":items,
              "op": operation,
              "div": div,
              "go" : (gofalse,gotrue),
              "score": 0
        }
        Monkeys.append(D)
    return Monkeys

def op(x,c,d):
    if d=='old':
        d=x
    if c=='+':
        return x+int(d)
    elif c=="*":
        return x*int(d)

def part1(data=None):
    """solve part 1"""
    M = parsedata(readdata(data))
    # print("------ Initial -------")
    # for i in range(len(M)):
    #     print("Monkey",i,":",M[i]['items'])
    for round in range(1,21):
        for i in range(len(M)):
            m = M[i]
            for item in m['items']:
                wl = item
                wl = op(wl,*m['op']) // 3
                F,T = m['go']
                if wl % m['div']==0:
                    M[T]['items'].append(wl)
                else:
                    M[F]['items'].append(wl)
            m['score'] += len(m['items'])
            m['items'] = [] # no monkey keep an object
        # print("------ Round {:02} ------".format(round))
        # for i in range(len(M)):
        #    print("Monkey",i,":",M[i]['items'])
    #for i in range(len(M)):
    #    print("Monkey",i,":",M[i]['score'])
    X = sorted(m['score'] for m in M)
    print("part1: ", X[-2]*X[-1])

def part2(data=None):
    """solve part 2"""
    M = parsedata(readdata(data))
    MOD = 1
    for m in M:
        MOD *= m['div']
    for round in range(1,10001):
        for i in range(len(M)):
            m = M[i]
            for item in m['items']:
                wl = item
                wl = op(wl,*m['op']) % MOD
                F,T = m['go']
                if wl % m['div']==0:
                    M[T]['items'].append(wl)
                else:
                    M[F]['items'].append(wl)
            m['score'] += len(m['items'])
            m['items'] = [] # no monkey keep an object
    X = sorted(m['score'] for m in M)
    print("part2: ", X[-2]*X[-1])

if __name__ == "__main__":
    part1(EXAMPLE)
    part1()
    part2(EXAMPLE)
    part2()
