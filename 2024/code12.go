// Advent of Code 2024 day 12
//
// Massimo Lauria

package main

import (
	"bytes"
	"fmt"
	"io/ioutil"
	"log"
	"time"
)

const example = `RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE`

func main() {
	example := processText([]byte(example))
	clock := time.Now()
	data, err := ioutil.ReadFile("input12.txt")
	if err != nil {
		log.Fatal(err)
	}
	challenge := processText(data)
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

func processText(data []byte) [][]byte {
	data = bytes.TrimSpace(data)
	lines := bytes.Split(data, []byte("\n"))
	return lines
}

func flood(i, j int, grid [][]byte, ids [][]int) (int, int) {
	region := ids[i][j]
	N := len(grid)
	plant := grid[i][j]
	area := 0
	perimeter := 0
	queue := make([][2]int, 0)
	qidx := 0
	directions := [4][2]int{{-1, 0}, {+1, 0}, {0, -1}, {0, +1}}
	var ci, cj, ni, nj int
	queue = append(queue, [2]int{i, j})
	for qidx < len(queue) {
		// explore a new patch
		ci, cj = queue[qidx][0], queue[qidx][1]
		area++
		for _, delta := range directions {
			ni, nj = ci+delta[0], cj+delta[1]
			switch {
			case nj < 0, nj >= N, ni < 0, ni >= N:
				perimeter++
			case grid[ni][nj] != plant:
				perimeter++
			case ids[ni][nj] == 0 && grid[ni][nj] == plant:
				ids[ni][nj] = region
				queue = append(queue, [2]int{ni, nj})
			}
		}
		qidx++
	}
	return area, perimeter
}

func part1(grid [][]byte) int {
	N := len(grid)
	var ids [][]int
	nextid := 1
	price := 0
	var a, p int
	ids = make([][]int, N)
	for i := 0; i < N; i++ {
		ids[i] = make([]int, N)
	}
	for i := 0; i < N; i++ {
		for j := 0; j < N; j++ {
			if ids[i][j] > 0 {
				continue
			}
			ids[i][j] = nextid
			a, p = flood(i, j, grid, ids)
			price += a * p
			nextid++
		}
	}
	return price
}

func part2(grid [][]byte) int {
	return len(grid)
}
