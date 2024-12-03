// Advent of Code 2024 day 03
//
// Massimo Lauria

package main

import (
	"fmt"
	"regexp"
	"io/ioutil"
	"os"
    "strconv"
)

var Atoi=strconv.Atoi

const example_data = `xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))`

const example_data2 =`xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))`

func read_input_file(filename string) string {
	data, err := ioutil.ReadFile(filename)
	if err != nil {
		fmt.Println("File", filename, "not found")
		os.Exit(1)
	}
	return string(data)
}


func main() {
	data := read_input_file("input03.txt")
	fmt.Println("Part1 - example  ", part1(example_data))
	fmt.Println("Part1 - solution ", part1(data))
	fmt.Println("Part2 - example"  , part2(example_data2))
	fmt.Println("Part2 - solution ", part2(data))
}

func part1(data string) int {
	var a,b int
	total:=0
	r := regexp.MustCompile(`mul\((\d+),(\d+)\)`)
	for _,v := range r.FindAllStringSubmatch(data,-1) {
		a,_ = Atoi(v[1])
		b,_ = Atoi(v[2])
		total += a*b
	}
	return total
}

func part2(data string) int {
	var a,b int
	total:=0
	enabled:=true
	r := regexp.MustCompile(`mul\((\d+),(\d+)\)|do\(\)|don't\(\)`)
	for _,v := range r.FindAllStringSubmatch(data,-1) {
		if v[0]==`do()` {
			enabled = true
		} else if v[0]==`don't()` {
			enabled = false
		} else if enabled {
			a,_ = Atoi(v[1])
			b,_ = Atoi(v[2])
			total += a*b
		}
	}
	return total
}
