// Advent of Code 2024 day 22
//
// Massimo Lauria

package main

import (
	"aoc2024/aoc"
	"fmt"
	"time"
)

const example = `
1
10
100
2024
`
const example2 = `
1
2
3
2024
`

func main() {
	clock := time.Now()
	example := aoc.AllNumbersInString(example)
	example2 := aoc.AllNumbersInString(example2)
	challenge := aoc.AllNumbersInFile("input22.txt")
	fmt.Printf("Load time                                     - %s\n", time.Since(clock))
	clock = time.Now()
	fmt.Printf("Part1 - example   : %-25d - %s\n", part1(example), time.Since(clock))
	clock = time.Now()
	fmt.Printf("Part1 - challenge : %-25d - %s\n", part1(challenge), time.Since(clock))
	clock = time.Now()
	fmt.Printf("Part2 - example2  : %-25d - %s\n", part2(example2), time.Since(clock))
	clock = time.Now()
	fmt.Printf("Part2 - challenge : %-25d - %s\n", part2(challenge), time.Since(clock))
}

func part1(values []int) int {
	mask := (1 << 24) - 1
	total := 0
	for _, n := range values {
		for i := 0; i < 2000; i++ {
			n = (n ^ (n << 6)) & mask
			n = (n ^ (n >> 5)) & mask
			n = (n ^ (n << 11)) & mask
		}
		total += n
	}
	return total
}

func part2(values []int) int {

	touched := make([]int, 1<<20)
	gains := make([]int, 1<<20)
	var packed, o int
	var mask = (1 << 20) - 1
	var bitmask = (1 << 24) - 1
	var lastdigit int
	var diff int
	for s, n := range values {
		lastdigit = n % 10
		diff = 0
		packed = 0
		for i := 0; i < 2000; i++ {
			o = n
			n = (n ^ (n << 6)) & bitmask
			n = (n ^ (n >> 5)) & bitmask
			n = (n ^ (n << 11)) & bitmask
			lastdigit = n % 10
			diff = n%10 - o%10
			packed = (packed<<5 + (10 + diff)) & mask
			if i < 3 {
				continue
			}
			if touched[packed] <= s {
				touched[packed] = s + 1
				gains[packed] += lastdigit
			}
		}
	}
	maxvalue := 0
	for _, v := range gains {
		maxvalue = max(maxvalue, v)
	}
	return maxvalue
}
