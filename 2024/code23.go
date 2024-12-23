// Advent of Code 2024 day 23
//
// Massimo Lauria

package main

import (
	"bytes"
	"fmt"
	"io/ioutil"
	"log"
	"slices"
	"strings"
	"time"
)

const example = `
kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn
`

func main() {
	example := processText([]byte(example))
	clock := time.Now()
	data, err := ioutil.ReadFile("input23.txt")
	if err != nil {
		log.Fatal(err)
	}
	challenge := processText(data)
	fmt.Printf("Load time                                     - %s\n", time.Since(clock))
	clock = time.Now()
	fmt.Printf("Part1 - example   : %-25d - %s\n", part1(example), time.Since(clock))
	clock = time.Now()
	fmt.Printf("Part1 - challenge : %-25d - %s\n", part1(challenge), time.Since(clock))
	clock = time.Now()
	fmt.Printf("Part2 - example   : %-25s - %s\n", part2(example), time.Since(clock))
	clock = time.Now()
	fmt.Printf("Part2 - challenge : %-25s - %s\n", part2(challenge), time.Since(clock))
}

type Graph map[string]map[string]bool

func processText(data []byte) Graph {
	G := make(Graph)
	data = bytes.TrimSpace(data)
	lines := bytes.Split(data, []byte("\n"))
	var a, b string
	for _, line := range lines {
		a, b = string(line[0:2]), string(line[3:5])
		if _, ok := G[a]; !ok {
			G[a] = make(map[string]bool)
		}
		if _, ok := G[b]; !ok {
			G[b] = make(map[string]bool)
		}
		G[a][b] = true
		G[b][a] = true
	}
	return G
}

func part1(G Graph) int {
	triangles := 0
	for v, neigh := range G {
		if v[0] != 't' {
			continue
		}
		ijs := make([]string, len(neigh))
		i := 0
		for w, _ := range neigh {
			ijs[i] = w
			i++
		}
		for i = 0; i < len(ijs)-1; i++ {
			for j := i + 1; j < len(ijs); j++ {
				if G[ijs[i]][ijs[j]] {
					switch {
					case ijs[i][0] == 't' && ijs[j][0] == 't':
						triangles += 2 // we are counting it 3 times
					case ijs[i][0] == 't' || ijs[j][0] == 't':
						triangles += 3 // we are counting it 2 times
					default:
						triangles += 6 // we are counting it 2 times
					}
				}
			}
		}
	}
	return triangles / 6
}

func MaxClique(V []string, E Graph) []string {
	return V[:10]
}

func part2(G Graph) string {
	V := make([]string, 0, len(G))
	for v, _ := range G {
		V = append(V, v)
	}
	K := MaxClique(V, G)
	slices.Sort(K)
	return strings.Join(K, ",")
}
