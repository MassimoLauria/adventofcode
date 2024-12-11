// Advent of Code 2024 day 11
//
// Massimo Lauria

package main

import (
	"bytes"
	"fmt"
	"io/ioutil"
	"log"
	"strconv"
	"time"
)

func main() {
	example := []int{125, 17}
	clock := time.Now()
	var v int
	data, err := ioutil.ReadFile("input11.txt")
	if err != nil {
		log.Fatal(err)
	}
	challenge := make([]int, 0)
	for _, s := range bytes.Fields(data) {
		v, _ = strconv.Atoi(string(s))
		challenge = append(challenge, v)
	}
	fmt.Printf("Load time                                     - %s\n", time.Since(clock))
	clock = time.Now()
	fmt.Printf("Part1 - example   : %-25d - %s\n", solve(example, 25), time.Since(clock))
	clock = time.Now()
	fmt.Printf("Part1 - challenge : %-25d - %s\n", solve(challenge, 25), time.Since(clock))
	clock = time.Now()
	fmt.Printf("Part2 - example   : %-25d - %s\n", solve(example, 75), time.Since(clock))
	clock = time.Now()
	fmt.Printf("Part2 - challenge : %-25d - %s\n", solve(challenge, 75), time.Since(clock))
}

func splitNumber(v int) (int, int, bool) {
	block := 1
	for v/(block*block) > 0 {
		block *= 10
	}
	return v / block, v % block, (10*v)/(block*block) > 0
}

func solve(stones []int, blinks int) int {
	score := 0
	count := make(map[int]int)
	var next map[int]int
	var l, r int
	var split bool
	// load
	for _, s := range stones {
		count[s] += 1
	}
	for b := 0; b < blinks; b++ {
		next = make(map[int]int)
		for s, n := range count {
			if s == 0 {
				next[1] += n
				continue
			}
			l, r, split = splitNumber(s)
			if split {
				next[l] += n
				next[r] += n
			} else {
				next[s*2024] += n
			}
		}
		count = next
	}
	for _, n := range count {
		score += n //score_stone(cache, stone, blinks)
	}
	return score
}
