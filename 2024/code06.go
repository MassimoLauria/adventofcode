// Advent of Code 2024 day 06
//
// Massimo Lauria

package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"strconv"
)

var ToInt = strconv.Atoi

var dirs [4][2]int = [4][2]int{{-1, 0}, {0, 1}, {1, 0}, {0, -1}}

func void() [3]int { return [3]int{-1, -1, -1} }

func walk_step(pos [2]int, toward int) [2]int {
	d := dirs[toward]
	return [2]int{pos[0] + d[0], pos[1] + d[1]}
}

const example_data = `....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...`

type Grid struct {
	N           int
	initial_pos [2]int
	data        map[[2]int]rune
}

func inside(pos [2]int, lab *Grid) bool {
	return (0 <= pos[0]) && (pos[0] < lab.N) && (0 <= pos[1]) && (pos[1] < lab.N)
}

func read_input_file(filename string) string {
	data, err := ioutil.ReadFile(filename)
	if err != nil {
		fmt.Fprintf(os.Stderr, "File %s not found\n", filename)
		os.Exit(1)
	}
	return string(data)
}

func process_text(data string) Grid {
	r, c := 0, 0
	lab := Grid{}
	lab.data = make(map[[2]int]rune)
	for _, s := range data {
		switch s {
		case '\n':
			r++
			c = 0
		case '.':
			c++
		case '^':
			lab.initial_pos = [2]int{r, c}
			c++
		case '#':
			lab.data[[2]int{r, c}] = s
			c++
		default:
			fmt.Fprintf(os.Stderr, "Malformed input")
			os.Exit(1)
		}
	}
	if c != r+1 {
		// ends with a newline
		lab.N = r
	} else {
		lab.N = r + 1
	}
	return lab
}

func main() {
	data := read_input_file("input06.txt")
	example := process_text(example_data)
	values := process_text(data)
	fmt.Println("Part1 - example  ", part1(example))
	fmt.Println("Part1 - solution ", part1(values))
	fmt.Println("Part2 - example", part2(example))
	fmt.Println("Part2 - solution ", part2(values))
}

func part1(lab Grid) int {
	var next_pos [2]int
	var c rune
	var ok bool

	current_pos := lab.initial_pos
	current_dir := 0
	lab.data[lab.initial_pos] = 'X'

	for {
		next_pos = walk_step(current_pos, current_dir)
		if !inside(next_pos, &lab) {
			break
		}
		c, ok = lab.data[next_pos]
		if !ok || c == 'X' {
			lab.data[next_pos] = 'X'
			current_pos = next_pos
		} else {
			// turn direction
			current_dir = (current_dir + 1) % len(dirs)
		}
	}
	visited := 0
	for _, k := range lab.data {
		if k == 'X' {
			visited++
		}
	}
	return visited
}

func doesloop(lab *Grid, new_crate [2]int) bool {
	var c rune
	var ok bool
	current_pos := lab.initial_pos
	var next_pos [2]int
	current_dir := 0
	turns := make(map[[3]int]bool)
	var record [3]int
	lab.data[new_crate] = '#'
	for {
		// compute next move
		next_pos = walk_step(current_pos, current_dir)

		if !inside(next_pos, lab) {
			lab.data[new_crate] = 'X'
			return false
		}

		c, ok = lab.data[next_pos]
		if !ok || c == 'X' {
			current_pos = next_pos
		} else {
			// take a turn
			current_dir = (current_dir + 1) % len(dirs)
			record[0] = current_pos[0]
			record[1] = current_pos[1]
			record[2] = current_dir
			_, ok = turns[record]
			if ok {
				lab.data[new_crate] = 'X'
				return true
			}
			turns[record] = true
		}
	}
}

func part2(lab Grid) int {
	loop_locations := 0
	try_count := 0
	for place, char := range lab.data {
		if char == '#' || place == lab.initial_pos {
			continue
		}
		try_count += 1
		if doesloop(&lab, place) {
			loop_locations++
		}
	}
	return loop_locations
}
