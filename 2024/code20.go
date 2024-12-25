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

func main() {
	clock := time.Now()
	challenge, _ := aoc.GridFromFile("input20.txt")
	fmt.Printf("Load time                                     - %s\n", time.Since(clock))
	clock = time.Now()
	fmt.Printf("Part1 - challenge : %-25d - %s\n", part12(challenge, 2, 100), time.Since(clock))
	clock = time.Now()
	fmt.Printf("Part2 - challenge : %-25d - %s\n", part12(challenge, 20, 100), time.Since(clock))
}

func getUniquePath(grid [][]byte) [][2]int {
	var sr, sc, r, c, nr, nc int
	for r = range grid {
		for c = range grid[r] {
			if grid[r][c] == 'S' {
				sr, sc = r, c
			}
		}
	}
	path := make([][2]int, 1, len(grid)*len(grid[0]))
	path[0] = [2]int{sr, sc}
	for {
		r, c = path[len(path)-1][0], path[len(path)-1][1]
		if grid[r][c] == 'E' {
			return path
		}
		for _, dir := range aoc.FourWays {
			nr, nc = r+dir[0], c+dir[1]
			if grid[nr][nc] == '#' {
				continue
			}
			if len(path) >= 2 &&
				nr == path[len(path)-2][0] &&
				nc == path[len(path)-2][1] {
				continue
			}
			path = append(path, [2]int{nr, nc})
			break
		}
	}
	return path
}

func abs(x int) int {
	if x < 0 {
		x = -x
	}
	return x
}

func part12(grid [][]byte, cheatLength int, filter int) int {
	path := getUniquePath(grid)
	count := 0
	blocks := make(map[[2]int][]int)
	var br, bc int
	// Group the path elements into squares of side cheatLength
	for i, pos := range path {
		br, bc = pos[0]/cheatLength, pos[1]/cheatLength
		blocks[[2]int{br, bc}] = append(blocks[[2]int{br, bc}], i)
	}
	segments := make([]int, 0, len(path))
	for i := range path {
		br, bc = path[i][0]/cheatLength, path[i][1]/cheatLength
		segments = segments[:0]
		segments = append(segments, blocks[[2]int{br, bc}]...)
		segments = append(segments, blocks[[2]int{br - 1, bc}]...)
		segments = append(segments, blocks[[2]int{br + 1, bc}]...)
		segments = append(segments, blocks[[2]int{br, bc - 1}]...)
		segments = append(segments, blocks[[2]int{br - 1, bc - 1}]...)
		segments = append(segments, blocks[[2]int{br + 1, bc - 1}]...)
		segments = append(segments, blocks[[2]int{br, bc + 1}]...)
		segments = append(segments, blocks[[2]int{br - 1, bc + 1}]...)
		segments = append(segments, blocks[[2]int{br + 1, bc + 1}]...)
		for _, j := range segments {
			d := abs(path[i][0]-path[j][0]) + abs(path[i][1]-path[j][1])
			if d > cheatLength {
				continue
			}
			if j-i-d >= filter {
				count++
			}
		}
	}
	return count
}
