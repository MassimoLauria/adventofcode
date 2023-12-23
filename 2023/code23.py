"""Advent of Code 2023 day 23
"""

EXAMPLE = """#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#"""

def readdata(data=None):
    """Read and parse the input data"""
    if data is None:
       with open("input23.txt") as f:
            data = f.read()
    return [list(x) for x in data.splitlines()]


def part1(data=None):
    """solve part 1"""
    pass


if __name__ == "__main__":
    part1(EXAMPLE)
    # part1()
    # part2()
