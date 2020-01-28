// A simulation of the EOG system output at a particular arrangement of electrodes 

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <stdbool.h>

int uniform_distribution(int low, int high) {
    double myRand = rand() / (1.0 + RAND_MAX);
    int range = high - low + 1;
    int myRand_scaled = (myRand * range) + low;
    return myRand_scaled;
}

int rand_range(int limit) {
    int divisor = RAND_MAX / (limit + 1);
    int returnValue = 0;
    while (returnValue > limit) {
        returnValue = rand() / divisor;
    }
    return returnValue;
}
int random(int min, int max){
    return min + rand() / (RAND_MAX / (max - min + 1) + 1);
}
#define simNegLimit (int)(100 + (uniform_distribution(1000, 4000) % 100))
#define min(a,b) (a < b ? a : b)
#define max(a,b) (a > b ? a : b)

int simNegCount = 0; simPrevVal = 512; simCurrentWaveCount = 0; simMaxOutCount = 0; differential;
bool simWaveStart = false;

/**int simNegCount = 0, simPrevVal = 512, simCurrentWaveCount = 0, simMaxOutCount = 0, differential = 0;
bool simWaveStart = false;**/

void simInput() {

    int limbuff = simNegLimit;

    printf("\nINITIAL STATE:");
    printf("\nsimNegCount: %d\n",simNegCount);
    printf("simCurrentWaveCount: %d\n",simCurrentWaveCount);
    printf("simMaxOutCount: %d\n",simMaxOutCount);
    printf("differential: %d\n",differential);
    printf("simPrevVal: %d\n",simPrevVal);
    printf("simWaveStart: %d\n",simWaveStart);
    printf("simNegLimit: %d\n", limbuff);
    printf("******************************************************");

    if (simNegCount < limbuff) {
        ++simNegCount;
        if (simNegCount >= limbuff) simWaveStart = true;
        //simPrevVal = 512;
        //return 512;
    } else {

        if (simWaveStart) {
            differential = random(0, 150) * 0.3 + random(0, 60);
            printf("\n$$$\ndifferential after start of wave: %d\n", differential);
            //      Serial.print(differential);
            //      Serial.print("\t");
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
                        simMaxOutCount = random(0, 75);
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
                    simMaxOutCount = random(0, 75);
                }
            } else if (simCurrentWaveCount == 3) {
                simMaxOutCount--;
                if (simMaxOutCount == 0) {
                    simCurrentWaveCount = 0;
                    simPrevVal = 0;
                }

            }

        }

    }
    printf("\nsimNegCount: %d\n",simNegCount);
    printf("simCurrentWaveCount: %d\n",simCurrentWaveCount);
    printf("simMaxOutCount: %d\n",simMaxOutCount);
    printf("differential: %d\n",differential);
    printf("simPrevVal: %d\n",simPrevVal);
    printf("simWaveStart: %d\n",simWaveStart);
    printf("simNegLimit: %d\n", limbuff);
}

int main()
{
    for(int i = 0; i < 1000; i++){
        printf("------------------------------------------------------------------------------------------------");
        simInput();
        printf("------------------------------------------------------------------------------------------------");
        printf("\n\n");
    }
}
