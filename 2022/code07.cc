/* -*- mode: C++; compile-command: "g++ -s -O3 code07.cc -o code07; ./code07" -*- */

// Get the data
#include <iostream>
#include <sstream>
#include <fstream>

//#include <vector>
//#include <string>
//#include <unordered_set>
//#include <unordered_map>

using namespace std;

// Data
string EXAMPLE {R"~(
)~"};

string INPUTFILE="input07.txt";


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
