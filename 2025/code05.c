// Advent of Code 2025 day XX

#include <stdlib.h>
#include <stdint.h>
#include <stdio.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <time.h>
#include <assert.h>

char example[]="3-5\n10-14\n16-20\n12-18\n\n1\n5\n8\n11\n17\n32\n";

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

int64_t getNum(char *s,char *e) {
    int64_t val=0;
    while (s<e) {
        val = *s-'0' + val*10;
        s++;
    }
    return val;
}

int64_t *parse_text(ssize_t textlen, char *text) {
    int pairs=0;
    int nls=0;
    int i;
    for(i=0;i<textlen;i++) {
        if (text[i]=='-') pairs++;
        if (text[i]=='\n') nls++;
    }
    int ids=nls-pairs-1;
    int64_t *data = (int64_t*)AllocArray(pairs*2+ids+2, pairs*2+ids+2,sizeof(int64_t));
    data[0]=(int64_t)pairs;
    data[1]=(int64_t)ids;
    char *s=text;
    char *e=text;
    for(i=2;i<Len(data);i++) {
        while(*s<'0' || *s >'9') s++;
        e=s;
        while(*e>='0' && *e <='9') e++;
        data[i]=getNum(s,e);
        s=e+1;
    }
    return data;
}


int64_t part1(ssize_t textlen, char *text) {
    int64_t *data = parse_text(textlen,text);
    int64_t pairs=data[0];
    int64_t ids=data[1];
    assert(2*pairs+ids + 2 == Len(data));
    int count=0;
    int fresh;
    int i,j;
    for(i=2*pairs+2;i<Len(data);i++) {
        fresh=0;
        for(j=2;j<2*pairs+2;j+=2) {
            if (data[i]>=data[j] && data[i]<=data[j+1]) {
                fresh=1;
                break;
            }
        }
        count+=fresh;
    }
    return count;
}

int cmp(const void *a, const void *b) {
    int64_t na=*(int64_t*)a;
    int64_t nb=*(int64_t*)b;
    if (na<nb) return -1;
    else if (na==nb) return 0;
    else return 1;
}

int64_t part2(ssize_t textlen, char *text) {
    int64_t *data = parse_text(textlen,text);
    int64_t N=data[0];
    int64_t *pairs=data+2;
    // sort pairs
    qsort(pairs,N,2*sizeof(int64_t),cmp);
    int64_t fresh=0;
    int64_t sb=0,se=0;  // [sb,se[ interval
    for(int i=0;i<2*N;i+=2) {
        if (pairs[i]>se) { // disjoint interval opens
            fresh+=(se-sb);
            sb=pairs[i];
            se=pairs[i+1]+1;
        } else if ( pairs[i+1]>=se) {
            se=pairs[i+1]+1;
        }
    }
    fresh += se-sb;
    return fresh;
}

int main() {
    clock_t start,end;
    int64_t res;
    char *buffer;

    start=clock();
	buffer = load_file("input05.txt");
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
