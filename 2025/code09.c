// Advent of Code 2025 day XX

#include <stdlib.h>
#include <stdint.h>
#include <stdio.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <time.h>
#include <assert.h>

char example[]="7,1\n11,1\n11,7\n9,7\n9,5\n2,5\n2,3\n7,3\n";

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


void *parse_text(size_t textlen, char *text) {
    int i=0;
    size_t N=0;
    for(i=0;i<textlen;i++) {
        if (text[i]=='\n') N++;
    }
    int64_t *data=AllocArray(2*N, 2*N, sizeof(int64_t));
    size_t idx=0;
    char *p=text;
    while(idx<2*N) {
        data[idx]=0;
        while('0'<=*p && *p <='9') {
            data[idx] = 10*data[idx]+(*p - '0');
            p++;
        }
        idx++;
        p++;
    }
    // check list properties
    assert(N%2==0);
    int64_t *a,*b;
    if (data[0]==data[2]) {
        assert(data[2*N-4]==data[2*N-2]);
        assert(data[1]==data[2*N-1]);
        a=data; b=data+3;
    } else {
        a=data+2; b=data+1;
        assert(data[2*N-3]==data[2*N-1]);
        assert(data[0]==data[2*N-2]);
    }
    for(i=0;i<N-2;i+=2) {
        assert(a[2*i]==a[2*i+2]);
        assert(a[2*i]!=a[2*i+4]);
        assert(b[2*i]==b[2*i+2]);
        assert(b[2*i]!=b[2*i+4]);
    }
    printf("%lu\n",N);
    return data;
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
    int64_t *R = parse_text(textlen,text);
    size_t i,j,N=Len(R)/2;
    int64_t maxarea=0;
    int64_t tmparea;
    for(i=0;i<N-1;i++) {
        for(j=i+1;j<N;j++) {
            tmparea = (R[2*i]-R[2*j]+1)*(R[2*i+1]-R[2*j+1]+1);
            if (tmparea<0) tmparea*=-1;
            if (tmparea>maxarea) maxarea=tmparea;
        }
    }
    return maxarea;
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
	buffer = load_file("input09.txt");
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
