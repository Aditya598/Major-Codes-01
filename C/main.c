//code to generate simulated waves of subject drowsy behavior and get out DTW costs by comparing two generated waves in
//real time to get a sense of how it might turn out ot work  in embedded C later on

#include <stdio.h>
#include <stdbool.h>
#include <time.h>
#include <math.h>
#include <stdlib.h>

int xWave[500];
int yWave[500];


int uniform_distribution(int min, int max) {
    double scaled = (double) rand() / RAND_MAX;
    return (max - min + 1) * scaled + min;
}

#define simNegLimit (int)(100 + (uniform_distribution(1000, 4000) % 100))
#define min(a, b) (a < b ? a : b)
#define max(a, b) (a > b ? a : b)


int simNegCount = 0, simPrevVal = 512, simCurrentWaveCount = 0, simMaxOutCount = 0, differential = 0;
bool simWaveStart = false;

int simInput() {

    struct timespec tmp;
    clock_gettime(CLOCK_MONOTONIC, &tmp);
    srand(tmp.tv_nsec);

    int limbuff = simNegLimit;

    if (simNegCount < limbuff) {
        simNegCount++;
        if (simNegCount >= limbuff) simWaveStart = true;
        return 512;
    } else {

        if (simWaveStart) {
            differential = uniform_distribution(0, 150) * 0.3 + uniform_distribution(0, 60) * 0.7;
            if (simCurrentWaveCount == 0) {
                if (simPrevVal < 512 && (simPrevVal + differential) >= 512) {
                    simNegCount = simCurrentWaveCount = simMaxOutCount = differential = 0;
                    limbuff = simNegLimit;
                    simPrevVal = 512;
                    simWaveStart = false;
                } else {
                    simPrevVal = min(1023, simPrevVal + differential);
                    if (simPrevVal >= 1023) {
                        simCurrentWaveCount = 1;
                        simMaxOutCount = uniform_distribution(0, 75);
                    }
                }
            } else if (simCurrentWaveCount == 1) {

                simMaxOutCount--;
                if (simMaxOutCount == 0) {
                    simCurrentWaveCount = 2;
                    simPrevVal = 512;
                }
            } else if (simCurrentWaveCount == 2) {
                simPrevVal = max(0, simPrevVal - differential);
                if (simPrevVal <= 0) {
                    simCurrentWaveCount = 3;
                    simMaxOutCount = uniform_distribution(0, 75);
                }
            } else if (simCurrentWaveCount == 3) {
                simMaxOutCount--;
                if (simMaxOutCount == 0) {
                    simCurrentWaveCount = 0;
                    simPrevVal = 0;
                }

            }

        }
        return simPrevVal;
    }
}

void DDTW(int X[], int Y[], int lX, int lY) {

    /**int **DerDist = (int **) malloc(lY * sizeof(int *));
    for (int (k) = 0; (k) < lX; ++(k)) {
        DerDist[k] = (int *) malloc(lX * sizeof(int));
    }**/

    float DerDist[500][500];

    printf("\n");
    printf("-------------------------------------------------------------------------------------------------------------");
    printf("\n");
    printf("Derivative Distance:\n");



    for (int i = 0; i < lY; i++) {
        for (int j = 0; j < lX; j++) {
            if ((i == 0 && j == 0) || (i == 0 && j != 0) || (j == 0 && i != 0)) DerDist[i][j] = (float)pow((xWave[j] - yWave[i]), 2);
            else if (i + 1 >= lY || j + 1 >= lX) DerDist[i][j] = (float)pow((xWave[j] - yWave[i]), 2);
            else {
                double Dx = ((xWave[j] - xWave[j - 1]) + ((xWave[j + 1] - xWave[j - 1]) / 2.0)) / 2.0;
                double Dy = ((yWave[i] - yWave[i - 1]) + ((yWave[i + 1] - yWave[i - 1]) / 2.0)) / 2.0;
                DerDist[i][j] = (float)pow((Dx - Dy), 2);
            }

            //printf("%d\t", DerDist[i][j]);
        }
        //printf("\n");
    }


    /*int **DTW = (int **) malloc(lY * sizeof(int *));
    for (int (k) = 0; (k) < lX; ++(k)) {
        DTW[k] = (int *) malloc(lX * sizeof(int));
    }**/

    float DTW[500][500];

    printf("\n");
    printf("-------------------------------------------------------------------------------------------------------------");
    printf("\n");
    printf("Accumulated Distance:\n");
    for (int i = 0; i < lY; i++) {
        for (int j = 0; j < lX; j++) {
            if (i == 0 && j == 0) DTW[i][j] = DerDist[i][j];
            else if (i == 0 && j != 0)DTW[i][j] = DerDist[i][j] + DTW[i][j - 1];
            else if (j == 0 && i != 0)DTW[i][j] = DerDist[i][j] + DTW[i - 1][j];
                /* DTW[i][0] = inf;
                 DTW[0][j] = inf;*/
            else DTW[i][j] = DerDist[i][j] + min(min(DTW[i - 1][j], DTW[i - 1][j - 1]), DTW[i][j - 1]);
            //printf("%d\t", DTW[i][j]);
        }
        //printf("\n");
    }

    double cost = 0;
    int i01 = lY - 1;
    int j01 = lX - 1;
    int count01 = 0;
    printf("\n\n");
    printf("lX = %d\nlY = %d\n", lX, lY);
    printf("optimal path:\n");
    while (i01 > 0 && j01 > 0) {
        if (i01 == 0) --j01;
        else if (j01 == 0) --i01;
        else {
            if (DTW[i01 - 1][j01] == min(min(DTW[i01 - 1][j01 - 1], DTW[i01 - 1][j01]), DTW[i01][j01 - 1])) --i01;
            else if (DTW[i01][j01 - 1] == min(min(DTW[i01 - 011][j01 - 1], DTW[i01 - 1][j01]), DTW[i01][j01 - 1]))
                --j01;
            else {
                --i01;
                --j01;
            }
        }
        cost += DerDist[j01][i01];

        //printf("%d %d\n", j01, i01);
        ++count01;
    }
    //printf("0 0");
    //free(DerDist);
    //free(DTW);

    printf("\n\n");
    printf("cost:\n");
    printf("%f", (cost / 100000.00));

}

int main() {
    int elementCount = 0;
    int negCount = 0;
    bool waveFlag = false, waveEnd = false;
    //printf("enter wave one\n")
    while (1) {
        int buf = simInput();
        //printf("%d\n", buf);
        if (buf - 512 > 150 || waveFlag) {
            if (buf != 512) {
                xWave[elementCount] = buf;
                elementCount++;
                //printf("%d\n", xWave[--elementCount]);
            }
            waveFlag = true;
            if (buf == 512) {
                negCount++;
                if (negCount >= 15) {
                    break;
                }
            } else if (negCount <= 15) {
                negCount = 0;
                continue;
            }
        }
    }

    int lX = elementCount;
    //printf("###\nlength of x wave: %d\n###", lX);

    printf("\n\n");
    //printf("first wave\n");
    //for (int i = 0; i < elementCount; ++i) printf("%d\n", xWave[i]);
    printf("--------------------------------------------------------------------");
    printf("\n\n");

    elementCount = 0;
    waveFlag = false;
    //printf("\nenter second wave\n");

    while (1) {
        int buf = simInput();
        //printf("%d\n", buf);
        if (buf - 512 > 150 || waveFlag) {
            if (buf != 512) {
                yWave[elementCount] = buf;
                elementCount++;
                //printf("%d\n", yWave[--elementCount]);
            }
            waveFlag = true;
            if (buf == 512) {
                negCount++;
                if (negCount >= 15) {
                    break;
                }
            } else if (negCount <= 15) {
                negCount = 0;
                continue;
            }
        }
    }

    int lY = elementCount;
    //printf("@@@\nlength of y wave: %d\n@@@", lY);

    printf("\n\n");
    //printf("second wave\n");
    //for (int i = 0; i < elementCount; ++i) printf("%d\n", yWave[i]);

    printf("------------------------ PHASE TWO ---------------------------------------");

    DDTW(xWave, yWave, lX, lY);
}



