// Advent of Code 2025 day XX

#include <stdlib.h>
#include <stdint.h>
#include <stdio.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <time.h>
#include <assert.h>

char example[]=\
    "0:\n"
    "###\n"
    "##.\n"
    "##.\n"
    "\n"
    "1:\n"
    "###\n"
    "##.\n"
    ".##\n"
    "\n"
    "2:\n"
    ".##\n"
    "###\n"
    "##.\n"
    "\n"
    "3:\n"
    "##.\n"
    "###\n"
    "##.\n"
    "\n"
    "4:\n"
    "###\n"
    "#..\n"
    "###\n"
    "\n"
    "5:\n"
    "###\n"
    ".#.\n"
    "###\n"
    "\n"
    "4x4: 0 0 0 0 2 0\n"
    "12x5: 1 0 1 0 2 2\n"
    "12x5: 1 0 1 0 3 2\n";


int mod(int x,int d){
    return (d + (x % d)) % d;
}

int64_t ABS(int64_t x) { return x<0?-x:x;  }
int64_t MIN(int64_t a,int64_t b) { return a<=b?a:b;  }
int64_t MAX(int64_t a,int64_t b) { return a<b?b:a;   }



void *parse_text(size_t textlen, char *p) {
    return p;
}


size_t file_size(char *filename) {
    struct stat st;
    if (stat(filename,&st)==-1) {
        perror(filename);
        exit(EXIT_FAILURE);
    }
    size_t n=(size_t)st.st_size;
    return n;
}

char *read_file(char *filename, size_t n) {
    char *buffer = (char*)malloc(n*sizeof(char));
    FILE *f = fopen(filename,"r");
    if (f==NULL) {
        perror(filename);
        exit(EXIT_FAILURE);
    }
    if (fread(buffer,1,n,f)!=n) {
        perror("Non ha letto tutti i bytes");
        exit(EXIT_FAILURE);
    }
    return buffer;
}

int64_t part1(size_t textlen, char *text) {
    parse_text(textlen,text);
    return 42;
}

int64_t part2(size_t textlen, char *text) {
    parse_text(textlen,text);
    return 42;
}

int main() {
    clock_t start,end;
    int64_t res;
    char *buffer;
    size_t filelen;

    start=clock();
    filelen  = file_size("input12.txt");
    buffer   = read_file("input02.txt",filelen);
	end = clock();
    printf("Loading data                                  - %f\n", ((double)(end-start))/CLOCKS_PER_SEC);

    start=clock();
	res = part1(sizeof(example),example);
	end = clock();
    printf("Part1 - example   : %-25ld - %f\n", res, ((double)(end-start))/CLOCKS_PER_SEC);

    start=clock();
    res = part1(filelen, buffer );
	end = clock();
    printf("Part1 - challenge : %-25ld - %f\n", res, ((double)(end-start))/CLOCKS_PER_SEC);

    start=clock();
	res = part2(sizeof(example),example);
	end = clock();
    printf("Part2 - example   : %-25ld - %f\n", res, ((double)(end-start))/CLOCKS_PER_SEC);

    start=clock();
    res = part2(filelen, buffer );
	end = clock();
    printf("Part2 - challenge : %-25ld - %f\n", res, ((double)(end-start))/CLOCKS_PER_SEC);

    return 0;
}
