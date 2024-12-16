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

func main() {
	example1 := processText([]byte(example1))
	example2 := processText([]byte(example2))
	clock := time.Now()
	data, err := ioutil.ReadFile("input16.txt")
	if err != nil {
		log.Fatal(err)
	}
	challenge := processText(data)
	d := time.Since(clock)
	fmt.Printf("Load time                                     - %s\n", time.Since(clock))

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

func processText(data []byte) [][]byte {
	data = bytes.TrimSpace(data)
	return bytes.Split(data, []byte("\n"))
}

type Conf struct {
	r, c   int
	dr, dc int
}

// Priority Queue (sort of)

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

func part12(grid [][]byte) (int, int) {
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
	useful := make(map[Conf]bool)
	reached := false
	var minCost int
	// start exploration
	for queue.Len() > 0 {
		top = heap.Pop(queue).(ConfQueueItem)
		cf, dist = top.conf, top.cost
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
	inPath(start, finalCost, useful)
	tiles := make(map[[2]int]bool)
	for k, v := range useful {
		if v {
			tiles[[2]int{k.r, k.c}] = true
		}
	}

	return minCost, len(tiles)
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
	turnleft := Conf{r: from.r, c: from.c, dr: -from.dc, dc: from.dr}
	turnright := Conf{r: from.r, c: from.c, dr: from.dc, dc: -from.dr}
	forward := Conf{r: from.r + from.dr, c: from.c + from.dc, dr: from.dr, dc: from.dc}
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
