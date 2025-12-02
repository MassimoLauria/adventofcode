// Advent of Code 2025 day XX

#include <stdlib.h>
#include <stdint.h>
#include <stdio.h>
#include <sys/stat.h>
#include <time.h>

char example[]="shndj4hkjhejkededs\nsdkjkas0";

ssize_t Len(void * mem) {
    return  *((ssize_t*)mem-1);
}

int mod(int x,int d){
    return (d + (x % d)) % d;
}

void* AllocLen(ssize_t n, ssize_t objsize) {
    if (n==0 || objsize==0) {
        perror("AllocLen does not accept zero sized data");
        exit(EXIT_FAILURE);
    }
    void *mem = malloc(sizeof(n)+objsize*n);
    if (mem==NULL) {
        perror("AllocLen failed");
        exit(EXIT_FAILURE);
    }
    return mem;
}

struct data {
    int len;
    int cap;
    int *data;
};


struct data parse_text(ssize_t textlen, char *p) {

    struct data input = { .len=0, .cap=textlen, .data=NULL };
    return input;
}


/* Gives a memory address containing the byte length of the file as an ssize_t,
   and all the bytes of the file.

   E.g. a 64bit integer and x bytes

   |IIIIIIII|BBBBBBBBBBBB....|

*/
char* load_file(char *filename) {
    struct stat st;
    if (stat(filename,&st)==-1) {
        perror(filename);
        exit(EXIT_FAILURE);
    }
    ssize_t n=st.st_size;
    char *buffer = AllocLen(n, sizeof(char));
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


int part1(struct data input) {
    return 42;
}

int part2(struct data input) {
    return 42;
}

int main() {
    clock_t start,end;
    int res;
    char *buffer;

    start=clock();
	buffer = load_file("input01.txt");
	end = clock();
    printf("Loading data                                  - %f\n", ((double)(end-start))/CLOCKS_PER_SEC);

    start=clock();
	res = part1(parse_text(sizeof(example),example));
	end = clock();
    printf("Part1 - example   : %-25d - %f\n", res, ((double)(end-start))/CLOCKS_PER_SEC);

    start=clock();
    res = part1(parse_text(Len(buffer), buffer ));
	end = clock();
    printf("Part1 - challenge : %-25d - %f\n", res, ((double)(end-start))/CLOCKS_PER_SEC);

    start=clock();
	res = part2(parse_text(sizeof(example),example));
	end = clock();
    printf("Part2 - example   : %-25d - %f\n", res, ((double)(end-start))/CLOCKS_PER_SEC);

    start=clock();
    res = part2(parse_text(Len(buffer), buffer ));
	end = clock();
    printf("Part2 - challenge : %-25d - %f\n", res, ((double)(end-start))/CLOCKS_PER_SEC);

    return 0;
}
