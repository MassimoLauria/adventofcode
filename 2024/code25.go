// Advent of Code 2024 day 25
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

const example = `
#####
.####
.####
.####
.#.#.
.#...
.....

#####
##.##
.#.##
...##
...#.
...#.
.....

.....
#....
#....
#...#
#.#.#
#.###
#####

.....
.....
#.#..
###..
###.#
###.#
#####

.....
.....
.....
#....
#.#..
#.#.#
#####
`

func main() {
	el, ek := processText([]byte(example))
	clock := time.Now()
	data, err := ioutil.ReadFile("input25.txt")
	if err != nil {
		log.Fatal(err)
	}
	cl, ck := processText(data)
	fmt.Printf("Load time                                     - %s\n", time.Since(clock))
	clock = time.Now()
	fmt.Printf("Part1 - example   : %-25d - %s\n", part1(el, ek), time.Since(clock))
	clock = time.Now()
	fmt.Printf("Part1 - challenge : %-25d - %s\n", part1(cl, ck), time.Since(clock))
}

func processText(data []byte) ([][5]int, [][5]int) {
	data = bytes.TrimSpace(data)
	lines := bytes.Split(data, []byte("\n"))
	l := 0
	var keys [][5]int
	var locks [][5]int
	var tuple [5]int
	var top byte
	for l < len(lines) {
		top = lines[l][0]
		for j := 0; j < 5; j++ {
			for i := 1; i < 7; i++ {
				if lines[l+i][j] != top {
					tuple[j] = i - 1
					break
				}
			}
		}
		if top == '#' {
			locks = append(locks, tuple)
		} else {
			for i := 0; i < 5; i++ {
				tuple[i] = 5 - tuple[i]
			}
			keys = append(keys, tuple)
		}
		l += 8
	}
	return locks, keys
}

func part1(locks, keys [][5]int) int {
	good := 0
	count := 0
	for i := 0; i < len(locks); i++ {
		for j := 0; j < len(keys); j++ {
			good = 1
			for t := 0; t < 5; t++ {
				if locks[i][t]+keys[j][t] > 5 {
					good = 0
					break
				}
			}
			count += good
		}
	}
	return count
}
