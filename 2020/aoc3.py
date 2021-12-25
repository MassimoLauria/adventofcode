

def readinput():
    with open('aoc3input.txt') as f:
        data = f.readlines()
    return data

def count_trees_on_slop(sright,sdown,data):
    width = len(data[0])-1
    height = len(data)
    i = 0
    j = 0
    trees=0
    while i < height:
        if data[i][j]=='#':
            trees += 1
        i += sdown
        j = (j + sright) % width
    return trees


def part1():
    data=readinput()
    print(count_trees_on_slop(3,1,data))

def part2():
    data=readinput()
    slopes = [(1,1), (3,1), (5,1), (7,1), (1,2)]
    res = 1
    for right,down in slopes:
        res *= count_trees_on_slop(right,down,data)
    print(res)

part1()
part2()