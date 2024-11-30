package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"strings"
)

func get_all_strings(filename string) []string {
	data, err := ioutil.ReadFile(filename)
	if err != nil {
		fmt.Println("File not found")
		os.Exit(1)
	}
	strings := strings.Split(string(data),"\n")
	n := len(strings)
	if len(strings[n-1])==0 {
		return strings[:n-1]
	} else {
		return strings
	}
}

func main() {
	lines := get_all_strings("input08.txt")
	fmt.Println(part1(lines))
	fmt.Println(part2(lines))
}


func part1(lines []string) int {
	total := 0

	for _,s := range lines {
		n := len(s)
		total += n
		str_cnt := 0
		// count the length of the actual string
		i:=1
		for i < n - 1 {
			str_cnt += 1
			if s[i]=='\\' {
				if s[i+1]=='\\' || s[i+1]=='"' {
					i += 1
				} else {
					i += 3
				}
			}
			i+=1
		}
		total -= str_cnt
	}
	return total
}

func encoded_length(text string) int {
	length := 2
	for _,c:= range text {
		if  c == '"'  { length += 1  }
		if  c == '\\' { length += 1  }
		length += 1
	}
	return length
}

func part2(lines []string) int {
	total := 0

	for _,s := range lines {
		total += encoded_length(s) - len(s)
	}
	return total
}
