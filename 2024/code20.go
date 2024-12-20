// Advent of Code 2024 day 20
//
// Massimo Lauria

package main

import (
	"aoc2024/aoc"
	"fmt"
	"time"
)

const example = `
###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############
`

func canCheat(grid [][]byte, r, c, dr, dc int) bool {
	return grid[r+dr][c+dc] == '#' &&
		grid[r+2*dr][c+2*dc] != '#'
}

func main() {
	example := aoc.GridFromString(example)
	clock := time.Now()
	challenge, _ := aoc.GridFromFile("input20.txt")
	fmt.Printf("Load time                                     - %s\n", time.Since(clock))
	clock = time.Now()
	fmt.Printf("Part1 - example   : %-25d - %s\n", part1(example), time.Since(clock))
	clock = time.Now()
	fmt.Printf("Part1 - challenge : %-25d - %s\n", part1(challenge), time.Since(clock))
	clock = time.Now()
	fmt.Printf("Part2 - example   : %-25d - %s\n", part2(example), time.Since(clock))
	clock = time.Now()
	fmt.Printf("Part2 - challenge : %-25d - %s\n", part2(challenge), time.Since(clock))
}

const NoCheatYet = -1

type Conf struct {
	posr, posc     int
	cheatr, cheatc int
}

func Solve(grid [][]byte, start Conf, int cap) map[Conf]int {
	Q := aoc.NewMinHeap[Conf]()
	var cf Conf
	var dist int
	Q.Improve(start, 0)
	finalCost := make(map[Conf]int)
	// start exploration
	for Q.Len() > 0 {
		cf, dist = Q.Pop()
		finalCost[cf] = dist
		if grid[cf.posr][cf.posc] == 'E' {
			if cf.cheatr == NoCheatYet { // most expensive path
				return finalCost
			}
			continue
		}
		// next conf
		for _, dir := range aoc.FourWays {
			switch {
			case grid[cf.posr+dir[0]][cf.posc+dir[1]] != '#':
				newconf := Conf{
					posr:   cf.posr + dir[0],
					posc:   cf.posc + dir[1],
					cheatr: cf.cheatr,
					cheatc: cf.cheatc,
				}
				if _, ok := finalCost[newconf]; !ok {
					Q.Improve(newconf, dist+1)
				}
			case cf.cheatr != NoCheatYet: // cannot cheat again
			case grid[cf.posr+dir[0]][cf.posc+dir[1]] == '#' && // can cheat
				grid[cf.posr+2*dir[0]][cf.posc+2*dir[1]] != '#':
				newconf := Conf{
					posr:   cf.posr + 2*dir[0],
					posc:   cf.posc + 2*dir[1],
					cheatr: cf.posr,
					cheatc: cf.posc,
				}
				if _, ok := finalCost[newconf]; !ok {
					Q.Improve(newconf, dist+2)
				}
			}
		}
	}
	return finalCost
}

func part1(grid [][]byte) int {
	grid = aoc.AddBorderToGrid(grid, '#')
	var sr, sc int
FindStart:
	for sr = range grid {
		for sc = range grid[sr] {
			if grid[sr][sc] == 'S' {
				break FindStart
			}

		}
	}
	fmt.Println(sr, sc)
	start := Conf{posr: sr, posc: sc, cheatr: NoCheatYet, cheatc: NoCheatYet}
	exploration := Solve(grid, start)
	//fmt.Println(exploration)
	freq := make(map[int]int)
	for cf, dist := range exploration {
		if grid[cf.posr][cf.posc] == 'E' {
			freq[dist] += 1
		}
	}
	fmt.Println(freq)
	return len(grid)
}

func part2(grid [][]byte) int {
	return len(grid)
}
