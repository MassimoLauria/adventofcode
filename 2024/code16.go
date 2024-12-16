// Advent of Code 2024 day 16
//
// Massimo Lauria

package main

import (
	"bytes"
	"container/heap"
	"fmt"
	"io/ioutil"
	"log"
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

func assert(b bool) {
	if !b {
		log.Fatal("Assertion failed")
	}
}

func main() {
	example1 := processText([]byte(example1))
	example2 := processText([]byte(example2))
	clock := time.Now()
	data, err := ioutil.ReadFile("input16.txt")
	if err != nil {
		log.Fatal(err)
	}
	challenge := processText(data)
	fmt.Printf("Load time                                     - %s\n", time.Since(clock))
	clock = time.Now()
	fmt.Printf("Part1 - example1   : %-25d - %s\n", part1(example1), time.Since(clock))
	clock = time.Now()
	fmt.Printf("Part1 - example2   : %-25d - %s\n", part1(example2), time.Since(clock))
	clock = time.Now()
	fmt.Printf("Part1 - challenge : %-25d - %s\n", part1(challenge), time.Since(clock))
	clock = time.Now()
	fmt.Printf("Part2 - example   : %-25d - %s\n", part2(example1), time.Since(clock))
	clock = time.Now()
	fmt.Printf("Part2 - challenge : %-25d - %s\n", part2(challenge), time.Since(clock))
}

func processText(data []byte) [][]byte {
	data = bytes.TrimSpace(data)
	return bytes.Split(data, []byte("\n"))
}

type Conf struct {
	r, c   int
	dr, dc int
}

type ConfQueueItem struct {
	conf Conf
	cost int
}

type PQueue []ConfQueueItem

func (h PQueue) Len() int           { return len(h) }
func (h PQueue) Less(i, j int) bool { return h[i].cost < h[j].cost }
func (h PQueue) Swap(i, j int)      { h[i], h[j] = h[j], h[i] }

func (h *PQueue) Push(x any) {
	// Push and Pop use pointer receivers because they modify the slice's length,
	// not just its contents.
	*h = append(*h, x.(ConfQueueItem))
}

func (h *PQueue) Pop() any {
	old := *h
	n := len(old)
	x := old[n-1]
	*h = old[0 : n-1]
	return x
}

func part1(grid [][]byte) int {
	N := len(grid)
	var cf Conf
	var dist int

	// initial conf
	start := Conf{r: N - 2, c: 1,
		dr: 0, dc: 1} // facing EAST, i.e. {0,+1}
	queue := &PQueue{}
	heap.Push(queue, ConfQueueItem{conf: start, cost: 0})
	var top ConfQueueItem
	finalCost := make(map[Conf]int)
	var reached bool
	var minCost int
	// start exploration
	for queue.Len() > 0 {
		top = heap.Pop(queue).(ConfQueueItem)
		cf, dist = top.conf, top.cost
		if reached && top.cost > minCost {
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
			continue
		}
		//
		turnleft := Conf{r: cf.r, c: cf.c, dr: -cf.dc, dc: cf.dr}
		if _, ok := finalCost[turnleft]; !ok {
			heap.Push(queue, ConfQueueItem{conf: turnleft, cost: dist + 1000})
		}
		turnright := Conf{r: cf.r, c: cf.c, dr: cf.dc, dc: -cf.dr}
		if _, ok := finalCost[turnright]; !ok {
			heap.Push(queue, ConfQueueItem{conf: turnright, cost: dist + 1000})
		}
		forward := Conf{r: cf.r + cf.dr, c: cf.c + cf.dc, dr: cf.dr, dc: cf.dc}
		if grid[forward.r][forward.c] != '#' {
			if _, ok := finalCost[forward]; !ok {
				heap.Push(queue, ConfQueueItem{conf: forward, cost: dist + 1})
			}
		}
	}
	return minCost
}

func part2(grid [][]byte) int {
	return 0
}
