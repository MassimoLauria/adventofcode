"""Advent of Code 2019 - day 13

"""
from collections import defaultdict
from intcode import IntCode, IntCodeCPU


def readdata(data=None):
    if data is None:
        with open("input13.txt") as f:
            return f.read()


def part1():
    code = readdata()
    Tiles = defaultdict(lambda: 0)
    output = IntCode(code, [])
    assert len(output) % 3 == 0
    for i in range(0, len(output), 3):
        x = output[i]
        y = output[i+1]
        tid = output[i+2]
        oldid = Tiles[x, y]
        if oldid in (1, 3):
            continue
        Tiles[x, y] = tid
    print(len([(x, y) for x, y in Tiles if Tiles[x, y] == 2]))


def part2(gfx=False, autoplay=True):
    if not autoplay:
        gfx = True

    Tiles = defaultdict(lambda: 0)
    code = readdata()
    CPU = IntCodeCPU('2' + code[1:])
    score = 0
    paddlex = -1
    ballx = -1
    SCREENW = 42
    SCREENH = 23
    SCREEN = [[' ']*SCREENW for _ in range(SCREENH)]
    convert = {0: ' ', 1: '#', 2: '*', 3: '=', 4: '0'}
    while True:
        CPU.run()
        output = CPU.get_output()
        assert len(output) % 3 == 0
        for i in range(0, len(output), 3):
            x = output[i]
            y = output[i+1]
            tid = output[i+2]
            if x == -1 and y == 0:
                score = tid
                continue
            if tid == 4:
                ballx = x
            if tid == 3:
                paddlex = x
            Tiles[x, y] = tid

        if gfx:
            for x, y in Tiles:
                SCREEN[y][x] = convert[Tiles[x, y]]
            for line in SCREEN:
                print("".join(line))
            print("Score:", score)
        while i not in [-1, 0, 1]:
            if autoplay:
                i = ballx-paddlex
                if abs(i) > 0:
                    i /= abs(i)
            else:
                i = input("> ").strip()
                if i not in ['-1', '0', '1', '']:
                    print("Please repeat input in -1,0,1 or empty")
                if i == '':
                    i = '0'
                i = int(i)

        CPU.flush_output()
        CPU.add_input([int(i)])
        if not CPU.is_waiting():
            break
    print(score)


if __name__ == "__main__":
    part1()
    part2()
