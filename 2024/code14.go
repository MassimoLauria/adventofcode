// Advent of Code 2024 day 14
//
// Massimo Lauria

package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"regexp"
	"strconv"
	"time"
)

const example = `
p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3
`

func main() {
	example := processText(example)
	clock := time.Now()
	data, err := ioutil.ReadFile("input14.txt")
	if err != nil {
		log.Fatal(err)
	}
	challenge := processText(string(data))
	fmt.Printf("Load time                                     - %s\n", time.Since(clock))
	clock = time.Now()
	fmt.Printf("Part1 - example   : %-25d - %s\n", part1(example, 11, 7),
		time.Since(clock))
	// clock = time.Now()
	fmt.Printf("Part1 - challenge : %-25d - %s\n", part1(challenge, 101, 103), time.Since(clock))
	clock = time.Now()
	fmt.Printf("Part2 - challenge : %-25d - %s\n", part2(challenge, 101, 103),
		time.Since(clock))
}

func processText(data string) []int {
	values := make([]int, 0)
	r := regexp.MustCompile(`-?\d+`)
	m := r.FindAllStringSubmatch(data, -1)
	var x int
	for i := 0; i < len(m); i++ {
		x, _ = strconv.Atoi(m[i][0])
		values = append(values, x)
	}
	return values
}

func part1(values []int, W, H int) int {
	var quads [4]int
	qpos := 0
	x, y := 0, 0
	for i := 0; i < len(values); i += 4 {
		x = (values[i] + 100*values[i+2] + 100*W) % W
		y = (values[i+1] + 100*values[i+3] + 100*H) % H
		if x != W/2 && y != H/2 {
			qpos = 0
			if x > W/2 {
				qpos += 1
			}
			if y > H/2 {
				qpos += 2
			}
			quads[qpos]++
		}
	}
	r := 1
	for _, v := range quads {
		r *= v
	}
	return r
}

func printPositions(X, Y []int) {
	N := len(X)
	W := 0
	H := 0
	var r, c int
	positions := make(map[[2]int]int)
	for i := 0; i < N; i++ {
		W = max(W, X[i])
		H = max(H, Y[i])
		positions[[2]int{X[i], Y[i]}] += 1
	}
	for r = 0; r < H; r++ {
		for c = 0; c < W; c++ {
			v, ok := positions[[2]int{c, r}]
			if !ok {
				fmt.Print(".")
			} else {
				fmt.Print(v % 10)
			}
		}
		fmt.Println()
	}
	fmt.Println()
}

func heuristic(X, Y []int) bool {
	N := len(X)
	var i int
	var pos [2]int
	positions := make(map[[2]int]int)
	for i = 0; i < N; i++ {
		positions[[2]int{X[i], Y[i]}] += 1
	}
	for i = 0; i < N; i++ {
		// check pattern
		//   #
		//  ###
		// #####
		found := true
	FindLoop:
		for r := 0; r < 3; r++ {
			for c := -r; c <= r; c++ {
				pos = [2]int{X[i] + c, Y[i] + r}
				_, ok := positions[pos]
				found = found && ok
				if !found {
					break FindLoop
				}
			}
		}
		if found {
			return true
		}
	}
	return false
}

func part2(values []int, W, H int) int {
	// Normalize
	N := len(values) / 4
	xs, ys := make([]int, N), make([]int, N)
	dx, dy := make([]int, N), make([]int, N)
	for i := 0; i < len(values); i += 4 {
		xs[i/4] = values[i]
		ys[i/4] = values[i+1]
		dx[i/4] = (values[i+2] + W) % W
		dy[i/4] = (values[i+3] + H) % H
	}
	cx, cy := make([]int, N), make([]int, N)
	T := 0
	for {
		for i := 0; i < N; i++ {
			cx[i] = (xs[i] + T*dx[i]) % W
			cy[i] = (ys[i] + T*dy[i]) % H
		}
		if heuristic(cx, cy) {
			return T
		}
		T++
	}
	return 0
}
