// Advent of Code 2024 day 09
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

const exampleData = `2333133121414131402`

type Block struct {
	pos  int
	id   int
	size int
}

type Hole struct {
	pos  int
	size int
}

func readInputFile(filename string) string {
	data, err := ioutil.ReadFile(filename)
	if err != nil {
		fmt.Fprintf(os.Stderr, "File %s not found\n", filename)
		os.Exit(1)
	}
	return string(data)
}

func processText(data string) ([]Block, []Hole) {
	files := make([]Block, 0, len(data))
	holes := make([]Hole, 0, len(data))
	pos := 0
	var file Block
	var hole Hole
	var size int
	for i, bvalue := range data {
		if bvalue == '\n' {
			break
		}
		size = int(bvalue - '0')
		if i%2 == 0 { // new file
			file.id = i / 2
			file.size = size
			file.pos = pos
			files = append(files, file)
		} else { // new hole
			if size == 0 {
				continue
			}
			hole.size = size
			hole.pos = pos
			holes = append(holes, hole)
		}
		pos += size
	}
	return files, holes
}

func main() {
	data := readInputFile("input09.txt")
	var efiles, files []Block
	var eholes, holes []Hole

	efiles, eholes = processText(exampleData)
	fmt.Println("Part1 - example", part1(efiles, eholes))

	files, holes = processText(data)
	fmt.Println("Part1 - solution ", part1(files, holes))

	efiles, eholes = processText(exampleData)
	fmt.Println("Part2 - example", part2(efiles, eholes))

	files, holes = processText(data)
	fmt.Println("Part2 - solution ", part2(files, holes))
}

func print_disk(files []Block) {
	pos := 0
	char := '0'
	for _, file := range files {
		for pos < file.pos {
			fmt.Printf("%c", '.')
			pos += 1
		}
		char = rune(file.id%10 + '0')
		for i := 0; i < file.size; i++ {
			fmt.Printf("%c", char)
		}
		pos += file.size
	}
	fmt.Printf("\n")
}

func split(files []Block) []Block {
	newfiles := make([]Block, 0)
	newfile := Block{pos: 0, size: 1, id: 0}
	for _, file := range files {
		for i := file.pos; i < file.pos+file.size; i++ {
			newfile.id = file.id
			newfile.pos = i
			newfiles = append(newfiles, newfile)
		}
	}
	return newfiles
}

func part1(files []Block, holes []Hole) int {
	nfiles := split(files)
	return part2(nfiles, holes)
}

func checksum(files []Block) int {
	c := 0
	for _, file := range files {
		c += file.id * file.size * (2*file.pos + file.size - 1) / 2
	}
	return c
}

func part2(files []Block, holes []Hole) int {
	starts := [10]int{0, 0, 0, 0, 0, 0, 0, 0, 0, 0}
	for fp := len(files) - 1; fp >= 0; fp-- {
		// move file fp
		for i := starts[files[fp].size]; i < len(holes); i++ {
			if holes[i].pos > files[fp].pos {
				break
			}
			if holes[i].size >= files[fp].size {
				// move file here
				starts[files[fp].size] = i
				holes[i].size = holes[i].size - files[fp].size
				files[fp].pos = holes[i].pos
				holes[i].pos = holes[i].pos + files[fp].size
				break
			}
		}
	}
	return checksum(files)
}
