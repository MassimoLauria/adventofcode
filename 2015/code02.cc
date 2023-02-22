/* -*- mode: C++; compile-command: "g++ -s -O3 code02.cc -o code02; ./code02" -*- */

// Get the data
#include <iostream>
#include <sstream>
#include <fstream>

#include <vector>
#include <string>
//#include <unordered_set>
//#include <unordered_map>

#include "utils.h"

using namespace std;

// Data
string EXAMPLE {R"~(
)~"};

string INPUTFILE="input02.txt";


void sortby3(vector<int> &V) {
    int t=0;
    for(int i=0;i<V.size();i+=3) {
        if (V[i]>V[i+1]) {t = V[i]; V[i] = V[i+1]; V[i+1]=t; }
        if (V[i+1]>V[i+2]) {t = V[i+1]; V[i+1] = V[i+2]; V[i+2]=t; }
    }
}

void part1(vector<int> &V) {
    int x,y,z,m;
    int s=0;
    for(int i=0;i<V.size();i+=3) {
        x = V[i];
        y = V[i+1];
        z = V[i+2];
        s += 2*x*y + 2*y*z + 2*x*z + x*y;
    }
    cout<<s<<endl;
}

void part2(vector<int> &V) {
    int x,y,z,m=0;
    int s=0;
    for(int i=0;i<V.size();i+=3) {
        x = V[i];
        y = V[i+1];
        z = V[i+2];
        s += 2*x+2*y + x*y*z;
    }
    cout<<s<<endl;
}


int main () {
    cout<<"Advent of code 2015 day 02"<<endl;

    // part1 - input file
    auto text = load_file_content(INPUTFILE);
    auto V = get_all_integers(text);
    sortby3(V);

    part1(V);
    part2(V);

    return 0;
}
