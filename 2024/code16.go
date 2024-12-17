// Advent of Code 2024 day 16
//
// Massimo Lauria

package main

import (
	"aoc2024/aoc"
	"fmt"
	"time"
)

const example1 = `
###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############
`
const example2 = `
#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################
`

func main() {
	example1 := aoc.GridFromString(example1)
	example2 := aoc.GridFromString(example2)
	clock := time.Now()
	challenge, _ := aoc.GridFromFile("input16.txt")
	d := time.Since(clock)
	fmt.Printf("Load time                                      - %s\n", time.Since(clock))

	var p1, p2 int

	clock = time.Now()
	p1, p2 = part12(example1)
	d = time.Since(clock)
	fmt.Printf("Part1 - example1   : %-25d - %s\n", p1, d)
	fmt.Printf("Part2 - example1   : %-25d - %s\n", p2, d)
	clock = time.Now()
	p1, p2 = part12(example2)
	d = time.Since(clock)
	fmt.Printf("Part1 - example2   : %-25d - %s\n", p1, d)
	fmt.Printf("Part2 - example2   : %-25d - %s\n", p2, d)
	clock = time.Now()
	p1, p2 = part12(challenge)
	d = time.Since(clock)
	fmt.Printf("Part1 - challenge  : %-25d - %s\n", p1, d)
	fmt.Printf("Part2 - challenge  : %-25d - %s\n", p2, d)
}

type Conf struct {
	r, c int
	dir  [2]int
}

func inPath(from Conf, finalCost map[Conf]int, cache map[Conf]bool) bool {
	var ok bool
	var thisCost int
	if v, ok := cache[from]; ok {
		return v
	}
	if thisCost, ok = finalCost[from]; !ok {
		return false
	}
	res := false
	turnleft := Conf{r: from.r, c: from.c, dir: aoc.RoL90(from.dir)}
	turnright := Conf{r: from.r, c: from.c, dir: aoc.RoR90(from.dir)}
	forward := Conf{r: from.r + from.dir[0], c: from.c + from.dir[1],
		dir: from.dir}
	if v, _ := finalCost[turnleft]; v == thisCost+1000 && inPath(turnleft, finalCost, cache) {
		res = true
	}
	if v, _ := finalCost[turnright]; v == thisCost+1000 && inPath(turnright, finalCost, cache) {
		res = true
	}
	if v, _ := finalCost[forward]; v == thisCost+1 && inPath(forward, finalCost, cache) {
		res = true
	}
	cache[from] = res
	return res
}

func part12(grid [][]byte) (int, int) {
	N := len(grid)
	Q := aoc.NewMinHeap[Conf]()
	var cf Conf
	var dist int

	// initial conf
	start := Conf{r: N - 2, c: 1, dir: aoc.RIGHT} // facing EAST, i.e. {0,+1}
	Q.Improve(start, 0)
	finalCost := make(map[Conf]int)
	useful := make(map[Conf]bool)
	reached := false
	var minCost int
	// start exploration
	for Q.Len() > 0 {
		cf, dist = Q.Pop()
		if reached && dist > minCost {
			continue
		}
		_, ok := finalCost[cf]
		if ok {
			continue
		}
		finalCost[cf] = dist
		// found the target
		if grid[cf.r][cf.c] == 'E' && !reached {
			reached = true
			minCost = dist
			useful[cf] = true
			continue
		}
		//
		turnleft := Conf{r: cf.r, c: cf.c, dir: aoc.RoL90(cf.dir)}
		if _, ok := finalCost[turnleft]; !ok {
			Q.Improve(turnleft, dist+1000)
		}
		turnright := Conf{r: cf.r, c: cf.c, dir: aoc.RoR90(cf.dir)}
		if _, ok := finalCost[turnright]; !ok {
			Q.Improve(turnright, dist+1000)
		}
		forward := Conf{r: cf.r + cf.dir[0], c: cf.c + cf.dir[1],
			dir: cf.dir}
		if grid[forward.r][forward.c] != '#' {
			if _, ok := finalCost[forward]; !ok {
				Q.Improve(forward, dist+1)
			}
		}
	}
	inPath(start, finalCost, useful)
	tiles := make(map[[2]int]bool)
	for k, v := range useful {
		if v {
			tiles[[2]int{k.r, k.c}] = true
		}
	}

	return minCost, len(tiles)
}
