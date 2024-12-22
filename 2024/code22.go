// Advent of Code 2024 day 22
//
// Massimo Lauria

package main

import (
	"aoc2024/aoc"
	"fmt"
	"time"
)

const example = `1
10
100
2024
`
const example2 = `1
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

func sequence(n, length int) []int {
	mask := (1 << 24) - 1
	digits := make([]int, length)
	var o int
	for i := 0; i < length; i++ {
		o = n
		n = (n ^ (n << 6)) & mask
		n = (n ^ (n >> 5)) & mask
		n = (n ^ (n << 11)) & mask
		digits[i] = n%10 - o%10
	}
	return digits
}

func gains(n int, diffs []int) map[[4]int]int {
	lastdigit := n%10 + diffs[0] + diffs[1] + diffs[2]
	gains := make(map[[4]int]int)
	var pattern [4]int
	for i := 3; i < len(diffs); i++ {
		lastdigit += diffs[i]
		pattern[0] = diffs[i-3]
		pattern[1] = diffs[i-2]
		pattern[2] = diffs[i-1]
		pattern[3] = diffs[i]
		_, ok := gains[pattern]
		if !ok {
			gains[pattern] = lastdigit
		}
	}
	return gains
}

func part2(values []int) int {
	global := make(map[[4]int]int)
	for _, n := range values {
		s := sequence(n, 2000)
		g := gains(n, s)
		for p, v := range g {
			global[p] += v
		}
	}
	maxvalue := 0
	for _, v := range global {
		maxvalue = max(maxvalue, v)
	}
	return maxvalue
}
