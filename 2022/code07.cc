/* -*- mode: C++; compile-command: "g++ -s -O3 code07.cc -o code07; ./code07" -*- */

// Get the data
#include <iostream>
#include <sstream>
#include <fstream>

#include <vector>
#include <string>
//#include <unordered_set>
//#include <unordered_map>

using namespace std;

// Data
string EXAMPLE {R"~(
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
)~"};

string INPUTFILE="input07.txt";

struct fsnode {
    bool isfile=false;
    int  size=0;
    string name;
    vector<fsnode*> children;
};

fsnode&& createfs(istream &input) {
    string line;
    for(int i=0; i<4;i++) {
        getline(input,line);
        if (line.size()==0) continue;
        cout<<line<<endl;
    }
    return {false,0,"/", vector<fsnode*> {} };
}

void part1(istream& input) {
    cout<<"part1"<<endl;
}

void part2(istream& input) {
    cout<<"part2"<<endl;
}

int main () {
    cout<<"Advent of code 2022 day 07"<<endl;

    // part1 - example data
    istringstream example {EXAMPLE} ;
    part1(example);
    createfs(example);
    // part2 - input file
    ifstream  input {INPUTFILE};
    if (!input) {
        cerr<<"Unable to open "<<INPUTFILE<<endl;
        return -1;
    }
    part1(input);

    // part2 - example data
    example.seekg(0);
    part2(example);
    // part2 - input file
    input.seekg(0);
    part2(input);

    return 0;
}
