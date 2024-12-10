// Advent of Code 2024 day 10
//
// Massimo Lauria

package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"strconv"
	"strings"
	"time"
)

var ToInt = strconv.Atoi

const exampleData = `89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732`

func readInputFile(filename string) string {
	data, err := ioutil.ReadFile(filename)
	if err != nil {
		fmt.Fprintf(os.Stderr, "File %s not found\n", filename)
		os.Exit(1)
	}
	return string(data)
}

type Vertex [2]int

type Digraph struct {
	arcs   map[Vertex][]Vertex
	value  map[Vertex]int
	starts []Vertex
	ends   []Vertex
}

func processText(data string) Digraph {
	lines := strings.Split(string(data), "\n")
	n := len(lines)
	if len(lines[n-1]) == 0 {
		lines = lines[:n-1]
		n--
	}

	var G Digraph
	G.arcs = make(map[Vertex][]Vertex)
	G.value = make(map[Vertex]int)
	G.starts = make([]Vertex, 0)
	G.ends = make([]Vertex, 0)

	for i := 0; i < n; i++ {
		for j := 0; j < n; j++ {
			G.value[Vertex{i, j}] = int(lines[i][j] - '0')
			if lines[i][j] == '0' {
				G.starts = append(G.starts, Vertex{i, j})
			}
			if lines[i][j] == '9' {
				G.ends = append(G.ends, Vertex{i, j})
			}
			if j > 0 && lines[i][j-1]-lines[i][j] == 1 {
				G.arcs[Vertex{i, j}] = append(G.arcs[Vertex{i, j}], Vertex{i, j - 1})
			}
			if j < n-1 && lines[i][j+1]-lines[i][j] == 1 {
				G.arcs[Vertex{i, j}] = append(G.arcs[Vertex{i, j}], Vertex{i, j + 1})
			}
			if i > 0 && lines[i-1][j]-lines[i][j] == 1 {
				G.arcs[Vertex{i, j}] = append(G.arcs[Vertex{i, j}], Vertex{i - 1, j})
			}
			if i < n-1 && lines[i+1][j]-lines[i][j] == 1 {
				G.arcs[Vertex{i, j}] = append(G.arcs[Vertex{i, j}], Vertex{i + 1, j})
			}
		}
	}
	return G
}

func main() {
	example := processText(exampleData)
	clock := time.Now()
	data := readInputFile("input10.txt")
	values := processText(data)
	fmt.Printf("Load time                             (%10s)\n", time.Since(clock))
	clock = time.Now()
	fmt.Printf("Part1 - example  %20d (%10s)\n", part1(example), time.Since(clock))
	clock = time.Now()
	fmt.Printf("Part1 - solution %20d (%10s)\n", part1(values), time.Since(clock))
	clock = time.Now()
	fmt.Printf("Part2 - example  %20d (%10s)\n", part2(example), time.Since(clock))
	clock = time.Now()
	fmt.Printf("Part2 - solution %20d (%10s)\n", part2(values), time.Since(clock))
}

func part1(G Digraph) int {
	var visited map[Vertex]bool
	queue := make([]Vertex, 0)
	score := 0
	for _, start := range G.starts {
		queue = queue[:0]
		visited = make(map[Vertex]bool)
		queue = append(queue, start)
		qidx := 0
		var v, w Vertex
		visited[start] = true
		for qidx < len(queue) {
			v = queue[qidx]
			for _, w = range G.arcs[v] {
				if !visited[w] {
					queue = append(queue, w)
				}
				visited[w] = true
			}
			if G.value[v] == 9 {
				score += 1
			}
			qidx++
		}
	}
	return score
}

func part2(G Digraph) int {
	howmany := make(map[Vertex]int)
	queue := make([]Vertex, 0)
	S := Vertex{-1, -2}
	G.arcs[S] = G.starts
	T := Vertex{-2, -2}
	for _, v := range G.ends {
		G.arcs[v] = append(G.arcs[v], T)
	}
	queue = append(queue, S)
	qidx := 0
	howmany[S] = 1
	var v, w Vertex
	for qidx < len(queue) {
		v = queue[qidx]
		for _, w = range G.arcs[v] {
			if howmany[w] == 0 {
				queue = append(queue, w)
			}
			howmany[w] += howmany[v]
		}
		qidx++
	}
	return howmany[T]
}
