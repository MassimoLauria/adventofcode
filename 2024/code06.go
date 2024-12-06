// Advent of Code 2024 day 06
//
// Massimo Lauria

package main

import (
	"fmt"
	"io/ioutil"
	"os"
)

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

type Conf [4]int
type WalkCache map[Conf]Conf

type Grid struct {
	N           int
	initial_pos [2]int
	data        map[[2]int]rune
	cache       WalkCache
}

var OutOfGrid = Conf{-1, -1, -1, -1}

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
	lab.cache = make(WalkCache)
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
	var temp int
	current_pos := lab.initial_pos
	current_dir := [2]int{-1, 0}
	lab.data[lab.initial_pos] = 'X'

	for {
		next_pos[0] = current_pos[0] + current_dir[0]
		next_pos[1] = current_pos[1] + current_dir[1]

		if next_pos[0] < 0 || next_pos[1] < 0 ||
			next_pos[0] >= lab.N || next_pos[1] >= lab.N {
			break
		}

		c, ok = lab.data[next_pos]
		if !ok || c == 'X' {
			lab.data[next_pos] = 'X'
			current_pos = next_pos
		} else {
			// rotate 90 degree clockwise (a,b) --> (b,-a)
			temp = -current_dir[0]
			current_dir[0] = current_dir[1]
			current_dir[1] = temp
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

func walk_next_event(current_conf [4]int, lab *Grid) [4]int {
	var nr, nc int
	var cr, cc int
	var dr, dc int
	var c rune
	var ok bool

	cr, cc = current_conf[0], current_conf[1]
	dr, dc = current_conf[2], current_conf[3]

	for {
		// compute next move
		nr = cr + dr
		nc = cc + dc

		if nr < 0 || nc < 0 || nr >= lab.N || nc >= lab.N {
			return OutOfGrid
		}

		c, ok = lab.data[[2]int{nr, nc}]
		if ok && c == '#' {
			return Conf{cr, cc, dc, -dr} // rotate 90 (dr,dc) --> (dc,-dr)
		}
		cr, cc = nr, nc
	}
}

func may_cache(last, curr [4]int, crate [2]int) bool {
	return !(last == OutOfGrid ||
		last[0] == crate[0] ||
		last[1] == crate[1] ||
		curr[0] == crate[0] ||
		curr[1] == crate[1])
}

func doesloop(lab *Grid, new_crate [2]int) bool {
	var ok bool
	current_conf := Conf{
		lab.initial_pos[0],
		lab.initial_pos[1],
		-1, 0} // Up
	var maybe_next Conf
	var last_conf Conf
	visited := make(map[Conf]bool)
	lab.data[new_crate] = '#'
	for {
		// compute next move
		maybe_next, ok = lab.cache[current_conf]
		if current_conf[0] != new_crate[0] && current_conf[1] != new_crate[1] && ok {
			last_conf = OutOfGrid
			current_conf = maybe_next
		} else {
			last_conf = current_conf
			current_conf = walk_next_event(current_conf, lab)
		}

		if current_conf == OutOfGrid { // left the grid
			lab.data[new_crate] = 'X'
			return false
		}

		if may_cache(last_conf, current_conf, new_crate) {
			lab.cache[last_conf] = current_conf
		}

		//
		_, ok = visited[current_conf]
		if ok {
			lab.data[new_crate] = 'X'
			return true
		}
		visited[current_conf] = true
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
