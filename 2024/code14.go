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

func rem(N, D int) int {
	if N%D < 0 {
		return N%D + D
	} else {
		return N % D
	}
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

func grid(values []int, W, H int) {
	var c, x, y int
	gridmap := make([]byte, W*H)
	for i := 0; i < W*H; i++ {
		gridmap[i] = '.'
	}
	for i := 0; i < len(values); i += 4 {
		c = values[i+1]*W + values[i]
		if gridmap[c] == '.' {
			gridmap[c] = '1'
		} else if gridmap[c] == '9' {
			gridmap[c] = '0'
		} else {
			gridmap[c] += 1
		}
	}
	c = 0
	for y = 0; y < H; y += 1 {
		for x = 0; x < W; x += 1 {
			fmt.Printf("%c", gridmap[c])
			c++
		}
		fmt.Println()
	}
}

func part1(values []int, W, H int) int {
	var quads [4]int
	qpos := 0
	x, y := 0, 0
	for i := 0; i < len(values); i += 4 {
		x = rem(values[i]+100*values[i+2], W)
		y = rem(values[i+1]+100*values[i+3], H)
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

func heuristic(values []int, W, H int) int {
	return 0
}

// Solve equation a+tb = v (mod P)
// for t, assuming P is prime
// t is positive
func solveLin(a, b, v, P int) int {
	b = rem(b, P) //
	binv := 0
	for i := 1; i < P; i++ {
		if rem(i*b, P) == 1 {
			binv = i
			break
		}
	}
	return rem(binv*(v-a), P)
}

func part2(values []int, W, H int) int {
	max_v := 0
	max_t := 0
	v := 0
	// Normalize
	for i := 0; i < len(values); i += 4 {
		if values[i+2] < 0 {
			values[i+2] += W
		}
		if values[i+3] < 0 {
			values[i+3] += H
		}
	}
	for T := 0; T < 1000; T += 1 {
		v = 0
		for i := 0; i < len(values); i += 4 {
			values[i] = (values[i] + values[i+2]) % W
			values[i+1] = (values[i+1] + values[i+3]) % H
		}
		v = heuristic(values, W, H)
		if v > max_v {
			max_t = T
			max_v = v
		}
	}
	fmt.Println(max_t, "with", max_v, "robot on central line")
	grid(values, W, H)
	return len(values)
}
