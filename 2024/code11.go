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
	fmt.Printf("Part1 - example   : %-25d - %s\n", part1(example), time.Since(clock))
	clock = time.Now()
	fmt.Printf("Part1 - challenge : %-25d - %s\n", part1(challenge), time.Since(clock))
	clock = time.Now()
	fmt.Printf("Part2 - example   : %-25d - %s\n", part2(example), time.Since(clock))
	clock = time.Now()
	fmt.Printf("Part2 - challenge : %-25d - %s\n", part2(challenge), time.Since(clock))
}

func processText(data []byte) int {
	data = bytes.TrimSpace(data)
	lines := bytes.Split(data, []byte("\n"))
	return len(lines)
}

func splitNumber(v int) (int, int, bool) {
	block := 1
	for v/(block*block) > 0 {
		block *= 10
	}
	return v / block, v % block, (10*v)/(block*block) > 0
}

type StoneCache map[[2]int]int

func score_stone(cache StoneCache, stone int, blinks int) int {
	if blinks == 0 {
		return 1
	}
	query := [2]int{stone, blinks}
	result, ok := cache[query]
	if ok {
		return result
	}
	if stone == 0 {
		result = score_stone(cache, 1, blinks-1)
		cache[query] = result
		return result
	}
	if a, b, split := splitNumber(stone); split {
		result = score_stone(cache, a, blinks-1) + score_stone(cache, b, blinks-1)
	} else {
		result = score_stone(cache, stone*2024, blinks-1)
	}
	cache[query] = result
	return result
}

func solve(stones []int, blinks int) int {
	score := 0
	cache := make(StoneCache)
	for _, stone := range stones {
		score += score_stone(cache, stone, blinks)
	}
	return score
}

func part1(stones []int) int {
	return solve(stones, 25)
}

func part2(stones []int) int {
	return solve(stones, 75)
}
