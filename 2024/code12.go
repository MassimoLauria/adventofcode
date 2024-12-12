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
	N := len(grid)
	var ids [][]int
	nextid := 1
	ids = make([][]int, N)
	for i := 0; i < N; i++ {
		ids[i] = make([]int, N)
	}
	areas := make([]int, 1)
	for i := 0; i < N; i++ {
		for j := 0; j < N; j++ {
			if ids[i][j] > 0 {
				continue
			}
			ids[i][j] = nextid
			a, _ := flood(i, j, grid, ids)
			areas = append(areas, a)
			nextid++
		}
	}
	corners := make([]int, len(areas))
	// 4 corners
	corners[ids[0][0]] += 1
	corners[ids[0][N-1]] += 1
	corners[ids[N-1][0]] += 1
	corners[ids[N-1][N-1]] += 1
	// corners on the sides
	for i := 1; i < N; i++ {
		if ids[0][i-1] != ids[0][i] {
			corners[ids[0][i-1]] += 1
			corners[ids[0][i]] += 1
		}
		if ids[N-1][i-1] != ids[N-1][i] {
			corners[ids[N-1][i-1]] += 1
			corners[ids[N-1][i]] += 1
		}
		if ids[i-1][0] != ids[i][0] {
			corners[ids[i-1][0]] += 1
			corners[ids[i][0]] += 1
		}
		if ids[i-1][N-1] != ids[i][N-1] {
			corners[ids[i-1][N-1]] += 1
			corners[ids[i][N-1]] += 1
		}
	}
	var tr, tl, br, bl int
	for i := 1; i < N; i++ {
		for j := 1; j < N; j++ {
			tl, tr = ids[i-1][j-1], ids[i-1][j]
			bl, br = ids[i][j-1], ids[i][j]
			if tl != bl && tl != tr {
				corners[tl] += 1
			}
			if bl != tl && bl != br {
				corners[bl] += 1
			}
			if tr != br && tr != tl {
				corners[tr] += 1
			}
			if br != tr && br != bl {
				corners[br] += 1
			}
		}
	}
	if N != 10 {
		return 0
	}
	for i := 1; i < len(areas); i++ {
		fmt.Printf("Region %d  a: %d c: %d\n", i, areas[i], corners[i])
	}
	return 0
}
