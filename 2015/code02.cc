/* -*- mode: C++; compile-command: "g++ -s -O3 code02.cc -o code02; ./code02" -*- */

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
)~"};

string INPUTFILE="input02.txt";

std::string slurp(std::ifstream& in) {
    std::ostringstream sstr;
    sstr << in.rdbuf();
    return sstr.str();
}


int main () {
    cout<<"Advent of code 2015 day 02"<<endl;

    // part1 - input file
    ifstream  input {INPUTFILE};
    if (!input) {
        cerr<<"Unable to open "<<INPUTFILE<<endl;
        return -1;
    }

    auto text = slurp(input);
    vector<int> V;
    // Clean up
    int x=0;
    for(auto c : text) {
        if ('0'<= c and c<='9') {
            x = x*10 + c-'0';
        } else if (x>0) {
            V.push_back(x);
            x = 0;
        } else {
            x = 0;
        }
    }
    if (x>0) {
        V.push_back(x);
        x = -1;
    }

    for(auto x : V) {
        cout<<x<<endl;
    }
    // part2 - example data
    //part2(root_example);
    //part2(root_input);

    return 0;
}
