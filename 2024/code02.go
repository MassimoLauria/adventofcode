// Advent of Code 2024 day 02
//
// Massimo Lauria

package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"strconv"
	"strings"
	//	"slices"
)

var ToInt = strconv.Atoi

const example_data = `7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9`

func read_input_file(filename string) string {
	data, err := ioutil.ReadFile(filename)
	if err != nil {
		fmt.Println("File", filename, "not found")
		os.Exit(1)
	}
	return string(data)
}

func process_text(data string) [][]int {
	lines := strings.Split(string(data), "\n")
	n := len(lines)
	if len(lines[n-1]) == 0 {
		lines = lines[:n-1]
		n--
	}
	records := make([][]int, n)
	for i := 0; i < n; i++ {
		data := strings.Fields(lines[i])
		records[i] = make([]int, len(data))
		for j := 0; j < len(data); j++ {
			records[i][j], _ = ToInt(data[j])
		}
	}
	return records
}

func main() {
	data := read_input_file("input02.txt")
	example := process_text(example_data)
	values := process_text(data)
	fmt.Println("Part1 - example  ", part1(example))
	fmt.Println("Part1 - solution ", part1(values))
	fmt.Println("Part2 - example", part2(example))
	fmt.Println("Part2 - solution ", part2(values))
}


func is_safe(report []int) bool {
	direction := 1
	diff := 0
	if report[0] <= report[1] {
		direction = 1
	} else {
		direction = -1
	}
	for j := 0; j < len(report)-1; j++ {
		diff = (report[j+1] - report[j]) * direction
		if diff > 3 || diff < 1 {
			return false
		}
	}
	return true
}

func part1(reports [][]int) int {
	safe_reports := 0
	for _, report := range reports {
		if is_safe(report) {
			safe_reports++
		}
	}
	return safe_reports
}


func maybe_safe(sequence []int, lo, hi int) bool {
	var p,diff int
	n := len(sequence)
	// Find first violation
	for p=0;p<n-1;p++ {
		diff = sequence[p+1] - sequence[p]
		if diff < lo || diff > hi { break }
	}
	if p>=n-2 {return true}
	// first violation between p and p+1.
	// there is an element p+2
	diff = sequence[p+2] - sequence[p+1]
	maybe_remove_first :=(lo <= diff && diff <= hi)
	if p>0 {
		diff = sequence[p+1] - sequence[p-1]
		maybe_remove_first = maybe_remove_first && (lo <= diff && diff <= hi)
	}
	diff = sequence[p+2] - sequence[p]
	maybe_remove_second:=(lo <= diff && diff <= hi)
	if !(maybe_remove_first || maybe_remove_second) { return false}
	p+=2
	for ;p<n-1;p++ {
		diff = sequence[p+1] - sequence[p]
		if diff < lo || diff > hi { return false }
	}
	return true
}

func part2(reports [][]int) int {
	safe_reports := 0
	for _, report := range reports {
		if maybe_safe(report,1,3) || maybe_safe(report,-3,-1) {
			safe_reports++
		}
	}
	return safe_reports
}
