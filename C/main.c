#include <stdio.h>
#include <time.h>
#include<stdlib.h>


int randr( int min,  int max)
{
    double scaled = (double)rand()/RAND_MAX;
    return (max - min +1)*scaled + min;
}

int uniform_distribution(int low, int high) {
    double myRand = rand() / (1.0 + RAND_MAX);
    int range = high - low + 1;
    int myRand_scaled = (myRand * range) + low;
    return myRand_scaled;
}

int main()
{
    struct timespec tmp;
    clock_gettime(CLOCK_MONOTONIC, &tmp);
    srand(tmp.tv_nsec);
    int a = 0;
    for (int i=0;i<10000;i++){
        int rr=randr(1000,4000);
        a+=rr;
        printf("%d\n",rr);
    }

    printf("@@@\nmean : %d\n", a/10000); // to quickly check the uniformity

    printf("\n\n");
    int b = 0;
    for (int i=0;i<10000;i++){
        int r2=uniform_distribution(1000, 4000);
        b+=r2;
        //printf("r2=%d\n",r2);
    }

    printf("###\nmean 2 : %d\n", b/10000);

    return 0;
}
