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


int mod(int x,int d){
    return (d + (x % d)) % d;
}

struct tile {
    int weight;
    char body[3][3];
};

struct board {
    int h;
    int w;
    int goals[6];
};

void fill_board(struct board *B,char *p) {
    B->w= p[0]*10+p[1] - 11*'0';
    B->h= p[3]*10+p[4] - 11*'0';
    B->goals[0] = p[ 7]*10+p[ 8] - 11*'0';
    B->goals[1] = p[10]*10+p[11] - 11*'0';
    B->goals[2] = p[13]*10+p[14] - 11*'0';
    B->goals[3] = p[16]*10+p[17] - 11*'0';
    B->goals[4] = p[19]*10+p[20] - 11*'0';
    B->goals[5] = p[22]*10+p[23] - 11*'0';
}

void print_board(struct board *B) {
    printf("%2dx%2d: %2d %2d %2d %2d %2d %2d\n",
           B->w,B->h,
           B->goals[0],B->goals[1],B->goals[2],
           B->goals[3],B->goals[4],B->goals[5]);
}

int64_t ABS(int64_t x) { return x<0?-x:x;  }
int64_t MIN(int64_t a,int64_t b) { return a<=b?a:b;  }
int64_t MAX(int64_t a,int64_t b) { return a<b?b:a;   }

void *parse_text(size_t textlen, char *p) {
    return p;
}

void *fill_tile(struct tile *data,char *p) {
    while(*p++!=':');
    p++;
    int i,j,w=0;
    for(i=0;i<3;i++) {
        for(j=0;j<3;j++) {
            data->body[i][j] = *(p+i*4+j);
            if (data->body[i][j]=='#') w++;
        }
    }
    data->weight = w;
    return p+12;
}

void print_tile(struct tile *data) {
    for(int i=0;i<3;i++) {
        for(int j=0;j<3;j++) {
            printf("%c",data->body[i][j]);
        }
        printf("\n");
    }
    printf("Weight %d\n",data->weight);
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
    size_t fs;
    fs=fread(buffer,1,n,f);
    if (fs!=n) {
        fprintf(stderr,"Non ha letto tutti i bytes: ne ha letti %lu invece di %lu\n",fs,n);
        exit(EXIT_FAILURE);
    }
    return buffer;
}

int64_t part1(size_t textlen, char *text) {
    struct tile T[6];
    struct board B[1000];
    char *p=text;
    char *end = text+textlen;
    int i,j,lowerbound,presents;
    for(i=0;i<6;i++) {
        p = fill_tile(&T[i], p);
    }
    p++;
    int num_boards=0;
    assert(*p<='9' && *p>='0');
    while(p<end-1) {
        assert(*p<='9' && *p>='0');
        fill_board(&B[num_boards],p);
        p+=25;
        num_boards++;
    }
    int maybesat=0;
    for(i=0;i<num_boards;i++) {
        lowerbound=0;
        presents=0;
        for(j=0;j<6;j++) {
            lowerbound+=B[i].goals[j]*T[j].weight;
            presents+=B[i].goals[j];
        }
        if (lowerbound>B[i].w*B[i].h) {
            printf("%3d: easy unsat\n",i);
        } else if (presents<=(B[i].w/3)*(B[i].h/3)) {
            printf("%3d: easy sat\n",i);
        } else {
            maybesat++;
            printf("%3d: maybe??\n",i);
        }
    }
    return maybesat;
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
