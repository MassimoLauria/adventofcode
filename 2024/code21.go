// Advent of Code 2024 day 21
//
// Massimo Lauria

package main

import (
	"bytes"
	"fmt"
	"math"
	"strconv"
	"time"
)

const example = `
029A
980A
179A
456A
379A
`

const challenge = `
083A
935A
964A
149A
789A
`

var keymap = map[byte][2]int{
	'A': {0, 0},
	'0': {0, -1},
	'1': {-1, -2}, '2': {-1, -1}, '3': {-1, 0},
	'4': {-2, -2}, '5': {-2, -1}, '6': {-2, 0},
	'7': {-3, -2}, '8': {-3, -1}, '9': {-3, 0},
	//
	'^': {0, -1},
	'<': {1, -2}, 'v': {1, -1}, '>': {1, 0},
}

func main() {
	example := processText([]byte(example))
	challenge := processText([]byte(challenge))
	clock := time.Now()
	fmt.Printf("Part1 - example   : %-25d - %s\n", part1(example), time.Since(clock))
	clock = time.Now()
	fmt.Printf("Part1 - challenge : %-25d - %s\n", part1(challenge), time.Since(clock))
	// clock = time.Now()
	// fmt.Printf("Part2 - example   : %-25d - %s\n", part2(example), time.Since(clock))
	clock = time.Now()
	fmt.Printf("Part2 - challenge : %-25d - %s\n", part2(challenge), time.Since(clock))
}

func processText(data []byte) [][]byte {
	data = bytes.TrimSpace(data)
	lines := bytes.Split(data, []byte("\n"))
	return lines
}

type Call struct {
	r, c int
	code string
	T    int
}

var CACHE = make(map[Call]int)

func recurseCode(r, c int, code []byte, T int) int {
	if T <= 0 || len(code) == 0 {
		return len(code)
	}
	call := Call{r: r, c: c, code: string(code), T: T}
	shortest, ok := CACHE[call]
	if ok {
		return shortest
	}
	var j, lr, lc int
	var rch, cch byte
	var lenHV, lenVH int
	b := code[0]
	dr, dc := keymap[b][0]-r, keymap[b][1]-c
	tr, tc := keymap[b][0], keymap[b][1]
	if dr >= 0 {
		rch = 'v'
		lr = dr
	} else {
		rch = '^'
		lr = -dr
	}
	if dc >= 0 {
		cch = '>'
		lc = dc
	} else {
		cch = '<'
		lc = -dc
	}
	// horiz vert
	if r == 0 && c+dc == -2 { // cannot move here
		lenHV = math.MaxInt
	} else {
		optionHV := make([]byte, 0)
		for j = 0; j < lc; j++ {
			optionHV = append(optionHV, cch)
		}
		for j = 0; j < lr; j++ {
			optionHV = append(optionHV, rch)
		}
		optionHV = append(optionHV, 'A')
		lenHV = recurseCode(0, 0, optionHV, T-1)
	}

	// vert horiz
	if r+dr == 0 && c == -2 { // cannot move here
		lenVH = math.MaxInt
	} else {
		optionVH := make([]byte, 0)
		for j = 0; j < lr; j++ {
			optionVH = append(optionVH, rch)
		}
		for j = 0; j < lc; j++ {
			optionVH = append(optionVH, cch)
		}
		optionVH = append(optionVH, 'A')
		lenVH = recurseCode(0, 0, optionVH, T-1)
	}

	result := min(lenHV, lenVH) + recurseCode(tr, tc, code[1:], T)
	CACHE[call] = result
	return result
}

func part1(codes [][]byte) int {
	total := 0
	ITER := 3
	var v, l int
	for _, code := range codes {
		v, _ = strconv.Atoi(string(code[:3]))
		l = recurseCode(0, 0, code, ITER)
		total += v * l
	}
	return total
}

func part2(codes [][]byte) int {
	total := 0
	ITER := 26
	var v, l int
	for _, code := range codes {
		v, _ = strconv.Atoi(string(code[:3]))
		l = recurseCode(0, 0, code, ITER)
		total += v * l
	}
	return total
}
