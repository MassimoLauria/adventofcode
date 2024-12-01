// Advent of Code 2024 day 01
//
// Massimo Lauria

package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"slices"
	"strings"
)

const example_data = `3   4
4   3
2   5
1   3
3   9
3   3`

func read_input_file(filename string) string {
	data, err := ioutil.ReadFile(filename)
	if err != nil {
		fmt.Println("File", filename, "not found")
		os.Exit(1)
	}
	return string(data)
}

func process_text(data string) ([]int, []int) {
	lines := strings.Split(data, "\n")
	n := len(lines)
	if len(lines[n-1]) == 0 {
		lines = lines[:n-1]
		n--
	}
	var left []int
	var right []int
	var a, b int
	for _, s := range lines {
		n, err := fmt.Sscanf(s, "%d %d", &a, &b)
		if err != nil || n != 2 {
			panic(err)
		}
		left = append(left, a)
		right = append(right, b)
	}
	slices.Sort(left)
	slices.Sort(right)
	return left, right
}

func main() {
	data := read_input_file("input01.txt")
	ex_left, ex_right := process_text(example_data)
	left, right := process_text(data)
	fmt.Println("Part1 - example ", part1(ex_left, ex_right))
	fmt.Println("Part1 - solution", part1(left, right))
	fmt.Println("Part2 - example ", part2(ex_left, ex_right))
	fmt.Println("Part2 - solution", part2(left, right))
}

func part1(left, right []int) int {
	total := 0
	for i, _ := range left {
		total += max(left[i]-right[i], right[i]-left[i])
	}
	return total
}

func part2(left, right []int) int {
	N := len(left)
	var v int
	total := 0
	i, j := 0, 0
	sl, sr := 0, 0
	for i < N && j < N {
		if left[i] < right[j] {
			i++
			continue
		}
		if left[i] > right[j] {
			j++
			continue
		}
		v = left[i]
		sl, sr = 0, 0
		for i < N && left[i] == v {
			i++
			sl++
		}
		for j < N && right[j] == v {
			j++
			sr++
		}
		total += sr * sl * v
	}
	return total
}
