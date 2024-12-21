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
	fmt.Printf("Part1 - example   : %-25d - %s\n", part12(example, 3), time.Since(clock))
	clock = time.Now()
	fmt.Printf("Part1 - challenge : %-25d - %s\n", part12(challenge, 3), time.Since(clock))
	clock = time.Now()
	fmt.Printf("Part2 - example   : %-25d - %s\n", part12(example, 26), time.Since(clock))
	clock = time.Now()
	fmt.Printf("Part2 - challenge : %-25d - %s\n", part12(challenge, 26), time.Since(clock))
}

func processText(data []byte) [][]byte {
	data = bytes.TrimSpace(data)
	lines := bytes.Split(data, []byte("\n"))
	return lines
}

type Call struct {
	code string
	T    int
}

var CACHE = make(map[Call]int)

func minSequence(code []byte, T int) int {
	// base case
	if T <= 0 || len(code) == 0 {
		return len(code)
	}
	// cached result
	call := Call{code: string(code), T: T}
	if shortest, ok := CACHE[call]; ok {
		return shortest
	}

	var lenHV, lenVH int
	var vmove, hmove []byte
	result := 0
	r, c := 0, 0
	for _, b := range code {
		dr, dc := keymap[b][0]-r, keymap[b][1]-c
		if dr >= 0 {
			vmove = bytes.Repeat([]byte{'v'}, dr)
		} else {
			vmove = bytes.Repeat([]byte{'^'}, -dr)
		}
		if dc >= 0 {
			hmove = bytes.Repeat([]byte{'>'}, dc)
		} else {
			hmove = bytes.Repeat([]byte{'<'}, -dc)
		}
		// horiz vert
		if r == 0 && c+dc == -2 { // cannot move here
			lenHV = math.MaxInt
		} else {
			optionHV := make([]byte, 0)
			optionHV = append(optionHV, hmove...)
			optionHV = append(optionHV, vmove...)
			optionHV = append(optionHV, 'A')
			lenHV = minSequence(optionHV, T-1)
		}
		// vert horiz
		if r+dr == 0 && c == -2 { // cannot move here
			lenVH = math.MaxInt
		} else {
			optionVH := make([]byte, 0)
			optionVH = append(optionVH, vmove...)
			optionVH = append(optionVH, hmove...)
			optionVH = append(optionVH, 'A')
			lenVH = minSequence(optionVH, T-1)
		}
		result += min(lenHV, lenVH)
		r, c = r+dr, c+dc
	}
	CACHE[call] = result
	return result
}

func part12(codes [][]byte, ITER int) int {
	total := 0
	var v, l int
	for _, code := range codes {
		v, _ = strconv.Atoi(string(code[:3]))
		l = minSequence(code, ITER)
		total += v * l
	}
	return total
}
