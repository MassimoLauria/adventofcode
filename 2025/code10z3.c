// Advent of Code 2025 day XX

#include <stdlib.h>
#include <stdint.h>
#include <stdio.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <time.h>
#include <assert.h>

#include <z3.h>

char example[]=\
    "[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}\n"
    "[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}\n"
    "[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}\n";

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


int ABS(int x) { return x<0?-x:x;  }
int MIN(int a,int b) { return a<=b?a:b;  }
int MAX(int a,int b) { return a<b?b:a;   }

struct systemF2 {
    int n;
    int m;
    uint16_t b;
    uint16_t A[13];
};

struct systemZ {
    int n;
    int m;
    int A[10][13];
    int b[10];
};

#define NOSOLUTION 100000


void print_systemZ(struct systemZ *S);

int solve(struct systemZ *S) {
    return 0;
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
    while(*p!='[') { p++;}
    p++;
    while(*p!=']') { S->n++; p++;}
    while(*p!='{') {
        if (*p=='(') {
            for(int i=0;i<S->n;i++) S->A[i][S->m]=0;
        }
        if (*p>='0' && *p <='9') S->A[(*p-'0')][S->m]=1;
        if (*p==')') S->m++;
        p++;
    }
    p++;
    int tmp=0;
    int idx=0;
    do {
        if (*p>='0' && *p <='9') tmp= 10*tmp+(*p-'0');
        else {
            S->b[idx] = tmp;
            tmp=0;
            idx++;
        }
        p++;
    } while (*p!='\n');
    return ++p;
}


void print_systemZ(struct systemZ *S) {
    int i,j;
    for (i=0;i<S->n;i++) {
        for (j=0;j<S->m;j++) {
            printf("%u",S->A[i][j]);
        }
        printf("  =  %u   \n",S->b[i]);
    }
}


/**
 * Solves a linear system with 0/1 coefficients, finding non-negative
 * integer solutions that minimize the sum of variables.
 *
 * System format: A * x = b
 * where A[i][j] ∈ {0, 1}, b[i] > 0, x[j] >= 0
 */

int solve_linear_system(struct systemZ *S)
    /* int **coefficients,  // coefficients[i][j] is coefficient of var j in equation i
     * int *targets         // targets[i] is the RHS of equation i */
{
    int num_equations= S->n;
    int num_variables= S->m;

    Z3_config cfg = Z3_mk_config();
    Z3_context ctx = Z3_mk_context(cfg);
    Z3_del_config(cfg);

    Z3_optimize opt = Z3_mk_optimize(ctx);
    Z3_optimize_inc_ref(ctx, opt);

    // Create integer variables
    Z3_ast *vars = (Z3_ast*)malloc(num_variables * sizeof(Z3_ast));
    Z3_sort int_sort = Z3_mk_int_sort(ctx);

    for (int j = 0; j < num_variables; j++) {
        char var_name[32];
        snprintf(var_name, sizeof(var_name), "x%d", j);
        Z3_symbol s = Z3_mk_string_symbol(ctx, var_name);
        vars[j] = Z3_mk_const(ctx, s, int_sort);

        // Add non-negativity constraint: x[j] >= 0
        Z3_ast zero = Z3_mk_int(ctx, 0, int_sort);
        Z3_ast ge = Z3_mk_ge(ctx, vars[j], zero);
        Z3_optimize_assert(ctx, opt, ge);
    }

    // Add linear equations
    for (int i = 0; i < num_equations; i++) {
        // Build sum of coefficients * variables
        Z3_ast *terms = (Z3_ast*)malloc(num_variables * sizeof(Z3_ast));
        int term_count = 0;

        for (int j = 0; j < num_variables; j++) {
            if (S->A[i][j] == 1) {
                terms[term_count++] = vars[j];
            }
        }

        if (term_count > 0) {
            Z3_ast lhs = Z3_mk_add(ctx, term_count, terms);
            Z3_ast rhs = Z3_mk_int(ctx, S->b[i], int_sort);
            Z3_ast eq = Z3_mk_eq(ctx, lhs, rhs);
            Z3_optimize_assert(ctx, opt, eq);
        }

        free(terms);
    }

    // Minimize sum of all variables
    Z3_ast sum = Z3_mk_add(ctx, num_variables, vars);
    Z3_optimize_minimize(ctx, opt, sum);

    // Check satisfiability and get solution
    Z3_lbool result = Z3_optimize_check(ctx, opt, 0, NULL);

    int total = 0;

    if (result == Z3_L_TRUE) {
        Z3_model model = Z3_optimize_get_model(ctx, opt);
        Z3_model_inc_ref(ctx, model);

        for (int j = 0; j < num_variables; j++) {
            Z3_ast val;
            Z3_model_eval(ctx, model, vars[j], Z3_TRUE, &val);

            int int_val;
            Z3_get_numeral_int(ctx, val, &int_val);
            total += int_val;
        }
        Z3_model_dec_ref(ctx, model);
    } else if (result == Z3_L_FALSE) {
        printf("No solution exists (unsatisfiable)\n");
    } else {
        printf("Unknown result\n");
    }

    // Cleanup
    free(vars);
    Z3_optimize_dec_ref(ctx, opt);
    Z3_del_context(ctx);
    return total;
}

int64_t part1(size_t textlen, char *text) {
    char *p=text;
    struct systemF2 Axb;
    int total=0;
    uint16_t X;

    int howmany[1<<13];
    howmany[0]=0;
    for(X=1;X<(1<<13);X++) {
        howmany[X]= 1 + howmany[X&(X-1)];
    }

    while (*p=='[') {
        p=parse_systemF2(&Axb,p);
        uint16_t T=1<<Axb.m;
        assert(T<=(1<<13));
        int sol=Axb.m+1;
        for(X=0;X<T;X++) {
            if (sol<=howmany[X]) continue;
            if (evaluateF2(&Axb,X)==Axb.b) {
                sol=howmany[X];
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
    int optimal;
    int sum=0;
    while (*p=='[') {
        p=parse_systemZ(&Axb,p);
        optimal=solve_linear_system(&Axb);
        sum+=optimal;
    }
    return sum;
}


int main() {
    clock_t start,end;
    int64_t res;
    char *buffer;
    size_t filelen;

    start=clock();
    filelen  = file_size("input10.txt");
    buffer   = read_file("input10.txt",filelen);
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
	res = part2(sizeof(example),example);
	end = clock();
    printf("Part2 - example   : %-25ld - %f\n", res, ((double)(end-start))/CLOCKS_PER_SEC);

    start=clock();
    res = part2(filelen, buffer );
	end = clock();
    printf("Part2 - challenge : %-25ld - %f\n", res, ((double)(end-start))/CLOCKS_PER_SEC);

    return 0;
}
