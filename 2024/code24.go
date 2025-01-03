// Advent of Code 2024 day 24
//
// Massimo Lauria

package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"slices"
	"strconv"
	"strings"
	"time"
)

const example = `
x00: 1
x01: 0
x02: 1
x03: 1
x04: 0
y00: 1
y01: 1
y02: 1
y03: 1
y04: 1

ntg XOR fgs -> mjb
y02 OR x01 -> tnw
kwq OR kpj -> z05
x00 OR x03 -> fst
tgd XOR rvg -> z01
vdt OR tnw -> bfw
bfw AND frj -> z10
ffh OR nrd -> bqk
y00 AND y03 -> djm
y03 OR y00 -> psh
bqk OR frj -> z08
tnw OR fst -> frj
gnj AND tgd -> z11
bfw XOR mjb -> z00
x03 OR x00 -> vdt
gnj AND wpb -> z02
x04 AND y00 -> kjc
djm OR pbm -> qhw
nrd AND vdt -> hwm
kjc AND fst -> rvg
y04 OR y02 -> fgs
y01 AND x02 -> pbm
ntg OR kjc -> kwq
psh XOR fgs -> tgd
qhw XOR tgd -> z09
pbm OR djm -> kpj
x03 XOR y03 -> ffh
x00 XOR y04 -> ntg
bfw OR bqk -> z06
nrd XOR fgs -> wpb
frj XOR qhw -> z04
bqk OR frj -> z07
y03 OR x01 -> nrd
hwm AND bqk -> z03
tgd XOR rvg -> z12
tnw OR pbm -> gnj
`

func main() {
	example := processText(example)
	clock := time.Now()
	data, err := ioutil.ReadFile("input24.txt")
	if err != nil {
		log.Fatal(err)
	}
	challenge := processText(string(data))
	fmt.Printf("Load time                                     - %s\n", time.Since(clock))
	clock = time.Now()
	fmt.Printf("Part1 - example   : %-25d - %s\n", part1(example), time.Since(clock))
	clock = time.Now()
	fmt.Printf("Part1 - challenge : %-25d - %s\n", part1(challenge), time.Since(clock))
	clock = time.Now()
	fmt.Printf("Part2 - challenge : %-25s - %s\n", part2(challenge), time.Since(clock))
}

type Circuit struct {
	gates  map[string][3]string
	values map[string]bool
}

func processText(data string) Circuit {
	data = strings.TrimSpace(data)
	var C Circuit
	var gate []string
	C.values = make(map[string]bool)
	C.gates = make(map[string][3]string)
	lines := strings.Split(data, "\n")
	// load input
	i := 0
	for i = range lines {
		if len(lines[i]) == 0 {
			break
		}
		C.values[lines[i][0:3]] = (lines[i][5] == '1')
	}
	i++
	for ; i < len(lines); i++ {
		gate = strings.Fields(lines[i])
		C.gates[gate[4]] = [3]string{gate[0], gate[1], gate[2]}
	}
	return C
}

func getValue(C Circuit, name byte) int {
	n := 0
	// get output
	for g, b := range C.values {
		if g[0] == name && b {
			idx, _ := strconv.Atoi(g[1:3])
			n += 1 << idx
		}
	}
	return n
}

func recEval(C Circuit, g string) bool {
	if v, ok := C.values[g]; ok {
		return v
	}
	a := recEval(C, C.gates[g][0])
	b := recEval(C, C.gates[g][2])
	switch C.gates[g][1] {
	case "OR":
		C.values[g] = a || b
	case "AND":
		C.values[g] = a && b
	case "XOR":
		C.values[g] = (a != b)
	}
	v, _ := C.values[g]
	return v
}

func part1(C Circuit) int {
	for g, _ := range C.gates {
		recEval(C, g)
	}
	// get output
	n := 0
	for g, b := range C.values {
		if g[0] == 'z' && b {
			idx, _ := strconv.Atoi(g[1:3])
			n += 1 << idx
		}
	}
	return n
}

func xorand(C Circuit, gates []string) (string, string) {
	op0 := C.gates[gates[0]][1]
	op1 := C.gates[gates[1]][1]
	if op0 == "XOR" && op1 == "AND" {
		return gates[0], gates[1]
	} else if op1 == "XOR" && op0 == "AND" {
		return gates[1], gates[0]
	} else {
		log.Fatal("xor and not in the right place")
	}
	return "", ""
}

func part2(C Circuit) string {
	// cache successors of a gate
	swapped := make([]string, 0)
	succ := make(map[string][]string)
	for g, desc := range C.gates {
		succ[desc[0]] = append(succ[desc[0]], g)
		succ[desc[2]] = append(succ[desc[2]], g)
	}
	// count the number of inputs (i.e. size of the adder)
	n := 0
	for g, _ := range C.values {
		if g[0] == 'x' {
			n += 1
		}
	}
	// first carry
	_, carry := xorand(C, succ["x00"])
	for i := 1; i < n; i++ {
		xin := fmt.Sprintf("x%02d", i)
		zout := fmt.Sprintf("z%02d", i)
		xor1, and1 := xorand(C, succ[xin]) // The XOR and AND from input bits
		if len(succ[xor1]) == 1 && len(succ[and1]) == 2 {
			swapped = append(swapped, xor1)
			swapped = append(swapped, and1)
			carry = succ[xor1][0]
			continue
		}
		xor2, _ := xorand(C, succ[carry])
		if xor2 != zout {
			swapped = append(swapped, zout)
			swapped = append(swapped, xor2)
			if C.gates[zout][1] == "OR" {
				carry = xor2
			} else if zout == and1 {
				carry = succ[xor2][0]
			} else {
				carry = succ[and1][0]
			}
			continue
		}
		carry = succ[and1][0]
	}
	slices.Sort(swapped)
	return strings.Join(swapped, ",")
}

func printDotFile(C Circuit) {
	var inbits, outbits int
	for g, _ := range C.gates {
		if g[0] == 'z' {
			outbits += 1
		}
	}
	for g, _ := range C.values {
		if g[0] == 'x' {
			inbits += 1
		}
	}
	fmt.Println("digraph {")
	for i := 0; i < inbits; i++ {
		fmt.Printf("subgraph cluster_%02d {\n cluster=true;\n rankdir=LR;\n label=\"i%02d\"\n", i, i)
		fmt.Printf("x%02d\n", i)
		fmt.Printf("y%02d\n", i)
		fmt.Println("}\n")
	}
	fmt.Println("subgraph cluster_Z {\n cluster=true; rankdir=LR;\n label=\"Z\"\n")
	for i := 0; i < outbits; i++ {
		fmt.Printf("o%02d [label=\"z%02d\"]\n", i, i)
	}
	fmt.Println("}\n")
	fmt.Printf("\n")
	for i := 0; i < outbits; i++ {
		fmt.Printf("z%02d -> o%02d\n", i, i)
		fmt.Printf("o%02d [label=\"z%02d\"]\n", i, i)
	}
	for g, desc := range C.gates {
		fmt.Printf("{%s,%s} -> %s\n", desc[0], desc[2], g)
		fmt.Printf("%s [label=\"%s(%s)\"]\n", g, desc[1], g)
	}
	fmt.Printf("}\n")
}
