/* -*- mode: C++; compile-command: "g++ -s -O3 code06.cc -o code06" -*- */

// Get the data
#include <iostream>
#include <sstream>
#include <fstream>
#include<iterator>

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

string INPUTFILE="input06.txt";

enum { OFF, ON, TOGGLE};

vector<int> commands(const string& text) {
    auto lines = splitlines(text);
    auto values = get_all_integers(text);
    int N = lines.size();
    vector<int> cmds(5*N);
    for (int i=0;i<N;i++) {
        if (lines[i].find("toggle")!=string::npos) {
            cmds[5*i] = TOGGLE;
        } else if (lines[i].find("turn off")!=string::npos) {
            cmds[5*i] = OFF;
        } else {
            cmds[5*i] = ON;
        }
        cmds[5*i+1] = values[4*i+0];
        cmds[5*i+2] = values[4*i+1];
        cmds[5*i+3] = values[4*i+2];
        cmds[5*i+4] = values[4*i+3];
    }
    return move(cmds);
}


void part1(const string& text) {
    cout<<"part1"<<endl;
    auto cmds = commands(text);
    int N = cmds.size();
    int lights_on=0;
    bool on=false;
    for(int i=0;i<1000;i++) {
        for(int j=0;j<1000;j++) {
            on = false;
            for (int k=0; k<N; k+=5) {
                if ( i < cmds[k+1] or
                     j < cmds[k+2] or
                     i > cmds[k+3] or
                     j > cmds[k+4] ) continue;
                if (cmds[k]==ON){
                    on = true;
                } else if (cmds[k]==OFF) {
                    on = false;
                } else {
                    on = not on;
                }
            }
            lights_on += on;
        }
    }
    cout<<lights_on<<endl;
}

void part2(const string& text) {
    cout<<"part2"<<endl;
    auto cmds = commands(text);
    int N = cmds.size();
    int lights_on=0;
    int bright=0;
    for(int i=0;i<1000;i++) {
        for(int j=0;j<1000;j++) {
            bright = 0;
            for (int k=0; k<N; k+=5) {
                if ( i < cmds[k+1] or
                     j < cmds[k+2] or
                     i > cmds[k+3] or
                     j > cmds[k+4] ) continue;
                if (cmds[k]==ON){
                    bright += 1;
                } else if (cmds[k]==OFF) {
                    bright = max(0,bright-1);
                } else {
                    bright += 2;
                }
            }
            lights_on += bright;
        }
    }
    cout<<lights_on<<endl;
}

int main () {
    cout<<"Advent of code 2023 day 13"<<endl;

    // part1 - input file
    auto text = load_file_content(INPUTFILE);
    part1(text);

    // part2 - example data
    // part2(EXAMPLE);

    // part2 - input file
    part2(text);

    return 0;
}
