// Advent of Code 2024 day 05
//
// Massimo Lauria

package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"slices"
	"strconv"
	"strings"
)

var ToInt = strconv.Atoi

const example_data = `47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47`

func read_input_file(filename string) string {
	data, err := ioutil.ReadFile(filename)
	if err != nil {
		fmt.Fprintf(os.Stderr, "File %s not found\n", filename)
		os.Exit(1)
	}
	return string(data)
}

func process_text(data string) (map[[2]int]bool, [][]int) {
	lines := strings.Split(string(data), "\n")
	edges := make(map[[2]int]bool)
	var updates [][]int
	var a, b int
	i := 0
	for {
		_, err := fmt.Sscanf(lines[i], "%d|%d", &a, &b)
		i++
		if err != nil {
			break
		}
		edges[[2]int{a, b}] = true
	}
	for ; i < len(lines); i++ {
		updates = append(updates, nil)
		for _, s := range strings.Split(lines[i], ",") {
			a, _ = ToInt(s)
			updates[len(updates)-1] = append(updates[len(updates)-1], a)
		}
	}
	return edges, updates
}

func main() {
	data := read_input_file("input05.txt")
	eorder, eupdates := process_text(example_data)
	order, updates := process_text(data)
	fmt.Println("Part1 - example  ", part1(eorder, eupdates))
	fmt.Println("Part1 - solution ", part1(order, updates))
	fmt.Println("Part2 - example", part2(eorder, eupdates))
	fmt.Println("Part2 - solution ", part2(order, updates))
}

func correct_order(order_relation map[[2]int]bool, update []int) bool {
	ordered := true
	for i := 0; i < len(update)-1; i++ {
		ordered = ordered && order_relation[[2]int{update[i], update[i+1]}]
	}
	return ordered
}

func part1(order_relation map[[2]int]bool, updates [][]int) int {
	value := 0
	for _, update := range updates {
		if correct_order(order_relation, update) {
			value += update[len(update)/2]
		}
	}
	return value
}

func part2(order_relation map[[2]int]bool, updates [][]int) int {
	value := 0
	cmp := func(a, b int) int {
		ok := order_relation[[2]int{a, b}]
		if ok {
			return -1
		} else {
			return 1
		}
	}

	for _, update := range updates {
		if correct_order(order_relation, update) {
			continue
		}
		// sort the update
		slices.SortFunc(update, cmp)
		value += update[len(update)/2]
	}
	return value
}
