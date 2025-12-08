// Advent of Code 2025 day 08

#include <stdlib.h>
#include <stdint.h>
#include <stdio.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <time.h>
#include <string.h>

char example[]=\
    "162,817,812\n"
    "57,618,57\n"
    "906,360,560\n"
    "592,479,940\n"
    "352,342,300\n"
    "466,668,158\n"
    "542,29,236\n"
    "431,825,988\n"
    "739,650,466\n"
    "52,470,668\n"
    "216,146,977\n"
    "819,987,18\n"
    "117,168,530\n"
    "805,96,715\n"
    "346,949,466\n"
    "970,615,88\n"
    "941,993,340\n"
    "862,61,35\n"
    "984,92,344\n"
    "425,690,689\n";

struct AllocatedArray {
    ssize_t cap;
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
    return ((struct AllocatedArray*)(array - sizeof(struct AllocatedArray)))->cap;
}

void Resize(void *array,ssize_t n) {
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

/* Allocation of an array with length and capacity

   |CAPACITY|DATASIZE|_LENGTH_|.... data ....|

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
    pack->cap=capacity;
    pack->len=len;
    pack->datasize=objsize;
    return mem+sizeof(struct AllocatedArray);
}


void *parse_text(ssize_t textlen, char *text) {
    int rows=0;
    for(int i=0;i<textlen;i++) {
        if (text[i]=='\n') rows++;
    }
    int64_t *data=AllocArray(3*rows, 3*rows, sizeof(int64_t));
    memset(data,0,3*rows*sizeof(int64_t));
    ssize_t idx=0;
    for(int i=0;i<textlen;i++) {
        if (text[i]>='0' && text[i]<='9') data[idx]=data[idx]*10+(text[i]-'0');
        else {idx++;}
    }
    return data;
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

int Find(int *P,int x) {
    while (P[x]!=x) {
        P[x] = P[P[x]];
        x = P[x];
    }
    return x;
}

void Join(int *P,int x,int y) {
    x = Find(P,x);
    y = Find(P,y);
    P[x] = y;
    P[y] = y;
}

int64_t MAX(int64_t a,int64_t b) { return a<b?b:a; }
int64_t MIN(int64_t a,int64_t b) { return a<=b?a:b; }


int64_t distsq(int64_t *numbers,ssize_t i,ssize_t j) {
    int64_t a =  numbers[3*i]-numbers[3*j];
    int64_t b =  numbers[3*i+1]-numbers[3*j+1];
    int64_t c =  numbers[3*i+2]-numbers[3*j+2];
    return a*a+b*b+c*c;
}

int cmp(const void *a, const void *b) {
    int64_t na=*(int64_t*)a;
    int64_t nb=*(int64_t*)b;
    if (na<nb) return -1;
    else if (na==nb) return 0;
    else return 1;
}

struct edge { int64_t w; int i; int j; };

int mypart(struct edge *E,int start,int end) {
    int pivot_pos = start;
    int i,j;
    int64_t value = E[pivot_pos].w;
    struct edge tmp;
    /* tmp = E[start];
     * E[start] = E[pivot_pos];
     * E[pivot_pos] = tmp; */
    i = start+1;
    j = end;
    while(i<j) {
        while(i<j && E[i].w < value) i++;
        while(i<j && E[j].w >= value) j--;
        if (i<j) {
            tmp = E[i];
            E[i] = E[j];
            E[j] = tmp;
        }
    }
    if (E[i].w>=value) i--;
    tmp = E[start];
    E[start] = E[i];
    E[i] = tmp;
    return i;
}

void  myqsort(struct edge *E,int start,int end,int needed) {
    if (start>=end) return;
    if (needed<=0) return;
    int pivot_pos= mypart(E, start, end);
    int neededleft, neededright;
    if (pivot_pos-start > needed) {
        neededleft = needed;
    } else {
        neededleft = pivot_pos-start;
    }
    neededright = needed - (pivot_pos-start+1);
    myqsort(E,start,pivot_pos-1,neededleft);
    myqsort(E,pivot_pos+1,end,neededright);
}


int64_t part1(ssize_t textlen, char *text, int howmany) {
    int64_t *numbers=parse_text(textlen,text);
    ssize_t i,j,N=Len(numbers)/3;
    int* parts=(int*)malloc(N*sizeof(int));
    for(i=0;i<N;i++) { parts[i]=i;}
    struct edge *E = (struct edge*)malloc(sizeof(struct edge)*N*(N-1)/2 );
    int t=0;
    for(i=0;i<N-1;i++) {
        for(j=i+1;j<N;j++) {
            E[t].w = distsq(numbers,i,j);
            E[t].i = i;
            E[t].j = j;
            t++;
        }
    }
    myqsort(E,0,N*(N-1)/2-1,howmany);
    for(t=0;t<howmany;t++) {
        i = E[t].i; j=E[t].j;
        Join(parts,E[t].i,E[t].j);
    }
    // Count
    int* C=(int*)malloc(N*sizeof(int));
    for(i=0;i<N;i++) { C[i]=0; parts[i]=Find(parts,i);} // finalize the parts
    for(i=0;i<N;i++) { C[parts[i]]++;}         // count sizes
    // best three
    int a=C[0],b=C[1],c=C[2]; // a<=b<=c
    int tmp;
    if (b<a) { tmp=a; a=b; b=tmp; }
    if (c<b) { tmp=c; c=b; b=tmp; }
    if (b<a) { tmp=a; a=b; b=tmp; }
    for(i=3;i<N;i++) {
        if (C[i]<=a) continue;
        a=C[i];
        if (b<a) { tmp=a; a=b; b=tmp; }
        if (c<b) { tmp=c; c=b; b=tmp; }
    }
    return a*b*c;
}

int64_t part2(ssize_t textlen, char *text,int howmany) {
    int64_t *numbers=parse_text(textlen,text);
    ssize_t i,j,N=Len(numbers)/3;
    int* parts=(int*)malloc(N*sizeof(int));
    for(i=0;i<N;i++) { parts[i]=i;}
    struct edge *E = (struct edge*)malloc(sizeof(struct edge)*N*(N-1)/2 );
    int t=0;
    for(i=0;i<N-1;i++) {
        for(j=i+1;j<N;j++) {
            E[t].w = distsq(numbers,i,j);
            E[t].i = i;
            E[t].j = j;
            t++;
        }
    }
    myqsort(E,0,N*(N-1)/2-1,howmany);
    int c=N-1;
    t=0;
    i= E[0].i; j=E[0].j;
    while(c) {
        i= E[t].i; j=E[t].j;
        if (Find(parts,i)!=Find(parts,j)) {
                Join(parts,i,j);
                c--;
        }
        t++;
    }
    return numbers[3*i]*numbers[3*j];
}

int main() {
    clock_t start,end;
    int64_t res;
    char *buffer;

    start=clock();
	buffer = load_file("input08.txt");
	end = clock();
    printf("Loading data                                  - %f\n", ((double)(end-start))/CLOCKS_PER_SEC);

    start=clock();
	res = part1(sizeof(example),example,10);
	end = clock();
    printf("Part1 - example   : %-25ld - %f\n", res, ((double)(end-start))/CLOCKS_PER_SEC);

    start=clock();
    res = part1(Len(buffer), buffer,1000);
	end = clock();
    printf("Part1 - challenge : %-25ld - %f\n", res, ((double)(end-start))/CLOCKS_PER_SEC);

    start=clock();
	res = part2(sizeof(example),example,30);
	end = clock();
    printf("Part2 - example   : %-25ld - %f\n", res, ((double)(end-start))/CLOCKS_PER_SEC);

    start=clock();
    res = part2(Len(buffer), buffer,7000);
	end = clock();
    printf("Part2 - challenge : %-25ld - %f\n", res, ((double)(end-start))/CLOCKS_PER_SEC);

    return 0;
}
