// Advent of Code 2024 day 08
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

const example_data = `............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............`

type Locations map[byte][][2]int

func read_input_file(filename string) string {
	data, err := ioutil.ReadFile(filename)
	if err != nil {
		fmt.Fprintf(os.Stderr, "File %s not found\n", filename)
		os.Exit(1)
	}
	return string(data)
}

func process_text(data string) (int, Locations) {
	lines := strings.Split(string(data), "\n")
	n := len(lines)
	if len(lines[n-1]) == 0 {
		lines = lines[:n-1]
		n--
	}
	locations := make(Locations)
	for r := 0; r < n; r++ {
		for c := 0; c < n; c++ {
			switch lines[r][c] {
			case '.':
				continue
			default:
				locations[lines[r][c]] = append(locations[lines[r][c]], [2]int{r, c})
			}
		}
	}
	return n, locations
}

func main() {
	data := read_input_file("input08.txt")
	en, example := process_text(example_data)
	n, values := process_text(data)
	fmt.Println("Part1 - example  ", part1(en, example))
	fmt.Println("Part1 - solution ", part1(n, values))
	fmt.Println("Part2 - example", part2(en, example))
	fmt.Println("Part2 - solution ", part2(n, values))
}

func antiNodes(loc1 [2]int, loc2 [2]int) ([2]int, [2]int) {
	var n1, n2 [2]int
	d0 := loc1[0] - loc2[0]
	d1 := loc1[1] - loc2[1]
	n1[0] = loc1[0] + d0
	n1[1] = loc1[1] + d1
	n2[0] = loc2[0] - d0
	n2[1] = loc2[1] - d1
	return n1, n2
}

func inside(loc [2]int, n int) bool {
	return loc[0] >= 0 && loc[1] >= 0 && loc[0] < n && loc[1] < n
}

func part1(n int, locations Locations) int {
	nodes := make(map[[2]int]bool)
	for _, ls := range locations {
		for i := 0; i < len(ls)-1; i++ {
			for j := i + 1; j < len(ls); j++ {
				n1, n2 := antiNodes(ls[i], ls[j])
				if inside(n1, n) {
					nodes[n1] = true
				}
				if inside(n2, n) {
					nodes[n2] = true
				}
			}
		}
	}
	return len(nodes)
}

func gcd(a, b int) int {
	a = max(a, -a)
	b = max(b, -b)
	a, b = max(a, b), min(a, b)
	for b > 0 {
		a, b = b, a%b
	}
	return a
}

func collectLine(n int, a, b [2]int, touched map[[2]int]bool) {
	var d0, d1, g int
	var s [2]int
	d0 = a[0] - b[0]
	d1 = a[1] - b[1]
	g = gcd(d0, d1)
	d0 /= g
	d1 /= g
	s = a
	for inside(s, n) {
		touched[s] = true
		s[0] = s[0] + d0
		s[1] = s[1] + d1
	}
	s[0] = a[0] - d0
	s[1] = a[1] - d1
	for inside(s, n) {
		touched[s] = true
		s[0] = s[0] - d0
		s[1] = s[1] - d1
	}
}

func part2(n int, locations Locations) int {
	nodes := make(map[[2]int]bool)
	for _, ls := range locations {
		for i := 0; i < len(ls)-1; i++ {
			for j := i + 1; j < len(ls); j++ {
				collectLine(n, ls[i], ls[j], nodes)
			}
		}
	}
	return len(nodes)
}
