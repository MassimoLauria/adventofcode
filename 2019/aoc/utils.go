package aoc

import (
	"io/ioutil"
	"log"
	"regexp"
	"strconv"
)

func AllNumbersInString(data string) []int {
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

func AllNumbersInFile(filename string) []int {
	data, err := ioutil.ReadFile(filename)
	if err != nil {
		log.Fatal(err)
	}
	return AllNumbersInString(string(data))
}
