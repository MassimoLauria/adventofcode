#include <iostream>
#include <sstream>
#include <fstream>

#include <vector>
#include <string>
#include <cstdlib>

#include <unordered_set>
#include <unordered_map>


using namespace std;

// Useful functions for the Advent of Code in C++

// Load file content into a string
const string load_file_content(string& filename) {
    ifstream  input {filename};
    if (!input) {
        cerr<<"Unable to open "<<filename<<endl;
        exit(-1);
    }
    ostringstream sstr;
    sstr << input.rdbuf();
    return sstr.str();
}

vector<int> get_all_integers(const string& t) {
    vector<int> V;
    int tmp  = 0;
    int sign = 1;
    int i    = 0;
    bool processing_number = false;
    bool is_digit = false;
    while(i<t.length()) {
        is_digit = ('0'<= t[i] and t[i]<='9');
        if (is_digit) processing_number = true;

        if (processing_number and is_digit) { // add digit
            tmp = tmp*10 + t[i]-'0';
            i += 1;
        }
        else if (processing_number) { // stop adding digits
            V.push_back(sign*tmp);
            processing_number = false;
            sign = +1;
            tmp = 0;
            continue;
        } else {                      // discard char (maybe update sign)
            sign = (t[i]=='-')? -1 : +1;
            i += 1;
        }
    }
    if (processing_number) V.push_back(sign*tmp);
    return std::move(V);
}

vector<string> splitlines(const string& sentence,bool empty_lines=false) {
  stringstream ss(sentence);
  string line;
  vector<string> lines;
  while(std::getline(ss,line,'\n')){
      if (line.length()!=0 or empty_lines) {
          lines.push_back(line);
      }
  }

  return std::move(lines);
}

vector<string> splittokens(const string& sentence) {
  stringstream ss(sentence);
  string token;
  vector<string> tokens;
  while(ss >> token){
      tokens.push_back(token);
  }
  return std::move(tokens);
}

// Dictionaries and set of tuples
//
// Using hash function in
// https://stackoverflow.com/questions/20511347/a-good-hash-function-for-a-vector/
//
template <typename T, size_t N> struct std::hash<std::array<T, N>> {
    inline size_t operator()(const std::array<T, N> &v) const {
        std::hash<T> d_hasher;
        std::size_t seed = N;
        for(auto& i : v) {
            seed ^= d_hasher(i) + 0x9e3779b9 + (seed << 6) + (seed >> 2);
        }
        return seed;
    }
};

// A set of tuples of length N of type T
template <typename T, size_t N>
using aoc_set = unordered_set<std::array<T,N>>;

// A dictonary that maps tuples of length N of type I and produces output of
// type O
template <typename I, size_t N, typename O>
using aoc_dict = unordered_map<std::array<I,N>,O>;
