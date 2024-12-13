// Advent of Code 2024 day 13
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

const example = `Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279`

func main() {
	example := processText(example)
	clock := time.Now()
	data, err := ioutil.ReadFile("input13.txt")
	if err != nil {
		log.Fatal(err)
	}
	challenge := processText(string(data))
	fmt.Printf("Load time                                     - %s\n", time.Since(clock))
	clock = time.Now()
	fmt.Printf("Part1 - example   : %-25d - %s\n", solve(example, false), time.Since(clock))
	clock = time.Now()
	fmt.Printf("Part1 - challenge : %-25d - %s\n", solve(challenge, false), time.Since(clock))
	clock = time.Now()
	fmt.Printf("Part2 - example   : %-25d - %s\n", solve(example, true), time.Since(clock))
	clock = time.Now()
	fmt.Printf("Part2 - challenge : %-25d - %s\n", solve(challenge, true), time.Since(clock))
}

func processText(data string) []int {
	values := make([]int, 0)
	r := regexp.MustCompile(`\d+`)
	m := r.FindAllStringSubmatch(data, -1)
	var x int
	for i := 0; i < len(m); i++ {
		x, _ = strconv.Atoi(m[i][0])
		values = append(values, x)
	}
	return values
}

func solve(values []int, p2 bool) int {
	score := 0
	var pa, pb, det int
	var X, Y, ax, ay, bx, by int
	for i := 0; i < len(values); i += 6 {
		ax, ay = values[i], values[i+1]
		bx, by = values[i+2], values[i+3]
		X, Y = values[i+4], values[i+5]
		if p2 {
			X += 10000000000000
			Y += 10000000000000
		}
		det = ax*by - bx*ay // always non zero, apparently
		pa = X*by - bx*Y
		pb = ax*Y - X*ay
		if pa%det == 0 && pb%det == 0 {
			// always positive solutions, apparently
			score += 3*pa/det + pb/det
		}
	}
	return score
}
