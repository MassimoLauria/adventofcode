// Advent of Code 2025 day XX

#include <stdlib.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <time.h>
#include <assert.h>

char example[]=\
    ".......S.......\n"
    "...............\n"
    ".......^.......\n"
    "...............\n"
    "......^.^......\n"
    "...............\n"
    ".....^.^.^.....\n"
    "...............\n"
    "....^.^...^....\n"
    "...............\n"
    "...^.^...^.^...\n"
    "...............\n"
    "..^...^.....^..\n"
    "...............\n"
    ".^.^.^.^.^...^.\n"
    "...............\n";

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


void *parse_text(ssize_t textlen, char *p) {

    int64_t *data=AllocArray(10, 35, sizeof(int64_t));
    for(int64_t i=0;i<Len(data);i++) {
        data[i]=i+1;
    }
    Resize(data,35);
    for(int64_t i=10;i<Len(data);i++) {
        data[i]=2*i;
    }
    struct AllocatedArray *a= GetArray(data);
    void *raw = (void*)a;
    void *end = a+Capacity(data)*sizeof(int64_t);
    int i=0;
    while(raw<end) {
        if (i%8==0) {
            printf("\n%p: ",raw);
        }
        printf("%02x ",*(unsigned char*)raw);
        raw++;
        i++;
    }
    printf("\n");
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


int64_t part1(ssize_t textlen, char *text) {
    int i,j,height,width;
    char *p;
    // size of the grid
    width=0;
    while(text[width]!='\n') width++;
    height= textlen/(width+1);
    int64_t *statei = (int64_t*)malloc(width*sizeof(int64_t));
    int64_t *stateo = (int64_t*)malloc(width*sizeof(int64_t));
    int64_t *tmp=NULL;
    memset(statei, 0, width*sizeof(int64_t));
    statei[width/2]=1;
    p = text+2*width+2;
    int splits=0;
    for(i=2;i<height;i+=2) {
        for(j=0;j<width;j++) {
            if (statei[j]==0) continue;
            if (p[j]=='^') {
                splits++;
                stateo[j-1]=1;
                stateo[j+1]=1;
            } else {
                stateo[j]=statei[j];
            }
            statei[j]=0;
        }
        tmp=statei;
        statei=stateo;
        stateo=tmp;
        p +=2*width+2;
    }
    return splits;
}

int64_t part2(ssize_t textlen, char *text) {
    int i,j,height,width;
    char *p;

    // size of the grid
    width=0;
    while(text[width]!='\n') width++;
    height= textlen/(width+1);


    int64_t *statei = (int64_t*)malloc(width*sizeof(int64_t));
    int64_t *stateo = (int64_t*)malloc(width*sizeof(int64_t));
    int64_t *tmp=NULL;
    memset(statei, 0, width*sizeof(int64_t));
    statei[width/2]=1;
    p = text+2*width+2;
    for(i=2;i<height;i+=2) {
        for(j=0;j<width;j++) {
            if (statei[j]==0) continue;
            if (p[j]=='^') {
                stateo[j-1]+=statei[j];
                stateo[j+1]+=statei[j];
            } else {
                stateo[j]+=statei[j];
            }
            statei[j]=0;
        }
        tmp=statei;
        statei=stateo;
        stateo=tmp;
        p +=2*width+2;
    }
    int64_t count=0;
    for(j=0;j<width;j++) {
        count+=statei[j];
    }
    return count;
}

int main() {
    clock_t start,end;
    int64_t res;
    char *buffer;

    start=clock();
	buffer = load_file("input07.txt");
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
