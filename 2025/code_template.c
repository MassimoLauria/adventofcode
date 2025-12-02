// Advent of Code 2025 day XX

#include <stdlib.h>
#include <stdint.h>
#include <stdio.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <time.h>

char example[]="shndj4hkjhejkededs\nsdkjkas0";

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

   |END-POINT|IIIIIIII|.... data ....|

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

void *parse_text(ssize_t textlen, char *p) {

    int64_t *data=AllocArray(10, 35, sizeof(int64_t));
    for(int64_t i=0;i<Len(data);i++) {
        data[i]=i+1;
    }
    Extend(data,25);
    for(int64_t i=10;i<Len(data);i++) {
        data[i]=2*i;
    }
    struct AllocatedArray *a= GetArray(data);
    void *raw = (void*)a;
    void *end = a->end;;
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


int part1(void *array) {
    return 42;
}

int part2(void *array) {
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
