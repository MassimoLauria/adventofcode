// Advent of Code 2024 day 07
//
// Massimo Lauria

package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"strconv"
	"strings"
)

var ToInt = strconv.ParseInt

const example_data = `190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20`

func read_input_file(filename string) string {
	data, err := ioutil.ReadFile(filename)
	if err != nil {
		fmt.Fprintf(os.Stderr, "File %s not found\n", filename)
		os.Exit(1)
	}
	return string(data)
}

type Equation struct {
	target   int64
	operands []int64
}

func process_text(data string) []Equation {
	var temp int64
	var parts []string
	lines := strings.Split(string(data), "\n")
	n := len(lines)
	if len(lines[n-1]) == 0 {
		lines = lines[:n-1]
		n--
	}
	eqs := make([]Equation, 0, n)
	for i, line := range lines {
		parts = strings.Fields(line)
		temp, _ = ToInt(parts[0][:len(parts[0])-1], 10, 64)
		eqs = append(eqs, Equation{temp, nil})
		for j := 1; j < len(parts); j++ {
			temp, _ = ToInt(parts[j], 10, 64)
			eqs[i].operands = append(eqs[i].operands, temp)
		}
	}
	return eqs
}

func main() {
	data := read_input_file("input07.txt")
	example := process_text(example_data)
	values := process_text(data)
	fmt.Println("Part1 - example  ", part1(example))
	fmt.Println("Part1 - solution ", part1(values))
	fmt.Println("Part2 - example", part2(example))
	fmt.Println("Part2 - solution ", part2(values))
}

func part1(equations []Equation) int64 {
	var total int64 = 0
	for _, equation := range equations {
		if is_sat(0, equation.target, equation.operands, 0, false) {
			total += equation.target
		}
	}
	return total
}

func digits10(x int64) int64 {
	var i int64 = 1
	if x == 0 {
		return 10
	}
	for x > 0 {
		x = x / 10
		i *= 10
	}
	return i
}

func is_sat(value, target int64, operands []int64, idx int, part2 bool) bool {
	if idx == len(operands) {
		return value == target
	}
	if value > target {
		return false
	}
	var temp int64
	temp = value * operands[idx]
	if temp <= target {
		if is_sat(temp, target, operands, idx+1, part2) {
			return true
		}
	}
	temp = value + operands[idx]
	if temp <= target {
		if is_sat(temp, target, operands, idx+1, part2) {
			return true
		}
	}
	if !part2 {
		return false
	}
	temp = value*digits10(operands[idx]) + operands[idx]
	if temp <= target {
		if is_sat(temp, target, operands, idx+1, true) {
			return true
		}
	}
	return false
}

func part2(equations []Equation) int64 {
	var total int64 = 0
	for _, equation := range equations {
		if is_sat(0, equation.target, equation.operands, 0, true) {
			total += equation.target
		}
	}
	return total
}
