// Advent of Code 2024 day 17
//
// Massimo Lauria

package main

import (
	"fmt"
	"io/ioutil"
	"log"
	"regexp"
	"strconv"
	"strings"
	"time"
)

const example = `Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0`

func getAllNumbers(data string) []int {
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

func main() {
	example := getAllNumbers(example)
	clock := time.Now()
	data, err := ioutil.ReadFile("input17.txt")
	if err != nil {
		log.Fatal(err)
	}
	challenge := getAllNumbers(string(data))
	fmt.Printf("Load time                                     - %s\n", time.Since(clock))
	clock = time.Now()
	fmt.Printf("Part1 - example   : %-25s - %s\n", part1(example), time.Since(clock))
	clock = time.Now()
	fmt.Printf("Part1 - challenge : %-25s - %s\n", part1(challenge), time.Since(clock))
	clock = time.Now()
	fmt.Printf("Part2 - challenge : %-25d - %s\n", part2(challenge), time.Since(clock))
}

const (
	ADV = iota
	BXL
	BST
	JNZ
	BXC
	OUT
	BDV
	CDV
)

func run(m *Machine, prg []int) {
	A := m.A
	B := m.B
	C := m.C
	ip := 0
	var output []int
	combo := func(ip int) int {
		switch prg[ip] {
		case 0, 1, 2, 3:
			return prg[ip]
		case 4:
			return A
		case 5:
			return B
		case 6:
			return C
		default:
			log.Fatalf("Invalid combo spec at ip=%d\n", ip)
		}
		return 0
	}
	var tmp int
	for ip < len(prg) {
		switch prg[ip] {
		case ADV:
			A = A >> combo(ip+1)
		case BDV:
			B = A >> combo(ip+1)
		case CDV:
			C = A >> combo(ip+1)
		case JNZ:
			if A != 0 {
				ip = prg[ip+1]
				continue
			}
		case OUT:
			tmp = combo(ip+1) % 8
			output = append(output, tmp)
		case BXL:
			B = B ^ prg[ip+1]
		case BXC:
			B = B ^ C
		case BST:
			B = combo(ip+1) % 8
		default:
			log.Fatalf("Invalid instruction at ip=%d\n", ip)
		}
		ip += 2
	}
	m.A, m.B, m.C = A, B, C
	m.output = output
	// fmt.Println("A", A, "B", B, "C", C, output)
}

type Machine struct {
	A, B, C int
	output  []int
}

func part1(values []int) string {
	m := Machine{A: values[0], B: values[1], C: values[2]}
	prg := values[3:]
	run(&m, prg)
	var soutput []string
	for _, v := range m.output {
		soutput = append(soutput, strconv.Itoa(v))
	}
	return strings.Join(soutput, ",")
}

func solve(prefix int, prg []int, guessIdx int) (int, bool) {
	m := Machine{}
	for a := prefix * 8; a < prefix*8+8; a++ {
		m.A = a
		run(&m, prg[:12]) // do not output or jump (just read B register)
		if m.B%8 == prg[guessIdx] {
			if guessIdx == 0 {
				return a, true
			} else if v, ok := solve(a, prg, guessIdx-1); ok {
				return v, ok
			}
		}
	}
	return 0, false
}

func part2(values []int) int {
	prg := values[3:]
	v, ok := solve(0, prg, len(prg)-1)
	if !ok {
		return 0
	}
	return v
}

func disassm(prg []int) {
	combo := func(ip int) string {
		switch prg[ip] {
		case 0, 1, 2, 3:
			return strconv.Itoa(prg[ip])
		case 4:
			return "A"
		case 5:
			return "B"
		case 6:
			return "C"
		default:
			log.Fatalf("Invalid combo spec at ip=%d\n", ip)
		}
		return ""
	}
	ip := 0
	for ip < len(prg) {
		fmt.Printf("%2d:  ", ip)
		switch prg[ip] {
		case ADV:
			fmt.Printf("A = A >> %s", combo(ip+1))
		case BDV:
			fmt.Printf("B = A >> %s", combo(ip+1))
		case CDV:
			fmt.Printf("C = A >> %s", combo(ip+1))
		case JNZ:
			fmt.Printf("if A!= 0 goto %d", prg[ip+1])
		case OUT:
			fmt.Printf("output %s %% 8", combo(ip+1))
		case BXL:
			fmt.Printf("B = B ^ %d", prg[ip+1])
		case BXC:
			fmt.Printf("B = B ^ C")
		case BST:
			fmt.Printf("B = %s %% 8", combo(ip+1))
		default:
			log.Fatalf("Invalid instruction at ip=%d\n", ip)
		}
		fmt.Println()
		ip += 2
	}
}
