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

type Grid [][]byte

func printGrid(g Grid) {
	for _, s := range g {
		fmt.Printf("%s\n", s)
	}
}

func copyGrid(g Grid) Grid {
	newg := make(Grid, len(g))
	for i := 0; i < len(g); i++ {
		newg[i] = make([]byte, len(g[i]))
		copy(newg[i], g[i])
	}
	return newg
}

func doubleGrid(g Grid) Grid {
	N := len(g)
	newg := make(Grid, N)
	var a, b byte
	for i := 0; i < len(g); i++ {
		newg[i] = make([]byte, 2*N)
		for j := 0; j < N; j++ {
			switch g[i][j] {
			case '#':
				a, b = '#', '#'
			case '.':
				a, b = '.', '.'
			case '@':
				a, b = '@', '.'
			case 'O':
				a, b = '[', ']'
			}
			newg[i][2*j] = a
			newg[i][2*j+1] = b
		}
	}
	return newg
}

func scoreGrid(g Grid, char byte) int {
	score := 0
	for r := 0; r < len(g); r++ {
		for c := 0; c < len(g[r]); c++ {
			if g[r][c] == char {
				score += 100*r + c
			}
		}
	}
	return score
}

func processText(data []byte) (Grid, [][2]int) {
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
	moves := make([][2]int, 0)
	for ; i < len(lines); i++ {
		for j := 0; j < len(lines[i]); j++ {
			switch lines[i][j] {
			case '^':
				moves = append(moves, [2]int{-1, 0})
			case '>':
				moves = append(moves, [2]int{0, +1})
			case 'v':
				moves = append(moves, [2]int{+1, 0})
			case '<':
				moves = append(moves, [2]int{0, -1})
			}
		}
	}
	return grid, moves
}

func canMove(grid Grid, r, c, dr, dc int, cache map[[2]int]bool) bool {
	var v, ok bool
	v, ok = cache[[2]int{r, c}]
	if ok {
		return v
	}
	switch {
	case grid[r][c] == '#':
		return false
	case grid[r][c] == '.':
		return true
	case grid[r][c] == 'O' || grid[r][c] == '@' || dc != 0:
		ok = canMove(grid, r+dr, c+dc, dr, dc, cache)
		cache[[2]int{r, c}] = ok
	case grid[r][c] == ']': // vertical box movement from ]
		ok = canMove(grid, r, c-1, dr, dc, cache)
	default: // vertical box movement from [
		ok = canMove(grid, r+dr, c+dc, dr, dc, cache) &&
			canMove(grid, r+dr, c+1+dc, dr, dc, cache)
		cache[[2]int{r, c + 1}] = ok
		cache[[2]int{r, c}] = ok
	}
	return ok
}

// Move a (guaranteed to be movable) object on the grid
// first moves the object needed to make room for it
func doMove(grid Grid, r, c, dr, dc int) {
	switch {
	case grid[r][c] == '.':
	case grid[r][c] == 'O' || grid[r][c] == '@' || dc != 0:
		doMove(grid, r+dr, c+dc, dr, dc)
		grid[r+dr][c+dc] = grid[r][c]
		grid[r][c] = '.'
	case grid[r][c] == ']':
		doMove(grid, r, c-1, dr, dc)
	default: // vertical box movement from [
		doMove(grid, r+dr, c+dc, dr, dc)
		doMove(grid, r+dr, c+dc+1, dr, dc)
		grid[r+dr][c+dc] = '['
		grid[r+dr][c+dc+1] = ']'
		grid[r][c] = '.'
		grid[r][c+1] = '.'
	}
}

func part1(grid Grid, moves [][2]int) int {
	grid = copyGrid(grid)
	N := len(grid)
	rr, rc := N/2-1, N/2-1
	for _, dir := range moves {
		dr, dc := dir[0], dir[1]
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
	return scoreGrid(grid, 'O')
}

func part2(grid Grid, moves [][2]int) int {
	N := len(grid)
	grid = doubleGrid(grid)
	rr, rc := N/2-1, N-2
	for _, dir := range moves {
		dr, dc := dir[0], dir[1]
		cache := make(map[[2]int]bool)
		if canMove(grid, rr, rc, dr, dc, cache) {
			doMove(grid, rr, rc, dr, dc)
			rr += dr
			rc += dc
		}
	}
	return scoreGrid(grid, '[')
}
