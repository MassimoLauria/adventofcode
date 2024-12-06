// Advent of Code 2024 day 06
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

var ToInt = strconv.Atoi

const example_data = `London to Dublin = 464
London to Belfast = 518
Dublin to Belfast = 141`

type Metric map[[2]string]int

func read_input_file(filename string) string {
	data, err := ioutil.ReadFile(filename)
	if err != nil {
		fmt.Fprintf(os.Stderr, "File %s not found\n", filename)
		os.Exit(1)
	}
	return string(data)
}

func process_text(data string) ([]string, Metric) {
	lines := strings.Split(string(data), "\n")
	n := 0
	metric := make(Metric)
	names := make([]string, 0)
	var a, b string
	var d int
	var err error
	for _, line := range lines {
		n, err = fmt.Sscanf(line, "%s to %s = %d", &a, &b, &d)
		if n != 3 || err != nil {
			break
		}
		if len(names) == 0 || a != names[len(names)-1] {
			names = append(names, a)
		}
		metric[[2]string{a, b}] = d
		metric[[2]string{b, a}] = d
	}
	return names, metric
}

func main() {
	data := read_input_file("input09.txt")
	ecities, edist := process_text(example_data)
	cities, dist := process_text(data)
	fmt.Println("Part1 - example  ", part1(ecities, edist))
	fmt.Println("Part1 - solution ", part1(cities, dist))
	fmt.Println("Part2 - example", part2(ecities, edist))
	fmt.Println("Part2 - solution ", part2(cities, dist))
}

func part1(cities []string, dist Metric) int {
	return 0
}

func part2(cities []string, dist Metric) int {
	return 0
}
