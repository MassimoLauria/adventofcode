"""Advent of Code 2022 day 06
"""

EXAMPLE = [ "bvwbjplbgvbhsrlpgdmjqwftvncz",
            "nppdvjthqldpwncqszvftbrmjlhg",
            "nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg",
            "zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw" ]

def readdata(data=None):
    """Read and parse the input data"""
    if data is None:
       with open("input06.txt") as f:
            data = f.read()
    return data


def distinct_substring(data,L):
    """solve part 1"""
    i = L
    X = set(data[:L])
    while len(X)!=L and i < len(data):
        i += 1
        X = set( data[i-L:i] )
    print(i)

def part1(txt):
    distinct_substring(txt,4)

def part2(txt):
    distinct_substring(txt,14)

if __name__ == "__main__":
    intxt=readdata()
    for txt in EXAMPLE:
        part1(txt)
    part1(intxt)
    for txt in EXAMPLE:
        part2(txt)
    part2(intxt)
