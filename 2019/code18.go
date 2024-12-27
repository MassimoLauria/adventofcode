// Advent of Code 2019 day 18
//
// Massimo Lauria

package main

import (
	"aoc2019/aoc"
	"bytes"
	"fmt"
	"log"
	"strings"
	"time"
)

const example = `
########################
#f.D.E.e.C.b.A.@.a.B.c.#
######################.#
#d.....................#
########################
`

const example2 = `
#################
#i.G..c...e..H.p#
########.########
#j.A..b...f..D.o#
########@########
#k.E..a...g..B.n#
########.########
#l.F..d...h..C.m#
#################
`

const example3 = `
#############
#g#f.D#..h#l#
#F###e#E###.#
#dCba...BcIJ#
######@######
#nK.L...G...#
#M###N#H###.#
#o#m..#i#jk.#
#############
`

func main() {
	example := aoc.GridFromString(example)
	example2 := aoc.GridFromString(example2)
	example3 := aoc.GridFromString(example3)
	clock := time.Now()
	challenge, err := aoc.GridFromFile("input18.txt")
	if err != nil {
		log.Fatal(err)
	}
	fmt.Printf("Load time                                     - %s\n", time.Since(clock))
	clock = time.Now()
	fmt.Printf("Part1 - example   : %-25d - %s\n", part1(example), time.Since(clock))
	clock = time.Now()
	fmt.Printf("Part1 - example2  : %-25d - %s\n", part1(example2), time.Since(clock))
	clock = time.Now()
	clock = time.Now()
	fmt.Printf("Part1a- example   : %-25d - %s\n", part1alt(example), time.Since(clock))
	clock = time.Now()
	fmt.Printf("Part1a- example2  : %-25d - %s\n", part1alt(example2), time.Since(clock))
	clock = time.Now()
	fmt.Printf("Part2 - example3  : %-25d - %s\n", part2(example3), time.Since(clock))
	clock = time.Now()
	fmt.Printf("Part1 - challenge : %-25d - %s\n", part1(challenge), time.Since(clock))
	clock = time.Now()
	fmt.Printf("Part1a- challenge : %-25d - %s\n", part1alt(challenge), time.Since(clock))
	clock = time.Now()
	fmt.Printf("Part2 - challenge : %-25d - %s\n", part2(challenge), time.Since(clock))
}

func processText(data []byte) int {
	data = bytes.TrimSpace(data)
	lines := bytes.Split(data, []byte("\n"))
	return len(lines)
}

func getGridInfo(grid [][]byte) (int, int, byte) {
	var r, c int
	alpha := byte('A')
	for i := range grid {
		for j := range grid[0] {
			switch grid[i][j] {
			case '@':
				r, c = i, j
			case '.', '#':
			default:
				if 'a' <= grid[i][j] && grid[i][j] <= 'z' {
					alpha = max(alpha, grid[i][j])
				}
			}
		}
	}
	return r, c, alpha
}

type Status struct {
	r, c int
	keys int
}

func keysStr(k int) string {
	var sb strings.Builder
	for i := 0; i < 27; i++ {
		if (k & (1 << i)) != 0 {
			sb.WriteString(string('a' + i))
		}
	}
	return sb.String()
}

func scanNextKeys(grid [][]byte, current Status) map[Status]int {
	bfs := make([]Status, 1)
	qidx := 0
	bfs[0] = current
	cost := make(map[Status]int)
	nextKeys := make(map[Status]int)
	cost[bfs[0]] = 0
	var cs, ns Status
	var r, c, key int
	for qidx < len(bfs) {
		cs = bfs[qidx]
		for _, dir := range aoc.FourWays {
			r, c = cs.r+dir[0], cs.c+dir[1]
			if grid[r][c] == '#' {
				continue
			}
			ns = Status{r: r, c: c, keys: cs.keys}
			switch {
			case grid[r][c] == '.', grid[r][c] == '@':
			case grid[r][c] >= 'A' && grid[r][c] <= 'Z':
				key = 1 << int(grid[r][c]-'A')
				if ns.keys&key == 0 {
					continue
				}
			case grid[r][c] >= 'a' && grid[r][c] <= 'z':
				key = 1 << int(grid[r][c]-'a')
				if ns.keys&key == 0 {
					ns.keys = ns.keys | key
					nextKeys[ns] = cost[cs] + 1
					continue
				}
			}
			if _, ok := cost[ns]; !ok {
				cost[ns] = cost[cs] + 1
				bfs = append(bfs, ns)
			}
		}
		qidx++
	}
	return nextKeys
}

func part1(grid [][]byte) int {
	sr, sc, Z := getGridInfo(grid)
	bfs := make([]Status, 1)
	qidx := 0
	bfs[0] = Status{sr, sc, 0}
	cost := make(map[Status]int)
	cost[bfs[0]] = 0
	var cs, ns Status
	var r, c, key int
	var allKeys = (1 << (int(Z-'a') + 1)) - 1
	for qidx < len(bfs) {
		cs = bfs[qidx]
		if cs.keys == allKeys {
			break
		}
		for _, dir := range aoc.FourWays {
			r, c = cs.r+dir[0], cs.c+dir[1]
			if grid[r][c] == '#' {
				continue
			}
			ns = Status{r: r, c: c, keys: cs.keys}
			switch {
			case grid[r][c] == '.', grid[r][c] == '@':
			case grid[r][c] >= 'A' && grid[r][c] <= 'Z':
				key = 1 << int(grid[r][c]-'A')
				if ns.keys&key == 0 {
					continue
				}
			case grid[r][c] >= 'a' && grid[r][c] <= 'z':
				key = 1 << int(grid[r][c]-'a')
				ns.keys = ns.keys | key
			}
			if _, ok := cost[ns]; !ok {
				cost[ns] = cost[cs] + 1
				bfs = append(bfs, ns)
			}
		}
		qidx++
	}
	return cost[cs]
}

func part1alt(grid [][]byte) int {

	sr, sc, Z := getGridInfo(grid)
	var allKeys = (1 << (int(Z-'a') + 1)) - 1

	// min heap setup
	Q := aoc.NewMinHeap[Status]()
	cs := Status{r: sr, c: sc, keys: 0}
	dist := 0
	Q.Improve(cs, dist)
	cost := make(map[Status]int)
	var ns Status
	var ndist int
	for Q.Len() > 0 {
		cs, dist = Q.Pop()
		cost[cs] = dist
		if cs.keys == allKeys {
			break
		}
		//fmt.Println("Visiting", cs)
		for ns, ndist = range scanNextKeys(grid, cs) {
			//fmt.Println("-- considering", ns, keysStr(ns.keys), "at dist", ndist)
			if _, ok := cost[ns]; !ok {
				Q.Improve(ns, cost[cs]+ndist)
			}
		}
	}
	return cost[cs]
}

type Status2 struct {
	r, c [4]int
	keys int
}

func part2(grid [][]byte) int {
	sr, sc, Z := getGridInfo(grid)
	grid[sr][sc] = '#'
	grid[sr-1][sc] = '#'
	grid[sr+1][sc] = '#'
	grid[sr][sc-1] = '#'
	grid[sr][sc+1] = '#'
	var allKeys = (1 << (int(Z-'a') + 1)) - 1
	// min heap setup
	var cs, ns Status2
	cs.r = [4]int{sr - 1, sr + 1, sr - 1, sr + 1}
	cs.c = [4]int{sc - 1, sc - 1, sc + 1, sc + 1}
	cs.keys = 0
	dist := 0
	Q := aoc.NewMinHeap[Status2]()
	Q.Improve(cs, dist)
	cost := make(map[Status2]int)
	var cs1 Status
	for Q.Len() > 0 {
		cs, dist = Q.Pop()
		cost[cs] = dist
		if cs.keys == allKeys {
			break
		}
		for i := 0; i < 4; i++ {
			cs1 = Status{r: cs.r[i], c: cs.c[i], keys: cs.keys}
			for ns1, ndist := range scanNextKeys(grid, cs1) {
				ns = cs
				ns.r[i] = ns1.r
				ns.c[i] = ns1.c
				ns.keys = ns1.keys
				//fmt.Println("-- considering", ns, keysStr(ns.keys), "at dist", ndist)
				if _, ok := cost[ns]; !ok {
					Q.Improve(ns, cost[cs]+ndist)
				}
			}
		}
	}
	return cost[cs]
}
