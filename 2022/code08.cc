/* -*- mode: C++; compile-command: "g++ -s -O3 code08.cc -o code08; ./code08" -*- */

// Get the data
#include <algorithm>
#include <iostream>
#include <sstream>
#include <fstream>

#include <vector>
#include <string>
#include <numeric>
//#include <unordered_set>
//#include <unordered_map>

using namespace std;

// Data
string EXAMPLE {R"~(
30373
25512
65332
33549
35390
)~"};

string INPUTFILE="input08.txt";

vector<vector<int>> load_grid(istream& input) {
    string line;
    vector<vector<int>> grid;
    getline(input,line);
    int i,j;
    if (line.size()==0) getline(input,line);
    while (line.size()!=0) {
        vector<int> V;
        for(i=0;i<line.size();i++) {
            V.push_back( line[i]-'0' );
        }
        grid.emplace_back(V);
        getline(input,line);
    }
    return std::move(grid);
}

vector<vector<int>> make_grid(int R, int C, int fill) {
    vector<vector<int>> grid;
    int i,j;
    for(i=0;i<R;i++) {
        vector<int> V(C,fill);
        grid.emplace_back(V);
    }
    return std::move(grid);
}

void print_grid(vector<vector<int>> &grid) {
    int R = grid.size();
    int C = grid[0].size();
    int i,j;
    for(i=0;i<R;i++) {
        for(j=0;j<C;j++) {
            cout<<grid[i][j];
        }
        cout<<endl;
    }
}

void part1(vector<vector<int>> grid) {
    int R = grid.size();
    int C = grid[0].size();
    int i,j;
    int max_height;
    auto visible = make_grid(R,C,0);
    visible[0][0]     = 1;
    visible[0][C-1]   = 1;
    visible[R-1][0]   = 1;
    visible[R-1][C-1] = 1;
    // Top and bottom
    for(j=1;j<C-1;j++) {
        visible[0][j]   = 1;
        max_height = grid[0][j];
        for (i=1;i<R-1;i++) {
            if (grid[i][j] > max_height) {
                visible[i][j] = 1;
                max_height = grid[i][j];
            }
        }
        visible[R-1][j]   = 1;
        max_height = grid[R-1][j];
        for (i=R-2;i>0;i--) {
            if (grid[i][j] > max_height) {
                visible[i][j] = 1;
                max_height = grid[i][j];
            }
        }
    }
    // Left and right
    for(i=1;i<R-1;i++) {
        visible[i][0]   = 1;
        max_height = grid[i][0];
        for (j=1;j<C-1;j++) {
            if (grid[i][j] > max_height) {
                visible[i][j] = 1;
                max_height = grid[i][j];
            }
        }
        visible[i][C-1]   = 1;
        max_height = grid[i][C-1];
        for (j=C-2;j>0;j--) {
            if (grid[i][j] > max_height) {
                visible[i][j] = 1;
                max_height = grid[i][j];
            }
        }
    }
    // print_grid(visible);
    int sum = 0;
    for(i=0;i<R;i++) {
        sum = accumulate(visible[i].begin(),visible[i].end(),sum);
    }
    cout<<"part1: "<<sum<<endl;
}

void part2(vector<vector<int>> grid) {
    int R = grid.size();
    int C = grid[0].size();
    auto score = make_grid(R, C, 0);
    int i,j,k,up,down,left,right;
    int height;
    int max_score = 0;
    for(i=1;i<R-1;i++) {
        for(j=1;j<C-1;j++) {
            height = grid[i][j];
            left = right = up = down = 1;
            k = j-1;
            while (k>0  and grid[i][k]<height) { left++; k--; }
            k = j+1;
            while (k<R-1   and grid[i][k]<height) { right++; k++; }
            k = i-1;
            while (k>0  and grid[k][j]<height) { up++; k--; }
            k = i+1;
            while (k<C-1   and grid[k][j]<height) { down++; k++; }
            score[i][j]= up*down*left*right;
            max_score = max(score[i][j],max_score);
        }
    }
    //print_grid(score);
    cout<<"part2: "<<max_score<<endl;
}

int main () {
    cout<<"Advent of code 2022 day 08"<<endl;
    // load data
    istringstream example {EXAMPLE} ;
    ifstream  input {INPUTFILE};
    if (!input) {
        cerr<<"Unable to open "<<INPUTFILE<<endl;
        return -1;
    }
    vector<vector<int>> grid_example = load_grid(example);
    vector<vector<int>> grid_input   = load_grid(input);

    // part1
    part1(grid_example);
    part1(grid_input);

    // part2 - input file
    part2(grid_example);
    part2(grid_input);

    return 0;
}
