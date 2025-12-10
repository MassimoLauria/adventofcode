// Advent of Code 2025 day XX

#include <stdlib.h>
#include <stdint.h>
#include <stdio.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <time.h>

char example[]=\
"[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}\n"
"[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}\n"
"[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}\n";

struct AllocatedArray {
    size_t cap;
    size_t datasize;
    size_t len;
};

struct AllocatedArray* GetArray(void * array) {
    return ((struct AllocatedArray*)(array - sizeof(struct AllocatedArray)));
}


size_t Len(void * array) {
    return ((struct AllocatedArray*)(array - sizeof(struct AllocatedArray)))->len;
}

size_t Capacity(void * array) {
    return ((struct AllocatedArray*)(array - sizeof(struct AllocatedArray)))->cap;
}

void Resize(void *array,size_t n) {
    struct AllocatedArray *x = (struct AllocatedArray*)(array - sizeof(struct AllocatedArray));
    if (n<1 || n > x->cap) {
        perror("AllocArray: Extension failure. Not enough capacity or new size < 1");
        exit(EXIT_FAILURE);
    }
    x->len = n;
}

int mod(int x,int d){
    return (d + (x % d)) % d;
}

int64_t ABS(int64_t x) { return x<0?-x:x;  }
int64_t MIN(int64_t a,int64_t b) { return a<=b?a:b;  }
int64_t MAX(int64_t a,int64_t b) { return a<b?b:a;   }


/* Allocation of an array with length and capacity

   |CAPACITY|DATASIZE|_LENGTH_|.... data ....|

*/
void* AllocArray(size_t  len, size_t capacity, size_t objsize) {
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
    pack->cap=capacity;
    pack->len=len;
    pack->datasize=objsize;
    return mem+sizeof(struct AllocatedArray);
}

struct system {
    int n;
    int m;
    uint16_t b;
    uint16_t A[13];
    int joltage[13];
};

uint16_t evaluate(struct system *S, uint16_t X) {
    unsigned int16_t value=0;
    unsigned int16_t bit=1;
    for(i=0;i<S->n;i++) {
        if ( X & bit ) value ^= S->A[i];
    }
    return value;
}

char *parse_text(struct system *S, char *p) {
    S->b = 0;
    int n,m;
    unsigned int16_t bit=1;
    int bits=0;
    int buttons=0;
    while(1) {
        switch(*p) {
        case '\n':
            return ++p;
        case '#':
            S-> |= bit  ;  // fall through case
        case '#':
            bit= bit<<1 ;
            n++;
            break;
        case '(':
            n++;
            break;
        }
        i++;
    }
}


char* load_file(char *filename) {
    struct stat st;
    if (stat(filename,&st)==-1) {
        perror(filename);
        exit(EXIT_FAILURE);
    }
    size_t n=(size_t)st.st_size;
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


int64_t part1(size_t textlen, char *text) {
    char *end = *text+textlen;
    char *p=text;
    struct system Axb;
    while (p<end) {
        p=parse_text(&Axb,p);
    }
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

    start=clock();
	buffer = load_file("input10.txt");
	end = clock();
    printf("Loading data                                  - %f\n", ((double)(end-start))/CLOCKS_PER_SEC);

    start=clock();
	res = part1(sizeof(example),example);
	end = clock();
    printf("Part1 - example   : %-25ld - %f\n", res, ((double)(end-start))/CLOCKS_PER_SEC);

    start=clock();
    res = part1(Len(buffer), buffer );
	end = clock();
    printf("Part1 - challenge : %-25ld - %f\n", res, ((double)(end-start))/CLOCKS_PER_SEC);

    start=clock();
	res = part2(sizeof(example),example);
	end = clock();
    printf("Part2 - example   : %-25ld - %f\n", res, ((double)(end-start))/CLOCKS_PER_SEC);

    start=clock();
    res = part2(Len(buffer), buffer );
	end = clock();
    printf("Part2 - challenge : %-25ld - %f\n", res, ((double)(end-start))/CLOCKS_PER_SEC);

    return 0;
}
