// Advent of Code 2024 day 04
//
// Massimo Lauria

package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"strings"
    "strconv"
)

var ToInt=strconv.Atoi

const example_data = `MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX`

func read_input_file(filename string) string {
	data, err := ioutil.ReadFile(filename)
	if err != nil {
		fmt.Println("File", filename, "not found")
		os.Exit(1)
	}
	return string(data)
}

func process_text(data string) []string {
	lines := strings.Split(string(data),"\n")
	n := len(lines)
	if len(lines[n-1])==0 {
		lines = lines[:n-1]
    }
	if n==0 || len(lines)!=len(lines[0]) {
		panic("data is non a square grid")
	}
	return lines
}


func main() {
	data := read_input_file("input04.txt")
	example := process_text(example_data)
	values  := process_text(data)
	fmt.Println("Part1 - example  ", part1(example))
	fmt.Println("Part1 - solution ", part1(values))
	fmt.Println("Part2 - example"  , part2(example))
	fmt.Println("Part2 - solution ", part2(values))
}

func xmas_in_all_directions(text []string, r int, c int) int {
	n:=len(text)
	count:=0
	if text[r][c]!='X' { return count }
	for dr:=-1;dr<2;dr++ {
		if r+dr*3 >=n {continue}
		if r+dr*3 <0  {continue}
		for dc:=-1;dc<2;dc++ {
			// which direction should I look
			if dr==0 && dc==0 { continue }
			if c+dc*3 >=n {continue}
			if c+dc*3 <0  {continue}
			if text[r+1*dr][c+1*dc]!='M' {continue}
			if text[r+2*dr][c+2*dc]!='A' {continue}
			if text[r+3*dr][c+3*dc]!='S' {continue}
			count+=1
		}
	}
	return count
}

func is_xmas_pattern(text []string, r int, c int) bool {
	if text[r][c]!='A' { return false }
	ch1:=text[r-1][c-1]
	ch2:=text[r+1][c+1]
	if !(ch1=='M' && ch2=='S' || ch2=='M' && ch1=='S') { return false }
	ch1=text[r+1][c-1]
	ch2=text[r-1][c+1]
	if !(ch1=='M' && ch2=='S' || ch2=='M' && ch1=='S') { return false }
	return true
}


func part1(text []string) int {
	n:=len(text)
	count:=0
	for r:=0;r<n;r++ {
		for c:=0;c<n;c++ {
			count+= xmas_in_all_directions(text,r,c)
		}
	}
	return count
}

func part2(text []string) int {
	n:=len(text)
	count:=0
	for r:=1;r<n-1;r++ {
		for c:=1;c<n-1;c++ {
			if is_xmas_pattern(text,r,c) {
				count++
			}
		}
	}
	return count
}
