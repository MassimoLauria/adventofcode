package aoc

import (
	"bytes"
	"fmt"
	"io/ioutil"
)

var UP = [2]int{-1, 0}
var RIGHT = [2]int{0, 1}
var DOWN = [2]int{1, 0}
var LEFT = [2]int{0, -1}

// the four direction from UP, going clockwise
var FourWays = [4][2]int{UP, RIGHT, DOWN, LEFT}

// Rotate a direction to the right of 90 degree
func RoR90(dir [2]int) [2]int {
	return [2]int{dir[1], -dir[0]}
}

// Rotate a direction to the left of 90 degree
func RoL90(dir [2]int) [2]int {
	return [2]int{-dir[1], dir[0]}
}

// Print a map grid of characters
func PrintGrid(g [][]byte) {
	for _, s := range g {
		fmt.Printf("%s\n", s)
	}
}

func CopyGrid(g [][]byte) [][]byte {
	newg := make([][]byte, len(g))
	for i := 0; i < len(g); i++ {
		newg[i] = make([]byte, len(g[i]))
		copy(newg[i], g[i])
	}
	return newg
}

func GridFromBytes(data []byte) [][]byte {
	data = bytes.TrimSpace(data)
	lines := bytes.Split(data, []byte("\n"))
	grid := make([][]byte, 0)
	var i int
	for i = 0; i < len(lines); i++ {
		if len(lines[i]) == 0 {
			break
		}
		grid = append(grid, lines[i])
	}
	return grid
}

func GridFromString(data string) [][]byte {
	return GridFromBytes([]byte(data))
}

func GridFromFile(filename string) ([][]byte, error) {
	data, err := ioutil.ReadFile(filename)
	if err != nil {
		return nil, err
	}
	return GridFromBytes(data), nil
}

func AddBorderToGrid(grid [][]byte, fill byte) [][]byte {
	R := len(grid)
	if R == 0 {
		result := make([][]byte, 0, 1)
		result = append(result, []byte{fill})
		return result
	}
	C := len(grid[0])
	result := make([][]byte, R+2)
	line := make([]byte, C+2)
	for i := range line {
		line[i] = fill
	}
	result[0] = make([]byte, C+2)
	result[R+1] = make([]byte, C+2)
	copy(result[0], line)
	copy(result[R+1], line)
	for i := range grid {
		result[i+1] = make([]byte, len(grid[i])+2)
		copy(result[i+1][1:len(grid[i])+1], grid[i])
		result[i+1][0] = fill
		result[i+1][len(grid[i])+1] = fill
	}
	return result
}
