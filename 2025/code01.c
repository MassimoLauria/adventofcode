#include <stdlib.h>
#include <stdint.h>
#include <stdio.h>
#include <sys/stat.h>
#include <time.h>

char example[]="L68\nL30\nR48\nL5\nR60\nL55\nL1\nL99\nR14\nL82\n";

struct numdata {
    int len;
    int cap;
    int *data;
};

int mod(int x,int d){
    return (d + (x % d)) % d;
}

struct numdata parse_text(char *p,ssize_t textlen) {

    struct numdata input = { .len=0, .cap=textlen, .data=NULL };
    input.data = (int*)malloc(sizeof(int)*textlen);

    int sign=+1;
    int tmp=0;
    char *end = p+textlen;
    while(p<end) {
        switch (*p) {
        case 'L':
            sign=-1;
            tmp=0;
            break;
        case 'R':
            sign=+1;
            tmp=0;
            break;
        case '\n':
            input.data[input.len++]=sign*tmp;
            break;
        default:
            tmp=tmp*10+(*p-'0');
        }
        p++;
    }
    return input;
}


struct numdata parse_file(char *filename) {
    ssize_t size;
    struct stat st;
    if (stat(filename,&st)==-1) {
        perror(filename);
        exit(EXIT_FAILURE);
    }
    size=st.st_size;
    char *text=(char*)malloc(size*sizeof(char));
    FILE *f = fopen(filename,"r");
    if (f==NULL) {
        perror(filename);
        exit(EXIT_FAILURE);
    }
    if (fread(text,1,size,f)!=size) {
        perror("Non ha letto tutti i bytes");
        exit(EXIT_FAILURE);
    }
    return parse_text(text,size);
}


int part1(struct numdata input) {
    int v=50;
    int count=0;
    for(int i=0;i<input.len;i++) {
        v += input.data[i];
        if (v%100==0) count++;
    }
    return count;
}

int part2(struct numdata input) {
    int v=50;
    int count=0;
    int R;
    for(int i=0;i<input.len;i++) {
        R = input.data[i];
        if (R<0) {
            count += (-R+mod(-v,100))/100;
        } else  {
            count += ( R+v)/100;
        }
        v = mod(v + R,100);
    }
    return count;
}

int main() {
    clock_t start,end;
    int res;

    start=clock();
	res = part1(parse_text(example,sizeof(example)));
	end = clock();
    printf("Part1 - example   : %-25d - %f\n", res, ((double)(end-start))/CLOCKS_PER_SEC);

    start=clock();
    res = part1(parse_file("input01.txt"));
	end = clock();
    printf("Part1 - challenge : %-25d - %f\n", res, ((double)(end-start))/CLOCKS_PER_SEC);

    start=clock();
	res = part2(parse_text(example,sizeof(example)));
	end = clock();
    printf("Part2 - example   : %-25d - %f\n", res, ((double)(end-start))/CLOCKS_PER_SEC);

    start=clock();
    res = part2(parse_file("input01.txt"));
	end = clock();
    printf("Part2 - challenge : %-25d - %f\n", res, ((double)(end-start))/CLOCKS_PER_SEC);

    return 0;
}
