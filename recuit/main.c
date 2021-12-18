#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <time.h>
#include <math.h>
#include <pthread.h>

#define MAX_THREAD 12

struct Solution{
    int * sol;
    int * size;
};
typedef struct Solution Solution;

struct SolverArgs{  
    int * input_numbers;
    Solution * init_sol;
    int N;
    int B;
    int E;
    float T;
    float Tf;
    float decreasing;
    int step;
    float mix;
};
typedef struct SolverArgs SolverArgs;

float randomFloat()
{
      float r = (float)rand()/(float)RAND_MAX;
      return r;
}

void freeSolution(Solution * sol){
    free(sol->sol);
    free(sol->size);
    free(sol);
}

//From : https://stackoverflow.com/questions/3893937/sorting-an-array-in-c
int compare( const void* a, const void* b)
{
     int int_a = * ( (int*) a );
     int int_b = * ( (int*) b );
     if ( int_a == int_b ) return 0;
     else if ( int_a < int_b ) return 1;
     else return -1;
}

int cost(Solution* sol, int N, int B, int E){
    int* list = malloc(B*E*sizeof(int));
    int index = 0;
    for(int i = 0; i < N; i++){
        for(int j = 0; j < sol->size[i]; j++){
            list[index] = sol->sol[i*(B*E-N) + j];
            index++;
        }
    }
    qsort(list, B*E, sizeof(int), compare);
    int c = 0;
    for(int i = 0; i < B; i++){
        c += list[i * E];
    }
    free(list);
    return c;
}

int * split(int x, int n, int m){
    int * res = malloc(n * sizeof(int));
    if (x == 0){
        for(int i = 0; i < n; i++){
            res[i]=0;
        }
    }
    else if(n == 1){
        res[0] = x;
    } else {
        int reste = x % m;
        int total = x / m;
        for(int i = 0; i < n-1; i++){
            int h = total-(n-i);
            int rnd = rand()%h + 1; 
            total -= rnd;
            res[i] = rnd*m;
        }
        res[n-1] = total*m + reste;
    }

    return res;
}

int * equalSplit(int x, int n, int m){
    int * res = malloc(n * sizeof(int));
    if(x == 0){
        for(int i = 0; i < n; i++){
            res[i] = 0;
        }
    }else if( x%n == 0){
        int part = x/n;
        for(int i = 0; i < n; i++){
            res[i] = part;
        }
    } else {
        int zp = n - (x % n);
        int pp = x/n;
        for(int i = 0; i < n; i++){
            if(i >= zp){
                res[i] = pp+1;
            } else {
                res[i] = pp;
            } 
        }
    }
    return res;
}

int * mixSplit(int x, int n, float mix){
    int * res = malloc(n * sizeof(int));
    int px = x*mix;
    int * eqSplit = equalSplit(px,n,1);
    int * spt = split(x - px,n,1);
    for(int i = 0; i < n; i++){
        res[i] = eqSplit[i] + spt[i];
    }
    free(eqSplit);
    free(spt);

    return res;
}   


Solution* getInitSol(int * input_numbers, int N, int B, int E){
    int r = N;
    int c = B*E-N;
    int* sol = malloc((r * c) * sizeof(int));
    int* size = malloc(N * sizeof(int));
    Solution* solution = malloc(sizeof(Solution));
    solution->sol = sol;
    solution->size = size;
    // Init solution with data
    for(int i = 0; i < N; i++){
        sol[i*c] = input_numbers[i]; 
        size[i] = 1;
    }
    // Split data to have a valid solution
    for(int i = 0; i < (B * E - N); i++){
        int index = i%N;
        int end = size[index] - 1;
        int num = sol[index*(B*E-N) + end];
        int* num_split = equalSplit(num, 2, 1);
        sol[index*(B*E-N) + end] = num_split[0];
        sol[index*(B*E-N) + end + 1] = num_split[1];
        size[index] += 1;
        free(num_split);
    }
    return solution;
}

bool correctSolution(Solution * sol, int * input_numbers, int N, int B, int E){
    int c = B*E-N;
    int count=0;
    for(int i = 0; i < N; i++){
        int sum = 0;
        for(int j = 0; j < sol->size[i]; j++){
            if(sol->sol[i*c + j] <= 0) 
                return false;
            sum += sol->sol[i*c + j]; 
            count+=1;
        }
        if(sum != input_numbers[i])
            return false;
    }
    if(count != B*E)
        return false;
    return true;
}

void printSol(Solution* sol, int N, int B, int E){
    printf("[");
    for (int i=0; i<N; i++){
        printf("[");
        int len=sol->size[i];
        for(int j=0; j<len; j++){
            printf("%d,",sol->sol[i*(B*E-N) + j]);
        }
        printf("]");
    }
    printf("]\n");
}

Solution * deepcopy(Solution * sol, int N, int B, int E){
    int r = N;
    int c = B*E-N;
    Solution * copy = malloc(sizeof(Solution));
    copy->sol = malloc((r * c) * sizeof(int));
    copy->size = malloc(N * sizeof(int));

    for(int i = 0; i < N; i++){
        for(int j = 0; j < sol->size[i]; j++){
            copy->sol[i*c + j] = sol->sol[i*c + j];
        }
        copy->size[i] = sol->size[i];
    }

    return copy;
}

Solution * randomNeighbor(int * input_numbers,Solution * sol, 
    int N, int B, int E, float mix){
    int c = B*E-N;
    Solution * neighbor = deepcopy(sol,N,B,E);
    //we generate a neighbor by swaping the number of split of two number
    //we choose two number to swap
    int i = 0;
    int j = 0;
    while (i == j){
        i = rand()%N;
        j = rand()%N;
    }
    int total_split = sol->size[i] + sol->size[j];
    int i_split;
    int j_split;
    if(total_split > B*E-N){
        i_split = total_split/2;
    } else {
        i_split = rand()%(total_split-1) + 1; 
    }
    j_split = total_split - i_split;

    int * new_i = mixSplit(input_numbers[i], i_split, mix);
    int * new_j = mixSplit(input_numbers[j], j_split, mix);

    neighbor->size[i] = i_split;
    for(int a = 0; a < i_split; a++){
        neighbor->sol[i * c + a] = new_i[a]; 
    }

    neighbor->size[j] = j_split;
    for(int a = 0; a < j_split; a++){
        neighbor->sol[j * c + a] = new_j[a]; 
    }

    free(new_i);
    free(new_j);
    return neighbor;
}

float prob(float de, float T){
    return pow(2.718,de/T);
}

void * solve(void* args){
    SolverArgs * input = (SolverArgs*) args;
    int * input_numbers = input->input_numbers;
    Solution * init_sol = input->init_sol;
    int N = input->N;
    int B = input->B;
    int E = input->E;
    float T = input->T;
    float Tf = input->Tf;
    float decreasing = input->decreasing;
    int step = input->step;
    float mix = input->mix;

    Solution * current_sol = deepcopy(init_sol,N,B,E);
    int current_cost = cost(init_sol,N,B,E);
    Solution * best_sol = deepcopy(init_sol,N,B,E);
    int best_cost = current_cost;
    Solution * neighbor_sol;
    while(T > Tf){
        for(int k=0; k < step; k++){
            neighbor_sol = randomNeighbor(input_numbers,current_sol,N,B,E,mix);
            int neighbor_cost = cost(neighbor_sol,N,B,E);
            if((neighbor_cost < current_cost) || 
                (randomFloat()< prob(current_cost-neighbor_cost,T))){
                freeSolution(current_sol);
                current_sol = deepcopy(neighbor_sol,N,B,E);
                current_cost = neighbor_cost;
                if(best_cost > current_cost){
                    freeSolution(best_sol);
                    best_sol = deepcopy(current_sol,N,B,E);
                    best_cost = current_cost;
                }
            }
            freeSolution(neighbor_sol);
        }
        T *= decreasing;
    }
    return (void *) best_sol;
}

int main(int argc, char const *argv[]){
    srand(time(NULL));
    char loc[32];
    int score_prof[10] ={5243, 8190, 3897, 9978, 4966, 15030, 7194, 239778, 229428, 226788};

    for(int i = 1; i <= 10; i++){
        snprintf(loc, 32, "../samples/data%d.dat", i);
        FILE *f = fopen(loc,"r");
        int bufferLength = 255;
        char buffer[bufferLength];

        fgets(buffer, bufferLength, f);
        int N = atoi(buffer);
        fgets(buffer, bufferLength, f);
        int E = atoi(buffer);
        fgets(buffer, bufferLength, f);
        int B = atoi(buffer);

        int * data = malloc(N * sizeof(int));
        for(int j=0; j < N; j++){
            fgets(buffer, bufferLength, f);
            data[j] = atoi(buffer);
        }

        fclose(f);

        Solution * init_sol = getInitSol(data,N,B,E);
        pthread_t tid[MAX_THREAD];
        SolverArgs args[MAX_THREAD];
        void * temp[MAX_THREAD];

        // CREATING THREADS
        for(int j = 0; j < MAX_THREAD; j++){
            args[j].input_numbers=data;
            args[j].init_sol=init_sol;
            args[j].N = N;
            args[j].B = B;
            args[j].E = E;
            args[j].T = 100;
            args[j].Tf = 0.01;
            args[j].decreasing = 0.99;
            args[j].step = 10000;
            args[j].mix = (float)j * 1/(float)(MAX_THREAD-1);
            pthread_create(&tid[j], NULL, solve, (void *)&args[j]); 
        }

        Solution * bestSolution;
        int bestc = 99999999;
        // PRINTING VALUE OF ALL THREAD WHEN THEY ARE ALL FINISHED
        for(int j = 0; j < MAX_THREAD; j++){
            pthread_join(tid[j], &temp[j]);
            Solution * solution = (Solution*) temp[j];
            int c = cost(solution, N, B, E);

            if(c < bestc){
                bestSolution = solution;
                bestc = c;
            } else {
                freeSolution(solution);
            }
        }
        int prof = score_prof[i-1];
        int diff = prof - bestc;
        bool correct = correctSolution(bestSolution,data, N,B,E);
        float p = ( (float)(prof - bestc) / prof) * 100;
        printf("Problem data%d.dat : %d vs %d | diff: %d => %.6f | correct: %d\n",i,bestc,prof,diff,p,correct);
        printSol(bestSolution,N,B,E);
    }
    return 0;
}