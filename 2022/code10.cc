/* -*- mode: C++; compile-command: "g++ -s -O3 code10.cc -o code10; ./code10" -*- */

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
addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop
)~"};

string INPUTFILE="input10.txt";

vector<int> X_history(istream& input) {
    vector <int> data;
    string tmp;
    int tvalue;
    input >> tmp;
    while (!input.fail()) {
        if (tmp[0]=='n') data.push_back(0);
        else if (tmp[0]=='a') {
            data.push_back(0);
            input>>tvalue;
            data.push_back(tvalue);
        }
        input >> tmp;
    }
    // propagate X
    vector <int> X(data.size()+1);
    X[0]=1; // start value
    for (int i=1;i<X.size();i++) {
        X[i] = X[i-1] + data[i-1];
    }
    return std::move(X);
}


void part1(istream& input) {
    cout<<"part1: ";
    vector<int> samples = {20,60,100,140,180,220};
    int result = 0;
    auto X = X_history(input);
    for(auto s:samples) {
        result += s*X[s-1];
    }
    cout<<result<<endl;
}

void print_screen(vector<char> &screen) {
    for(int r=0;r<6;r++) {
        for(int c=0;c<40;c++) cout<<screen[40*r+c];
        cout<<endl;
    }

}

void part2(istream& input) {
    cout<<"part2"<<endl;
    int width = 40;
    int height = 6;
    vector<char> screen(240,'.');
    auto X = X_history(input);
    cout<<X.size()<<endl;
    for(auto i: X) {
        cout<<i<<" ";
    }
    cout<<endl;
    for(int i;i<240;i++) {
        int sp = X[i] % 40;
        int px = i % 40;
        if (abs(sp-px) <= 1) {
            screen[i]='#';
        }
    }
    print_screen(screen);
}

int main () {
    cout<<"Advent of code 2022 day 10"<<endl;

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
    istringstream p2example(EXAMPLE);
    part2(p2example);
    // part2 - input file
    ifstream  input2 {INPUTFILE};
    if (!input2) {
        cerr<<"Unable to open "<<INPUTFILE<<endl;
        return -1;
    }
    part2(input2);

    return 0;
}
