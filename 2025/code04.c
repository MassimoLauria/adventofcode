// Advent of Code 2025 day XX

#include <stdlib.h>
#include <stdint.h>
#include <stdio.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <time.h>
#include <assert.h>

char example[]="..@@.@@@@.\n@@@.@.@.@@\n@@@@@.@.@@\n@.@@@@..@.\n@@.@@@@.@@\n.@@@@@@@.@\n.@.@.@.@@@\n@.@@@.@@@@\n.@@@@@@@@.\n@.@.@@@.@.\n";

struct AllocatedArray {
    void *end;
    ssize_t datasize;
    ssize_t len;
};

struct AllocatedArray* GetArray(void * array) {
    return ((struct AllocatedArray*)(array - sizeof(struct AllocatedArray)));
}


ssize_t Len(void * array) {
    return ((struct AllocatedArray*)(array - sizeof(struct AllocatedArray)))->len;
}

ssize_t Capacity(void * array) {
    struct AllocatedArray *x = (struct AllocatedArray*)(array - sizeof(struct AllocatedArray));
    return  (x->end-array)/x->datasize;
}

void Extend(void *array,ssize_t n) {
    struct AllocatedArray *x = (struct AllocatedArray*)(array - sizeof(struct AllocatedArray));
    if (x->end < array+(n+x->len)*x->datasize) {
        perror("AllocArray: Extension failure. No more capacity");
        exit(EXIT_FAILURE);
    }
    x->len += n;
}

int mod(int x,int d){
    return (d + (x % d)) % d;
}

/* Allocation of an array with length and capacity

   |END-POINT|DATASIZE|IIIIIIII|.... data ....|

*/
void* AllocArray(ssize_t  len, ssize_t capacity, ssize_t objsize) {
    if (len==0 || objsize==0 || len>capacity) {
        perror("AllocArray: Invalid parameters");
        exit(EXIT_FAILURE);
    }
    void *mem = malloc(sizeof(struct AllocatedArray)+ objsize*capacity);
    if (mem==NULL) {
        perror("AllocArray failed");
        exit(EXIT_FAILURE);
    }
    struct AllocatedArray* pack=mem;
    pack->end=mem + sizeof(struct AllocatedArray)+ objsize*capacity;
    pack->len=len;
    pack->datasize=objsize;
    return mem+sizeof(struct AllocatedArray);
}


char* load_file(char *filename) {
    struct stat st;
    if (stat(filename,&st)==-1) {
        perror(filename);
        exit(EXIT_FAILURE);
    }
    ssize_t n=st.st_size;
    char *buffer = AllocArray(n, n,sizeof(char));
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

int D8[][2] = { {-1,-1},{-1, 0},{-1,+1},
                { 0,-1},        { 0,+1},
                {+1,-1},{+1, 0},{+1,+1}};


int mark(char *text, int N) {
    char x,y;
    int i,r,c,dr,dc,count=0;
    int neigs;
    for(r=0;r<N;r++) {
        for(c=0;c<N;c++) {
            x = text[r*N+r+c];
            neigs=0;
            if (x=='.') continue;
            for(i=0;i<8;i++) {
                dr=r+D8[i][0];
                dc=c+D8[i][1];
                if ( dr<0 || dr>=N ) continue;
                if ( dc<0 || dc>=N ) continue;
                y = text[dr*N+dr+dc];
                if (y!='.') neigs++;
            }
            if (neigs<4) {
                count++;
                text[r*N+r+c]='x';
            }
        }
    }
    return count;
}

void removepaper(char *text, int N) {
    char x;
    int r,c;
    for(r=0;r<N;r++) {
        for(c=0;c<N;c++) {
            x = text[r*N+r+c];
            if (x!='x') continue;
            text[r*N+r+c] ='.';
        }
    }
}


/* Matrix is square */
int64_t part1(ssize_t textlen, char *text) {
    int N=0;
    char *p=text;
    while(*(p++)!='\n') N++;
    assert(N == textlen/(N+1));
    return mark(text,N);
}

int64_t part2(ssize_t textlen, char *text) {
    int N=0;
    char *p=text;
    int r;
    while(*(p++)!='\n') N++;
    assert(N == textlen/(N+1));
    int count=0;
    do {
        r =  mark(text,N);
        removepaper(text, N);
        count += r;
    } while (r);
    return count;
}

int main() {
    clock_t start,end;
    int64_t res;
    char *buffer;

    start=clock();
	buffer = load_file("input04.txt");
	end = clock();
    printf("Loading data                                  - %f\n", ((double)(end-start))/CLOCKS_PER_SEC);

    start=clock();
	res = part1(sizeof(example),example);
	end = clock();
    printf("Part1 - example   : %-25ld - %f\n", res, ((double)(end-start))/CLOCKS_PER_SEC);

    start=clock();
    res = part1(Len(buffer), buffer);
	end = clock();
    printf("Part1 - challenge : %-25ld - %f\n", res, ((double)(end-start))/CLOCKS_PER_SEC);

    start=clock();
	res = part2(sizeof(example),example);
	end = clock();
    printf("Part2 - example   : %-25ld - %f\n", res, ((double)(end-start))/CLOCKS_PER_SEC);

    start=clock();
    res = part2(Len(buffer), buffer);
	end = clock();
    printf("Part2 - challenge : %-25ld - %f\n", res, ((double)(end-start))/CLOCKS_PER_SEC);

    return 0;
}
