// Advent of Code 2025 day XX

#include <stdlib.h>
#include <stdint.h>
#include <stdio.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <time.h>
#include <assert.h>

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

int howmanybits(uint16_t x) {
    int n=0;
    while(x) {
        n++;
        x &= x - 1;
    }
    return n;
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

struct systemF2 {
    int n;
    int m;
    uint16_t b;
    uint16_t A[13];
};

struct systemZ {
    unsigned n;
    unsigned m;
    unsigned A[10][13];
    unsigned b[10];
    unsigned value[10];
    unsigned total;
};

#define NOSOLUTION 100000


unsigned max_value(struct systemZ *S, unsigned j) {
    unsigned value = 100000;
    for(unsigned i=0;i<S->n;i++) {
        assert(S->b[i]>=S->value[i]);
        if (S->A[i][j]) value = MIN(value,S->b[i] - S->value[i]);
    }
    return value;
}

void add_some(struct systemZ *S, unsigned j, unsigned w) {
    S->total += w;
    for(unsigned i=0;i<S->n;i++) {
        S->value[i] += w*S->A[i][j];
    }
}

void sub_some(struct systemZ *S, unsigned j, unsigned w) {
    S->total -= w;
    for(unsigned i=0;i<S->n;i++) {
        assert(S->value[i]>=w*S->A[i][j]);
        S->value[i] -= w*S->A[i][j];
    }
}

void print_systemZ(struct systemZ *S);

unsigned solve(struct systemZ *S, unsigned depth) {
    unsigned i=0,R;
    if (depth>=S->m) {
        for(unsigned i=0;i<S->n;i++) {
            if (S->b[i]!=S->value[i]) return NOSOLUTION;
        }
        return S->total;
    }

    R = max_value(S,depth);
    unsigned opt=solve(S,depth+1);
    unsigned tmp;
    for(i=1;i<=R;i++) {
        add_some(S,depth,1);
        tmp = solve(S,depth+1);
        if (tmp<opt ) opt=tmp;
    }
    sub_some(S,depth,R);
    return opt;
}

uint16_t evaluateF2(struct systemF2 *S, uint16_t X) {
    uint16_t value=0;
    uint16_t bit=1;
    for(size_t i=0;i<S->m;i++) {
        if ( X & bit ) value ^= S->A[i];
        bit <<= 1;
    }
    return value;
}

char *parse_systemF2(struct systemF2 *S, char *p) {
    S->b = 0;
    S->n = 0;
    S->m = 0;
    uint16_t bit=1;
    while(1) {
        switch(*p) {
        case '\n':
            return ++p;
        case '#':
            S->b |= bit  ;  // fall through case
        case '.':
            bit= bit<<1 ;
            S->n++;
            break;
        case '(':
            p++;
            S->A[S->m]=0;
            while(*p!=' ') {
                S->A[S->m] |= 1 << (*p-'0');
                p+=2;
            }
            S->m++;
            break;
        }
        p++;
    }
}

char *parse_systemZ(struct systemZ *S, char *p) {
    S->n = 0;
    S->m = 0;
    S->total=0;
    while(*p!='[') { p++;}
    p++;
    while(*p!=']') { S->n++; p++;}
    while(*p!='{') {
        if (*p=='(') {
            for(unsigned i=0;i<S->n;i++) S->A[i][S->m]=0;
        }
        if (*p>='0' && *p <='9') S->A[(*p-'0')][S->m]=1;
        if (*p==')') S->m++;
        p++;
    }
    p++;
    unsigned tmp=0;
    unsigned idx=0;
    do {
        if (*p>='0' && *p <='9') tmp= 10*tmp+(*p-'0');
        else {
            S->b[idx] = tmp;
            S->value[idx] = 0;
            tmp=0;
            idx++;
        }
        p++;
    } while (*p!='\n');
    return ++p;
}


void print_systemZ(struct systemZ *S) {
    unsigned i,j;
    unsigned  tmp,units=0;
    for (i=0;i<S->n;i++) {
        tmp=0;
        for (j=0;j<S->m;j++) {
            tmp+=S->A[i][j];
            printf("%u",S->A[i][j]);
        }
        if (tmp==1) units++;
        printf("  =  %u   (%u)\n",S->b[i], S->value[i]);
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
    char *p=text;
    struct systemF2 Axb;
    int total=0;
    uint16_t X;

    int howmany[1<<13];
    for(X=0;X<(1<<13);X++) howmany[X]=howmanybits(X);

    while (*p=='[') {
        p=parse_systemF2(&Axb,p);
        uint16_t T=1<<Axb.m;
        assert(T<=(1<<13));
        int sol=Axb.m+1;
        for(X=0;X<T;X++) {
           if (evaluateF2(&Axb,X)==Axb.b) {
               if (sol>howmany[X]) sol=howmany[X];
            }
        }
        assert(sol<=Axb.m);
        total+=sol;
    }
    return total;
}

int64_t part2(size_t textlen, char *text) {
    char *p=text;
    struct systemZ Axb;
    unsigned optimal;
    unsigned sum=0;
    while (*p=='[') {
        p=parse_systemZ(&Axb,p);
        optimal=solve(&Axb,0);
        sum+=optimal;
    }
    return sum;
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

    /* start=clock();
     * res = part2(Len(buffer), buffer );
	 * end = clock();
     * printf("Part2 - challenge : %-25ld - %f\n", res, ((double)(end-start))/CLOCKS_PER_SEC); */

    return 0;
}
