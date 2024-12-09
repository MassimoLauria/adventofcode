// Advent of Code 2024 day 09
//
// Massimo Lauria

package main

import (
	"fmt"
	"io/ioutil"
	"os"
)

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

	fmt.Println("Part1 - example", part1(exampleData))
	fmt.Println("Part1 - solution ", part1(data))

	efiles, eholes = processText(exampleData)
	files, holes = processText(data)
	fmt.Println("Part2 - example", part2(efiles, eholes))
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

func part1(data string) int {
	disk := make([]int, 0)
	var size int
	for i, bvalue := range data {
		size = int(bvalue - '0')
		switch true {
		case bvalue == '\n': // end of string
			break
		case i%2 == 0: // new file
			for j := 0; j < size; j++ {
				disk = append(disk, i/2)
			}
		case size != 0: // non empty hole
			for j := 0; j < size; j++ {
				disk = append(disk, -1)
			}
		}
	}
	start := 0
	end := len(disk) - 1
	for start < end {
		switch true {
		case disk[start] >= 0:
			start++
		case disk[end] < 0:
			end--
		default:
			disk[start] = disk[end]
			disk[end] = -1
		}
	}
	c := 0
	i := 0
	for disk[i] >= 0 {
		c += i * disk[i]
		i++
	}
	return c
}

func checksum(files []Block) int {
	c := 0
	for _, file := range files {
		c += file.id * file.size * (2*file.pos + file.size - 1) / 2
	}
	return c
}

func part2(files []Block, holes []Hole) int {
	var starts [10]int
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
