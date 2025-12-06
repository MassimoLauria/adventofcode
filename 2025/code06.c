// Advent of Code 2025 day XX

#include <stdlib.h>
#include <stdint.h>
#include <stdio.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <time.h>
#include <ctype.h>
#include <assert.h>

char example[]="123 328  51 64 \n 45 64  387 23 \n  6 98  215 314\n*   +   *   +  \n";

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
    pack->cap=capacity;
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

int getNumbers1(int64_t  *buffer, char *p,int rows,int stride) {
    assert (rows<=4);
    int i,j,width;
    width=0;
    Resize(buffer,rows);
    for(i=0;i<rows;i++) {
        j=0;
        buffer[i]=0;
        while(p[j]==' ') j++;
        while(p[j]>='0' && p[j]<='9') {
            buffer[i] *= 10;
            buffer[i] += p[j]-'0';
            j++;
        }
        p+=stride;
        width=width<j?j:width;
    }
    return width;
}

int getNumbers2(int64_t  buffer[4], char *block,int rows,int stride) {
    assert (rows<=4);
    int i,j;
    char *p;
    int width=0;
    p=block;
    for(i=0;i<rows;i++) {
        j=0;
        while(p[j]==' ') j++;
        while(p[j]>='0' && p[j]<='9') j++;
        p+=stride;
        width=width<j?j:width;
    }
    Resize(buffer,width);
    for(j=0;j<width;j++) {
        p=block+width-1-j;
        buffer[j]=0;
        i=0;
        while(*p==' ') { p+=stride; i++;}
        while(*p>='0' && *p<='9' && i<rows) {
            buffer[j] *= 10;
            buffer[j] += *p-'0';
            p+=stride;
            i++;
        }
    }
    return width;
}

int64_t workhard(ssize_t textlen, char *text,
                 int (*getNumbers)(int64_t[4],char *,int,int)
                 ) {
    int linesize;
    int64_t *buffer= (int64_t*)AllocArray(4,4,sizeof(int64_t));
    int64_t tmp,total;
    int c,rows,cols,i;
    int stride;
    char *ops,*p=text;
    while(*p!='\n') p++;
    linesize = p-text;
    p++;
    rows=1;
    stride=linesize+1;
    while(*p!='+' && *p!='*') { rows++; p+=stride; }
    cols=0;
    ops=p;
    char *w=p;
    while(*p!='\n') {
        if (*p!=' ') { *w=*p; w++; cols++;}
        p++;
    }
    *w='\n';
    p=text;
    total=0;
    for(c=0;c<cols;c++) {
        p+=getNumbers(buffer,p,rows,stride)+1;
        switch(ops[c]) {
        case '*':
            tmp=1;
            for(i=0;i<Len(buffer);i++) tmp*=buffer[i];
            break;
        case '+':
            tmp=0;
            for(i=0;i<Len(buffer);i++) tmp+=buffer[i];
            break;
        }
        total+=tmp;
    }
    return total;
}

int64_t part1(ssize_t textlen, char *text) {
    return workhard(textlen,text,getNumbers1);
}

int64_t part2(ssize_t textlen, char *text) {
    return workhard(textlen,text,getNumbers2);
}

int main() {
    clock_t start,end;
    int64_t res;
    char *buffer;
    start=clock();
    buffer=load_file("input06.txt");
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
