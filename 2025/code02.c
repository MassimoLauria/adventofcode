// Advent of Code 2025 day 02
/*
Part1 - example   : 1227775554                - 0.000002
Part1 - challenge : 30599400849               - 0.000006
Part2 - example   : 4174379265                - 0.000005
Part2 - challenge : 46270373595               - 0.000013
*/

#include <stdlib.h>
#include <stdint.h>
#include <stdio.h>
#include <sys/stat.h>
#include <time.h>

int64_t POW[19];

int64_t Ranges[300];

char example[]="11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124\n";

ssize_t Len(void * mem) {
    return  *((ssize_t*)mem-1);
}

int64_t getNum(char *s,char *e) {
    int64_t val=0;
    while (s<e) {
        val = *s-'0' + val*10;
        s++;
    }
    return val;
}


void* AllocLen(ssize_t n, ssize_t objsize) {
    if (n==0 || objsize==0) {
        perror("AllocLen does not accept zero sized data");
        exit(EXIT_FAILURE);
    }
    void *mem = malloc(sizeof(n)+objsize*n);
    if (mem==NULL) {
        perror("AllocLen failed");
        exit(EXIT_FAILURE);
    }
    return mem;
}


int parse_text(ssize_t textlen, char *p) {
    char *textend=p+textlen;
    char *bots,*tops;
    int idx=0;
    int digits;
    int64_t bot,top;
    while(p<textend) {
        // find delimiters of number pairs
        while( (*p < '0' || *p > '9') && p<textend) p++;
        if (p>=textend) break;
        bots=p;
        while( *p >= '0' && *p <= '9') p++;
        bot=getNum(bots,p);
        digits=p-bots;
        p++;
        tops=p;
        while( *p >= '0' && *p <= '9') p++;
        top=getNum(tops,p);
        Ranges[idx++]=bot;
        if (digits < (p-tops)) {
            Ranges[idx++]=POW[digits]-1;
            Ranges[idx++]=POW[digits];
        }
        Ranges[idx++]=top;
        p++;
    }
    return idx;
}

int digitsOf(int64_t n) {
    if (n<1) return 0;
    int d=1;
    while(n>=POW[d]) d++;
    return d;
}

int64_t repeating(int64_t a, int64_t b,int patternlen,int totallen) {
    if ((totallen % patternlen) != 0) return 0;
    int64_t base=0;
    int64_t delta=0;
    int64_t sum;
    int64_t botHi=a/POW[totallen-patternlen];
    for (int i=0;i< totallen/patternlen;i++) {
        base  = base*POW[patternlen] + botHi;
        delta  = delta*POW[patternlen] + 1;
    }
    sum=0;
    if (base<a) base+= delta;
    while(base<=b) {
        sum+=base;
        base += delta;
    }
    return sum;
}


int64_t part1(ssize_t textlen, char *text) {
    int N = parse_text(textlen,text);
    int64_t bot,top,digits,sum=0;

    for(int i=0;i<N;i+=2) {
        bot = Ranges[i];
        top = Ranges[i+1];
        digits = digitsOf(bot);
        if (digits % 2 ==1) continue;
        sum += repeating(bot,top, digits/2,digits);
    }
    return sum;
}

int64_t part2(ssize_t textlen, char *text) {
    int N = parse_text(textlen,text);
    int64_t sum=0;
    int64_t tmp=0;
    int64_t bot,top,digits;
    for(int i=0;i<N;i+=2) {
        bot = Ranges[i];
        top = Ranges[i+1];
        digits = digitsOf(bot);
        tmp=0;
        switch(digits) {
        case 2: case 3: case 5: case 7: case 11:
            tmp+=repeating(bot,top,1,digits);
            break;
        case 4: case 8:
            tmp+=repeating(bot,top,digits/2,digits);
            break;
        case 6:
            tmp+=repeating(bot,top,2,6);
            tmp+=repeating(bot,top,3,6);
            tmp-=repeating(bot,top,1,6);
            break;
        case 9:
            tmp+=repeating(bot,top,3,9);
            break;
        case 10:
            tmp+=repeating(bot,top,2,10);
            tmp+=repeating(bot,top,5,10);
            tmp-=repeating(bot,top,1,10);
            break;
        default:
            tmp=0;
        }
        sum+=tmp;
    }
    return sum;
}


/* Gives a memory address containing the byte length of the file as an ssize_t,
   and all the bytes of the file.

   E.g. a 64bit integer and x bytes

   |IIIIIIII|BBBBBBBBBBBB....|

*/
char* load_file(char *filename) {
    struct stat st;
    if (stat(filename,&st)==-1) {
        perror(filename);
        exit(EXIT_FAILURE);
    }
    ssize_t n=st.st_size;
    char *buffer = AllocLen(n, sizeof(char));
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


int main() {

    POW[0]=1;
    for(int i=1; i<sizeof(POW)/sizeof(int64_t);i++) {
        POW[i]=POW[i-1]*10;
    }

    clock_t start,end;
    int64_t res;
    char *buffer;

    start=clock();
    buffer = load_file("input02.txt");
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
