/* -*- mode: C++; compile-command: "g++ -s -O3 code03.cc -o code03; ./code03" -*- */

// Get the data
#include <iostream>
#include <sstream>
#include <fstream>

#include <vector>
#include <string>
#include <unordered_set>
#include <utility>
//#include <unordered_map>

/* utils.h provides
   - load_file_content: loads a text file into a string
   - get_all_integers: parses all integers in text into a vector<int>,
                       and ignores other non digit characters
   - splitlines: split text into lines, produces a vector<string>
   - splitlines: split text into tokens, produces a vector<string>
*/
#include "utils.h"


using namespace std;

// Data
string EXAMPLE {R"~(
)~"};

string INPUTFILE="input03.txt";

template <> struct std::hash<std::pair<int, int>> {
    inline size_t operator()(const std::pair<int, int> &v) const {
        std::hash<int> int_hasher;
        return int_hasher(v.first) ^ int_hasher(v.second);
    }
};

void part1(const string& text) {
    int x=0;
    int y=0;
    unordered_set< pair<int,int> > C;
    C.insert({x,y});
    for(int i=0;i<text.length();i++) {
        if (text[i]=='>') x += 1;
        else if (text[i]=='<') x -= 1;
        else if (text[i]=='^') y += 1;
        else if (text[i]=='v') y -= 1;
        C.insert({x,y});
    }
    cout<<"part1: "<< C.size()<<endl;
}

void part2(const string& text) {
    int x[2]={0,0};
    int y[2]={0,0};
    unordered_set< pair<int,int> > C;
    C.insert({x[0],y[0]});
    for(int i=0;i<text.length();i++) {
        if (text[i]=='>') x[i%2] += 1;
        else if (text[i]=='<') x[i%2] -= 1;
        else if (text[i]=='^') y[i%2] += 1;
        else if (text[i]=='v') y[i%2] -= 1;
        C.insert({x[i%2],y[i%2]});
    }
    cout<<"part2: "<< C.size()<<endl;
}

int main () {
    cout<<"Advent of code 2023 day 03"<<endl;

    // part1 - example data
    part1("^v^v^v^v^v");

    // part1 - input file
    auto text = load_file_content(INPUTFILE);
    part1(text);

    // part2 - example data
    part2("^v");
    part2("^>v<");
    part2("^v^v^v^v^v");

    // part2 - input file
    part2(text);

    return 0;
}
