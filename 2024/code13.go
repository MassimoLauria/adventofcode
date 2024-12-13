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
	example := processText([]byte(example))
	clock := time.Now()
	data, err := ioutil.ReadFile("input13.txt")
	if err != nil {
		log.Fatal(err)
	}
	challenge := processText(data)
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

func processText(data []byte) []int {
	r, err := regexp.Compile(`(\d+)`)
	if err != nil {
		panic(err)
	}
	m := r.FindAllStringSubmatch(string(data), -1)
	prizes := make([]int, 0, len(m))
	for _, v := range m {
		x, _ := strconv.Atoi(v[1])
		prizes = append(prizes, x)
	}
	return prizes
}

func part1(values []int) int {
	if len(values)%6 != 0 {
		log.Fatalln("Invalid data")
	}
	// for i := 0; i < len(values); i += 6 {
	// 	ax, ay, X, Y := values[i], values[i+1]
	// 	bx, by := values[i+2], values[i+3]
	// 	X, Y := values[i+4], values[i+5]
	// }
	return len(values)
}

func part2(values []int) int {
	if len(values)%6 != 0 {
		log.Fatalln("Invalid data")
	}
	return len(values)
}
