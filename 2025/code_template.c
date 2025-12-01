// Advent of Code 2025 day XX

#include <stdlib.h>
#include <stdint.h>
#include <stdio.h>
#include <sys/stat.h>
#include <time.h>

char example[]="shndj4hkjhejkededs\nsdkjkas0";

struct data {
    int len;
    int cap;
    int *data;
};

int mod(int x,int d){
    return (d + (x % d)) % d;
}

struct data parse_text(ssize_t textlen, char *p) {

    struct data input = { .len=0, .cap=textlen, .data=NULL };
    return input;
}


/* Gives a memory address containing the byte length of the file as an ssize_t,
   and all the bytes of the file.

   E.g. a 64bit integer and x bytes

   |IIIIIIII|BBBBBBBBBBBB....|

*/
void *load_file(char *filename) {
    ssize_t size;
    struct stat st;
    if (stat(filename,&st)==-1) {
        perror(filename);
        exit(EXIT_FAILURE);
    }
    size=st.st_size;
    void *mem=malloc(sizeof(size)+size*sizeof(char));
    int  *p=mem;
    *p = size;
    char *text=mem+sizeof(size);
    FILE *f = fopen(filename,"r");
    if (f==NULL) {
        perror(filename);
        exit(EXIT_FAILURE);
    }
    if (fread(text,1,size,f)!=size) {
        perror("Non ha letto tutti i bytes");
        exit(EXIT_FAILURE);
    }
    return mem;
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
    void *mem;

    start=clock();
	res = part1(parse_text(sizeof(example),example));
	end = clock();
    printf("Part1 - example   : %-25d - %f\n", res, ((double)(end-start))/CLOCKS_PER_SEC);

    start=clock();
    mem=load_file("input01.txt");
    res = part1(parse_text(*(int*)mem, mem +sizeof(ssize_t) ));
	end = clock();
    printf("Part1 - challenge : %-25d - %f\n", res, ((double)(end-start))/CLOCKS_PER_SEC);

    start=clock();
	res = part2(parse_text(sizeof(example),example));
	end = clock();
    printf("Part2 - example   : %-25d - %f\n", res, ((double)(end-start))/CLOCKS_PER_SEC);

    start=clock();
    mem=load_file("input01.txt");
    res = part1(parse_text(*(int*)mem, mem +sizeof(ssize_t) ));
	end = clock();
    printf("Part2 - challenge : %-25d - %f\n", res, ((double)(end-start))/CLOCKS_PER_SEC);

    return 0;
}
