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

func fillSequence(n int, digits []int) {
	mask := (1 << 24) - 1
	length := len(digits)
	var o int
	for i := 0; i < length; i++ {
		o = n
		n = (n ^ (n << 6)) & mask
		n = (n ^ (n >> 5)) & mask
		n = (n ^ (n << 11)) & mask
		digits[i] = n%10 - o%10
	}
}

func gains(n int, diffs []int) map[int]int {
	lastdigit := n%10 + diffs[0] + diffs[1] + diffs[2]
	gains := make(map[int]int)
	var packed = (10+diffs[0])<<10 + (10+diffs[1])<<5 + (10 + diffs[2])
	var mask = (1 << 20) - 1
	for i := 3; i < len(diffs); i++ {
		lastdigit += diffs[i]
		packed = (packed<<5 + (10 + diffs[i])) & mask
		_, ok := gains[packed]
		if !ok {
			gains[packed] = lastdigit
		}
	}
	return gains
}

func part2(values []int) int {

	global := make(map[int]int)
	buffer := make([]int, 2000)
	for _, n := range values {
		fillSequence(n, buffer)
		g := gains(n, buffer)
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
