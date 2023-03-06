/* -*- mode: C++; compile-command: "g++ -s -O3 code04.cc -o code04 -lcrypto; ./code04" -*- */

// Get the data
#include <iostream>
#include <sstream>
#include <fstream>

#include <vector>
#include <string>
#include <unordered_set>
#include <unordered_map>

/* utils.h provides
   - load_file_content: loads a text file into a string
   - get_all_integers: parses all integers in text into a vector<int>,
                       and ignores other non digit characters
   - splitlines: split text into lines, produces a vector<string>
   - splitlines: split text into tokens, produces a vector<string>

   - aoc_set<T,N>   : A set of tuples of length N of type T

   - aoc_dict<I,N,O>: A dictonary that maps tuples of length N of type I and
                      produces output of type O
*/
#include "utils.h"

#include <openssl/md5.h>

// Print the MD5 sum as hex-digits.
void print_md5_sum(unsigned char* md) {
    int i;
    for(i=0; i <MD5_DIGEST_LENGTH; i++) {
            printf("%02x",md[i]);
    }
    printf("\n");
}


using namespace std;


void solve(const char *text, const unsigned char mask[3]) {
    char buffer[20];
    unsigned char result[MD5_DIGEST_LENGTH];
    int i=0;
    int n=0;
    int check=0;
    printf("part2 on text %s\n",text);
    do {
        n = sprintf(buffer,"%s%d",text,i);
        MD5((unsigned char*) buffer, n, result);
        check  = (result[0] & mask[0]) ==0;
        check  = check and (result[1] & mask[1]) ==0;
        check  = check and (result[2] & mask[2]) ==0;
        i++;
    } while(!check);
    printf("    Buffer [%d] - %s\n    ",i-1,buffer);
    print_md5_sum(result);
}

int main () {
    cout<<"Advent of code 2015 day 04"<<endl;
    const char *example = "abcdef";
    const char *secret  = "bgvyzdsv";
    const unsigned char fivezeros[3] = {0xff,0xff,0xf0};
    const unsigned char sixzeros [3] = {0xff,0xff,0xff};
    solve(secret,fivezeros);
    solve(secret,sixzeros);
    return 0;
}
