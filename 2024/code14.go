// Advent of Code 2024 day 14
//
// Massimo Lauria

package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"regexp"
	"strconv"
	"time"
)

const example = `
p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3
`

func main() {
	example := processText(example)
	clock := time.Now()
	data, err := ioutil.ReadFile("input14.txt")
	if err != nil {
		log.Fatal(err)
	}
	challenge := processText(string(data))
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

func processText(data string) []int {
	values := make([]int, 0)
	r := regexp.MustCompile(`-?\d+`)
	m := r.FindAllStringSubmatch(data, -1)
	var x int
	for i := 0; i < len(m); i++ {
		x, _ = strconv.Atoi(m[i][0])
		values = append(values, x)
	}
	return values
}

func part1(values []int) int {
	return len(values)
}

func part2(values []int) int {
	return len(values)
}
