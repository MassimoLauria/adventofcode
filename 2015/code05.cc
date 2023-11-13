/* -*- mode: C++; compile-command: "g++ -s -O3 code05.cc -o code05; ./code05" -*- */

// Get the data
#include <iostream>
#include <sstream>
#include <fstream>

#include <vector>
#include <string>
#include <unordered_set>
#include <unordered_map>

/* utils.h provides
   - load_file_content: loads a text file into a string
   - get_all_integers: parses all integers in text into a vector<int>,
                       and ignores other non digit characters
   - splitlines : split text into lines, produces a vector<string>
   - splittokens: split text into tokens, produces a vector<string>

   - aoc_set<T,N>   : A set of tuples of length N of type T

   - aoc_dict<I,N,O>: A dictonary that maps tuples of length N of type I and
                      produces output of type O
*/
#include "utils.h"


using namespace std;

// Data
string EXAMPLE {R"~(
)~"};

string INPUTFILE="input05.txt";


void part1(const string& text) {
    cout<<"part1"<<endl;
    vector<string> lines=splitlines(text);
    int nice=0;
    string vowels = "aeiou";
    for (auto &line: lines) {
        int  cvow=0;
        bool twice=false;
        bool forbid=false;
        // count vowels
        for(auto c : line) {
            if (vowels.find(c) != string::npos) { cvow += 1; }
        }
        // double char
        for(int i=1; i < line.size(); i++) {
            if (line[i-1]==line[i]) { twice = true; }
        }
        // forbidden pairs
        if (line.find("ab")!=string::npos) { forbid=true;}
        if (line.find("cd")!=string::npos) { forbid=true;}
        if (line.find("pq")!=string::npos) { forbid=true;}
        if (line.find("xy")!=string::npos) { forbid=true;}
        if ((not forbid) and twice and (cvow>=3)) nice+=1;
    }
    cout<<nice<<endl;
}

size_t findpair(const string& line) {
    for(int i=0; i < line.size()-3; i++) {
        for (int j=i+2; j < line.size()-1; j++) {
            if (line[i]!=line[j]) continue;
            if (line[i+1]==line[j+1]) { return i;}
        }
    }
    return string::npos;
}

void part2(const string& text) {
    cout<<"part2"<<endl;
    vector<string> lines=splitlines(text);
    int nice=0;
    for (auto &line: lines) {
        bool xyx=false;
        // xyx pattern
        for(int i=2; i < line.size(); i++) {
            if (line[i-2]==line[i]) { xyx = true; }
        }
        // xy xy pattern
        auto pair = findpair(line);
        if (xyx and pair!=string::npos) nice+=1;
    }
    cout<<nice<<endl;
}

int main () {
    cout<<"Advent of code 2023 day 13"<<endl;

    // part1 - input file
    auto text = load_file_content(INPUTFILE);
    part1(text);
    // part2 - input file
    part2(text);

    return 0;
}
