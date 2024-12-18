// Advent of Code 2024 day 18
//
// Massimo Lauria

package main

import (
	"aoc2024/aoc"
	"fmt"
	"strconv"
	"strings"
	"time"
)

const example = `5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0`

func main() {
	example := aoc.AllNumbersInString(example)
	clock := time.Now()
	challenge := aoc.AllNumbersInFile("input18.txt")

	fmt.Printf("Load time                                     - %s\n", time.Since(clock))
	clock = time.Now()
	fmt.Printf("Part1 - example   : %-25d - %s\n", part1(example, 12, 7), time.Since(clock))
	clock = time.Now()
	fmt.Printf("Part1 - challenge : %-25d - %s\n", part1(challenge, 1024, 71), time.Since(clock))
	clock = time.Now()
	fmt.Printf("Part2 - example   : %-25s - %s\n", part2(example, 7), time.Since(clock))
	clock = time.Now()
	fmt.Printf("Part2 - challenge : %-25s - %s\n", part2(challenge, 71), time.Since(clock))
}

func part1broken(values []int, B int, N int) int {
	G := aoc.MakeGrid(N, N, '.')
	for i := 0; i < 2*B; i += 2 {
		G[values[i+1]][values[i]] = '#'
	}
	G = aoc.AddBorderToGrid(G, '#')
	start := [2]int{1, 1}  // adding border offset
	target := [2]int{N, N} // adding border offset

	Q := aoc.NewMinHeap[[2]int]()
	// initial conf
	Q.Improve(start, 0)
	var pos, newpos [2]int
	var dist int
	// start exploration
	for Q.Len() > 0 {
		pos, dist = Q.Pop()
		G[pos[0]][pos[1]] = byte(dist%10) + '0'
		// found the target
		if pos == target {
			aoc.PrintGrid(G)
			return dist
		}
		for _, dir := range aoc.FourWays {
			newpos = [2]int{pos[0] + dir[0], pos[1] + dir[1]}
			if G[newpos[0]][newpos[1]] == '.' {
				Q.Improve(newpos, dist+1)
			}
		}
	}
	aoc.PrintGrid(G)
	return dist
}

func part1(values []int, B int, N int) int {
	G := aoc.MakeGrid(N, N, '.')
	for i := 0; i < 2*B; i += 2 {
		G[values[i+1]][values[i]] = '#'
	}
	G = aoc.AddBorderToGrid(G, '#')
	start := [2]int{1, 1}  // adding border offset
	target := [2]int{N, N} // adding border offset

	Q := make([][2]int, 0, 10000)
	// initial conf
	finalcost := make(map[[2]int]int)
	finalcost[start] = 0
	Q = append(Q, start)
	qidx := 0
	// start exploration
	var pos, newpos [2]int
	var dist int
	for qidx < len(Q) {
		pos = Q[qidx]
		dist = finalcost[pos]
		// found the target
		if pos == target {
			return finalcost[target]
		}
		for _, dir := range aoc.FourWays {
			newpos = [2]int{pos[0] + dir[0], pos[1] + dir[1]}
			_, ok := finalcost[newpos]
			if G[newpos[0]][newpos[1]] != '#' && !ok {
				Q = append(Q, newpos)
				finalcost[newpos] = dist + 1
			}
		}
		qidx++
	}
	return -1
}

func part2(values []int, N int) string {
	start := 0
	end := len(values) / 2
	var mid int
	for start+1 < end {
		mid = (start + end) / 2
		switch part1(values, mid, N) {
		case -1:
			end = mid
		default:
			start = mid
		}
	}
	x := strconv.Itoa(values[2*end-2])
	y := strconv.Itoa(values[2*end-1])
	return strings.Join([]string{x, y}, ",")
}
