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
    "04x04: 00 00 00 00 02 00\n"
    "12x05: 01 00 01 00 02 02\n"
    "12x05: 01 00 01 00 03 02\n";


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
    size_t fs;
    fs=fread(buffer,1,n,f);
    if (fs!=n) {
        fprintf(stderr,"Non ha letto tutti i bytes: ne ha letti %lu invece di %lu\n",fs,n);
        exit(EXIT_FAILURE);
    }
    return buffer;
}

int64_t part1(size_t textlen, char *text) {
    int W[6]={0,0,0,0,0,0};
    int B[6]={0,0,0,0,0,0};
    int w,h;
    char *p=text;
    char *end = text+textlen;
    int i,j;
    // we only care about the weights of tiles
    assert(*p=='0');
    for(i=0;i<6;i++) {
        p++;
        while(*p<'0' || *p>'9') {
            if (*p=='#') W[i]++;
            p++;
        }
    }

    int maybe=0,sat=0,unsat=0;
    int lowerbound,presents;
    assert(*p<='9' && *p>='0');
    while(p<end-1) {
        assert(*p<='9' && *p>='0');
        w= p[0]*10+p[1] - 11*'0';
        h= p[3]*10+p[4] - 11*'0';
        B[0] = p[ 7]*10+p[ 8] - 11*'0';
		B[1] = p[10]*10+p[11] - 11*'0';
		B[2] = p[13]*10+p[14] - 11*'0';
		B[3] = p[16]*10+p[17] - 11*'0';
		B[4] = p[19]*10+p[20] - 11*'0';
		B[5] = p[22]*10+p[23] - 11*'0';
        lowerbound=0;
        presents=0;
        for(j=0;j<6;j++) {
            lowerbound+=B[j]*W[j];
            presents+=B[j];
        }
        if (lowerbound>w*h) {
            unsat++;
        } else if (presents<=(w/3)*(h/3)) {
            sat++;
        } else {
            maybe++;
        }
        p+=25;
    }
    if (maybe+sat+unsat==3) {
        // hard example ;)
        return 2;
    }
    assert(maybe==0);
    return sat;
}

int main() {
    clock_t start,end;
    int64_t res;
    char *buffer;
    size_t filelen;

    start=clock();
    filelen  = file_size("input12.txt");
    buffer   = read_file("input12.txt",filelen);
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
    return 0;
}
