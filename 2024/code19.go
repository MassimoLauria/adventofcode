// Advent of Code 2024 day 19
//
// Massimo Lauria

package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"strings"
	"time"
)

const example = `
r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb`

func main() {
	etowels, epatterns := processText(example)
	clock := time.Now()
	data, err := ioutil.ReadFile("input19.txt")
	if err != nil {
		log.Fatal(err)
	}
	ctowels, cpatterns := processText(string(data))
	fmt.Printf("Load time                                     - %s\n", time.Since(clock))
	clock = time.Now()
	fmt.Printf("Part1 - example   : %-25d - %s\n", part1(etowels, epatterns), time.Since(clock))
	clock = time.Now()
	fmt.Printf("Part1 - challenge : %-25d - %s\n", part1(ctowels, cpatterns), time.Since(clock))
	clock = time.Now()
	fmt.Printf("Part2 - example   : %-25d - %s\n", part2(etowels, epatterns), time.Since(clock))
	clock = time.Now()
	fmt.Printf("Part2 - challenge : %-25d - %s\n", part2(ctowels, cpatterns), time.Since(clock))
}

func processText(data string) ([]string, []string) {
	data = strings.TrimSpace(data)
	lines := strings.Split(data, "\n")
	if len(lines[1]) != 0 {
		log.Fatal("malformed input")
	}
	return strings.Split(lines[0], ", "), lines[2:]
}

func designPossible(text string, towels []string, cache map[string]int) int {
	if len(text) == 0 {
		return 1
	}
	if v, ok := cache[text]; ok {
		return v
	}
	for _, t := range towels {
		if strings.HasPrefix(text, t) {
			cache[text] += designPossible(text[len(t):], towels, cache)
		}
	}
	return cache[text]
}

func part1(towels []string, patterns []string) int {
	cache := make(map[string]int)
	count := 0
	for _, p := range patterns {
		if designPossible(p, towels, cache) > 0 {
			count++
		}
	}
	return count
}

func part2(towels []string, patterns []string) int {
	cache := make(map[string]int)
	count := 0
	for _, p := range patterns {
		count += designPossible(p, towels, cache)
	}
	return count
}
