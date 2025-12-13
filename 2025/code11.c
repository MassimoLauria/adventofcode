// Advent of Code 2025 day XX

#include <stdlib.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <time.h>
#include <assert.h>
#include <ctype.h>
#include <string.h>


char example[]=\
    "aaa: you hhh\n"
    "you: bbb ccc\n"
    "bbb: ddd eee\n"
    "ccc: ddd eee fff\n"
    "ddd: ggg\n"
    "eee: out\n"
    "fff: out\n"
    "ggg: out\n"
    "hhh: ccc fff iii\n"
    "iii: out\n";

char example2[]=\
    "svr: aaa bbb\n"
    "aaa: fft\n"
    "fft: ccc\n"
    "bbb: tty\n"
    "tty: ccc\n"
    "ccc: ddd eee\n"
    "ddd: hub\n"
    "hub: fff\n"
    "eee: dac\n"
    "dac: fff\n"
    "fff: ggg hhh\n"
    "ggg: out\n"
    "hhh: out\n";

#define MAXVERTICES 26*26*26
#define MAXEDGES    1800
#define UNREACH     0

struct graph {
    int adj[MAXVERTICES];
    int deg[MAXVERTICES];
    int E[MAXEDGES];
    // dfs and topological sort stuff
    int vstart[MAXVERTICES];
    int vend[MAXVERTICES];
    int dfs_reached;
    int sorted[MAXVERTICES];
};

void clear_graph(struct graph *G) {
    memset(G, 0, sizeof(struct graph));
}

int id(char *name) {
    return 26*26*(name[0]-'a')+
              26*(name[1]-'a')+
                 (name[2]-'a');
}

void revid(char *buf,int id) {
    buf[0]=id / (26*26) +'a';
    buf[1]=((id % (26*26))/26) + 'a';
    buf[2]=id % 26 +'a' ;
}


void parse_graph(struct graph *G,size_t textlen,char *text) {
    int *D=G->deg;
    assert(D[0]==0);
    int *E=G->E;
    int *A=G->adj;
    char *p=text;
    char *end=text+textlen;
    int edgeoffset=0;
    int v;

    while(p<end-1) {
        // read vertex
        assert(isalpha(*p));
        v = id(p);
        p+=3;
        assert(*p==':');

        // edges
        A[v] = edgeoffset;
        p++;
        while(*p!='\n') {
            p++;
            assert(isalpha(*p));
            D[v]++;
            E[edgeoffset] = id(p);
            edgeoffset++;
            p+=3;
        }
        p++;
    }
}



void DFS(struct graph *G,int v,int time) {
    int j,w;
    assert(G->vstart[v]==0);
    assert(G->vend[v]==0);
    G->vstart[v]=time;
    time++;
    for (j=G->adj[v];j<G->adj[v]+G->deg[v];j++) {
        w = G->E[j];
        assert(G->vstart[w]==0 || G->vend[w]!=0);
        if (G->vstart[w]!=0) continue;
        DFS(G,w,time);
        time = G->vend[w]+1;
    }
    G->vend[v]=time;
    G->sorted[G->dfs_reached++]=v;
}


size_t file_size(char *filename) {
    struct stat st;
    if (stat(filename,&st)==-1) {
        perror(filename);
        exit(EXIT_FAILURE);
    }
    size_t n=(size_t)st.st_size;
    return n;
}

char *read_file(char *filename, size_t n) {
    char *buffer = (char*)malloc(n*sizeof(char));
    FILE *f = fopen(filename,"r");
    if (f==NULL) {
        perror(filename);
        exit(EXIT_FAILURE);
    }
    size_t fs;
    fs=fread(buffer,1,n,f);
    if (fs!=n) {
        fprintf(stderr,"Non ha letto tutti i bytes: ne ha letti %lu invece di %lu\n",fs,n);
        exit(EXIT_FAILURE);
    }
    return buffer;
}

void topological_sort(struct graph *G, int start) {
    int tmp;
    int i=0;
    DFS(G,start,1);
    int j=G->dfs_reached-1;
    while(i<j) {
        tmp = G->sorted[i];
        G->sorted[i] = G->sorted[j];
        G->sorted[j] = tmp;
        i++; j--;
    }
}


int64_t howmanypaths(struct graph *G, int64_t from, int64_t to, int64_t *paths) {
    memset(paths,0,sizeof(int64_t)*MAXVERTICES);
    int i,j,v;
    paths[from]=1;
    for(i=0;i<G->dfs_reached;i++) {
        v = G->sorted[i];
        for(j=G->adj[v];j<G->adj[v]+G->deg[v];j++) {
            paths[G->E[j]]+=paths[v];
        }
    }
    return paths[to];
}

int64_t part1(size_t textlen, char *text) {
    struct graph G;
    clear_graph(&G);
    parse_graph(&G, textlen, text);
    char you[4]="you";
    char out[4]="out";
    topological_sort(&G,id(you));
    int64_t paths[MAXVERTICES];
    return howmanypaths(&G,id(you),id(out),paths);
}

int64_t part2(size_t textlen, char *text) {
    struct graph G;
    clear_graph(&G);
    parse_graph(&G, textlen, text);
    char svr[4]="svr";
    char fft[4]="fft";
    char dac[4]="dac";
    char out[4]="out";
    topological_sort(&G,id(svr));
    int64_t paths[MAXVERTICES];
    int64_t a = howmanypaths(&G,id(svr),id(fft),paths);
    int64_t b = howmanypaths(&G,id(fft),id(dac),paths);
    int64_t c = howmanypaths(&G,id(dac),id(out),paths);
    return a*b*c;
}

int main() {
    clock_t start,end;
    int64_t res;
    char *buffer;
    size_t filelen;

    start=clock();
    filelen  = file_size("input11.txt");
    buffer   = read_file("input11.txt",filelen);
	end = clock();
    printf("Loading data                                  - %f\n", ((double)(end-start))/CLOCKS_PER_SEC);

    start=clock();
	res = part1(sizeof(example),example);
	end = clock();
    printf("Part1 - example   : %-25ld - %f\n", res, ((double)(end-start))/CLOCKS_PER_SEC);

    start=clock();
    res = part1(filelen, buffer );
	end = clock();
    printf("Part1 - challenge : %-25ld - %f\n", res, ((double)(end-start))/CLOCKS_PER_SEC);

    start=clock();
	res = part2(sizeof(example2),example2);
	end = clock();
    printf("Part2 - example   : %-25ld - %f\n", res, ((double)(end-start))/CLOCKS_PER_SEC);

    start=clock();
    res = part2(filelen, buffer );
	end = clock();
    printf("Part2 - challenge : %-25ld - %f\n", res, ((double)(end-start))/CLOCKS_PER_SEC);

    return 0;
}
