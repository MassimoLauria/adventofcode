/* -*- mode: C++; compile-command: "g++ -s -O3 code09.cc -o code09; ./code09" -*- */

// Get the data
#include <cmath>
#include <iostream>
#include <sstream>
#include <fstream>

#include <vector>
#include <string>
#include <unordered_set>
#include <utility>

using namespace std;

typedef pair<int, int> pairs;

// Data
string EXAMPLE {R"~(
R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2
)~"};

string EXAMPLE2 {R"~(
R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20
)~"};

string INPUTFILE="input09.txt";

inline bool touch(int x1, int y1, int x2, int y2) {
    return ( abs(x1-x2)<=1 and abs(y1-y2)<=1 );
}

inline pair<int,int> follow(int xt, int yt, int xh, int yh) {
    // assume they do not touch
    int xn,yn;
    int deltax,deltay;
    deltax = (xh > xt) ? 1 : ((xh < xt) ? -1 : 0);
    deltay = (yh > yt) ? 1 : ((yh < yt) ? -1 : 0);
    xn = xt + deltax;
    yn = yt + deltay;
    // printf("D=(%d,%d) H=(%d,%d) T=(%d,%d)\n",deltax,deltay,xh,yh,xt,yt);
    return std::move(make_pair(xn,yn));
}


// void part1(istream& input) {
//     int xh,yh,xt,yt; // head and tail
//     char dir;        // where to go
//     int  dst;        // how far
//     xh=xt=yh=yt=0;
//     int i;
//     unordered_set<int> visited {};
//     while (true) {
//         input >> dir;
//         input >> dst;
//         if (input.fail()) break;
//         // cout<<"Move: "<<dir<<" "<<dst<<endl;
//         for(i=0;i<dst;i++) {
//             if (dir=='L') {xh -= 1;}
//             if (dir=='R') {xh += 1;}
//             if (dir=='D') {yh -= 1;}
//             if (dir=='U') {yh += 1;}
//             if (!touch(xt,yt,xh,yh)) {
//                 auto p = follow(xt, yt, xh, yh);
//                 xt=p.first;
//                 yt=p.second;
//                 //cout<<"Head: "<<xh<<","<<yh<<" Tail: "<<xt<<","<<yt<<endl;
//             }
//             visited.insert(1000*xt + 500 + yt);
//         }
//     }
//     cout<<"part1: "<<visited.size()<<endl;
// }

// void draw_windows(int lx,int ly,int hx, int hy,
//                   vector<int> &X, vector<int> &Y,
//                   unordered_set<int> & visited) {
//     int i,j;
//     for(i=hy;i>=ly;i--) {
//         for(j=lx;j<=hx;j++) {
//             cout<<".";
//         }
//         cout<<endl;
//     }
// }

int tail_visited(istream& input,int ropelength) {
    int L = ropelength;
    vector<int> X(L,0); // rope nodes
    vector<int> Y(L,0); // rope nodes
    char dir;        // where to go
    int  dst;        // how far
    int i;
    int r;
    unordered_set<int> visited {};
    while (true) {
        input >> dir;
        input >> dst;
        if (input.fail()) break;
        for(i=0;i<dst;i++) {
            if (dir=='L') {X[0] -= 1; }
            if (dir=='R') {X[0] += 1; }
            if (dir=='D') {Y[0] -= 1; }
            if (dir=='U') {Y[0] += 1; }
            // propagate
            r = 1;
            while (r<L and !touch(X[r],Y[r],X[r-1],Y[r-1])) {
                auto p = follow(X[r],Y[r],X[r-1],Y[r-1]);
                X[r] = p.first;
                Y[r] = p.second;
                r++;
            }
            visited.insert(1000*X[L-1] + 500 + Y[L-1]);
        }
    }
    return visited.size();
}


void part1(istream& input) {
    cout<<"part1: "<<tail_visited(input, 2)<<endl;
}

void part2(istream& input) {
    cout<<"part2: "<<tail_visited(input, 10)<<endl;
}

int main () {
    cout<<"Advent of code 2022 day 09"<<endl;

    istringstream example1 {EXAMPLE} ;
    istringstream example2a {EXAMPLE} ;
    istringstream example2b {EXAMPLE2} ;
    ifstream  input1 {INPUTFILE};
    if (!input1) {
        cerr<<"Unable to open "<<INPUTFILE<<endl;
        return -1;
    }
    ifstream  input2 {INPUTFILE};
    if (!input2) {
        cerr<<"Unable to open "<<INPUTFILE<<endl;
        return -1;
    }

    part1(example1);
    part1(input1);
    part2(example2a);
    part2(example2b);
    part2(input2);

    return 0;
}
