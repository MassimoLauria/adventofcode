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

const exampleData = `3   4
4   3
2   5
1   3
3   9
3   3`

func readInputFile(filename string) string {
	data, err := ioutil.ReadFile(filename)
	if err != nil {
		fmt.Println("File", filename, "not found")
		os.Exit(1)
	}
	return string(data)
}

func processText(data string) ([]int, []int) {
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
	data := readInputFile("input01.txt")
	leftEx, rightEx := processText(exampleData)
	left, right := processText(data)
	fmt.Println("Part1 - example ", part1(leftEx, rightEx))
	fmt.Println("Part1 - solution", part1(left, right))
	fmt.Println("Part2 - example ", part2(leftEx, rightEx))
	fmt.Println("Part2 - solution", part2(left, right))
}

func part1(left, right []int) int {
	total := 0
	for i := range left {
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
