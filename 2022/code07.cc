/* -*- mode: C++; compile-command: "g++ -s -O3 code07.cc -o code07; ./code07" -*- */

// Get the data
#include <iostream>
#include <sstream>
#include <fstream>

#include <vector>
#include <string>
//#include <unordered_set>
#include <unordered_map>

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
    bool isfile;
    string name;
    int  size;
    fsnode *parent;
    vector<fsnode*> children;
};

fsnode* createfs(istream &input) {

    string line;
    fsnode *root = new fsnode { false, "/", 0, nullptr, {} };
    root->parent = root;

    fsnode *cwd = root;
    int size;
    string name;

    // Discard empty lines
    do { getline(input,line); } while (line.size()==0);

    while (line.size()!=0) {
        // cout<<"CWD: "<<cwd->name<<" "<<endl;
        // cout<<"LINE: "<<line<<endl;

        // directory move
        if (line.substr(0,5)!="$ cd ") {
            cerr<<"Something wrong..."<<endl;
            exit(1);
        }
        if (line.substr(5,2)=="..") { // go up
            cwd = cwd->parent;
            getline(input,line);
            continue;
        }
        // move to a subdirectory
        string newdir = line.substr(5);
        int it=0;
        if (newdir!="/") {
            it=0;
            while (it < cwd->children.size() ) {
                if (cwd->children[it]->name==newdir) break;
                it += 1;
            }
            if (it == cwd->children.size()) {
                cerr<<"Folder "<<newdir<<" do not exist"<<endl;
                cerr<<newdir<<endl;
                exit(1);
            }
            if (cwd->children[it]->isfile) {
                cerr<<"Target "<<newdir<<" is a file"<<endl;
                exit(1);
            }
            cwd = cwd->children[it];
        }

        getline(input,line);
        if (line!="$ ls") {
            cerr<<"Change dir not followed by ls"<<endl;
            exit(1);
        }
        getline(input,line);
        // Load children
        do {
            // cout<<"CHILD: "<<line<<endl;
            fsnode *newobj = new fsnode{ false, "", 0, cwd, {}};
            if (line.substr(0,4)=="dir ") {
                name = line.substr(4);
                newobj -> name = name;
            } else {
                int i=0;
                for (i=0;i<line.size();i++){
                    if (line[i]==' ') break;
                }
                newobj -> isfile = true;
                newobj -> size = stoi(line.substr(0,i));
                newobj -> name = line.substr(i+1);
            }
            cwd->children.push_back(newobj);
            getline(input,line);
        } while (line.size()!=0 and line[0]!='$');
    }
    return root;
}

int collect_small_size(fsnode *ptr) {
    if (ptr->isfile) return 0;

    int total_size = 0;
    int small_sum = 0;
    for (auto *c: ptr->children) {
        small_sum += collect_small_size(c);
    }
    for (auto *c: ptr->children) {
        total_size += c->size;
    }
    ptr->size = total_size;
    if (total_size<=100000) {
        small_sum += total_size;
    }
    return small_sum;
}

int find_smallest_atleast(fsnode *ptr, int lower_bound) {
    if (ptr->isfile) return -1;

    if (ptr->size < lower_bound) return -1;

    int candidate = ptr->size;
    int tmp=0;
    for (auto *c: ptr->children) {
        tmp = find_smallest_atleast(c, lower_bound);
        if (tmp==-1) continue;
        if (tmp<candidate) candidate = tmp;
    }
    return candidate;
}

void part1(fsnode * root) {
    int x = collect_small_size(root);
    cout<<"part1: "<<x<<endl;
}

void part2(fsnode * root) {
    int sol = find_smallest_atleast(root, root->size - 40000000);
    cout<<"part2: "<<sol<<endl;
}

int main () {
    cout<<"Advent of code 2022 day 07"<<endl;

    // part1 - example data
    istringstream example {EXAMPLE} ;
    auto root_example = createfs(example);
    part1(root_example);

    // part1 - input file
    ifstream  input {INPUTFILE};
    if (!input) {
        cerr<<"Unable to open "<<INPUTFILE<<endl;
        return -1;
    }
    auto root_input = createfs(input);
    part1(root_input);

    // part2 - example data
    part2(root_example);
    part2(root_input);

    return 0;
}
