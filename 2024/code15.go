// Advent of Code 2024 day 15
//
// Massimo Lauria

package main

import (
	"bytes"
	"fmt"
	"io/ioutil"
	"log"
	"time"
)

const example = `##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^`

func main() {
	egrid, emoves := processText([]byte(example))
	clock := time.Now()
	data, err := ioutil.ReadFile("input15.txt")
	if err != nil {
		log.Fatal(err)
	}
	cgrid, cmoves := processText(data)
	fmt.Printf("Load time                                     - %s\n", time.Since(clock))
	clock = time.Now()
	fmt.Printf("Part1 - example   : %-25d - %s\n", part1(egrid, emoves), time.Since(clock))
	clock = time.Now()
	fmt.Printf("Part1 - challenge : %-25d - %s\n", part1(cgrid, cmoves), time.Since(clock))
	clock = time.Now()
	fmt.Printf("Part2 - example   : %-25d - %s\n", part2(egrid, emoves), time.Since(clock))
	clock = time.Now()
	fmt.Printf("Part2 - challenge : %-25d - %s\n", part2(cgrid, cmoves), time.Since(clock))
}

// up, right, down, left
var FourWays = [4][2]int{{-1, 0}, {0, +1}, {+1, 0}, {0, -1}}

type Grid [][]byte
type Moves []int

func printGrid(g Grid) {
	for _, s := range g {
		fmt.Printf("%s\n", s)
	}
}

func processText(data []byte) (Grid, Moves) {
	data = bytes.TrimSpace(data)
	lines := bytes.Split(data, []byte("\n"))
	grid := make(Grid, 0)
	var i int
	for i = 0; i < len(lines); i++ {
		if len(lines[i]) == 0 {
			break
		}
		grid = append(grid, lines[i])
	}
	moves := make(Moves, 0)
	for ; i < len(lines); i++ {
		for j := 0; j < len(lines[i]); j++ {
			switch lines[i][j] {
			case '^':
				moves = append(moves, 0)
			case '>':
				moves = append(moves, 1)
			case 'v':
				moves = append(moves, 2)
			case '<':
				moves = append(moves, 3)
			}
		}
	}
	return grid, moves
}

func part1(grid Grid, moves Moves) int {
	N := len(grid)
	rr, rc := (N-1)/2, (N-1)/2
	for _, dir := range moves {
		dr, dc := FourWays[dir][0], FourWays[dir][1]
		tr, tc := rr+dr, rc+dc
		for grid[tr][tc] == 'O' {
			tr, tc = tr+dr, tc+dc
		}
		if grid[tr][tc] == '#' {
			continue
		}
		grid[tr][tc] = 'O'
		grid[rr][rc] = '.'
		rr += dr
		rc += dc
		grid[rr][rc] = '@'
	}
	score := 0
	for r := 0; r < N; r++ {
		for c := 0; c < N; c++ {
			if grid[r][c] == 'O' {
				score += 100*r + c
			}
		}
	}
	return score
}

func part2(grid Grid, moves Moves) int {
	return len(moves)
}
