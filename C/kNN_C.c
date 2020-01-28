// a C language implementation of the k-Nearest Neighbors algorithm

#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#define ARRAYSIZE(a) (sizeof(a) / sizeof(a[0]))

float trainingSet[50][2];
float testSet[1][2];
float neighborDistance[50][2];
//int kNN = 5;
int length__;

void printMatrix(float a[][2]) {
    int length = length__;

    for (int i = 0; i < length; i++) {
        for (int j = 0; j < 2; j++) {
            printf("%f\t", a[i][j]);
        }
        printf("\n");
    }
}

void equalCondition(int k){
    k += 1;
    int pb = 0, r = 0, l = 0;
    for (int i = 0; i < k; i++) {
        if (neighborDistance[i][1] == 1) ++pb;
        else if(neighborDistance[i][1] == -1) ++r;
        else ++l;
    }
    if (pb > r && pb > l) printf("\n%f is Prolonged\n", testSet[0][0]);
    else if(r > pb && r > l) printf("\n%f is Right\n", testSet[0][0]);
    else if(l > pb && l > r) printf("\n%f is Left\n", testSet[0][0]);
}

void predict() {
    int kNN = ceil(sqrt(length__));
    printf("\nValue of k = %d\n", kNN);
    int pb = 0, r = 0, l = 0;
    for (int i = 0; i < kNN; i++) {
        if (neighborDistance[i][1] == 1) ++pb;
        else if(neighborDistance[i][1] == -1) ++r;
        else ++l;
    }
    if (pb > r && pb > l) printf("\n%f is Prolonged\n", testSet[0][0]);
    else if(r > pb && r > l) printf("\n%f is Right\n", testSet[0][0]);
    else if(l > pb && l > r) printf("\n%f is Left\n", testSet[0][0]);
    else if(pb == r || pb ==l) equalCondition(kNN);
}

void sorting(int trainLength) {
    float temp[2];
    for (int i = 0; i < trainLength; i++) {
        for(int j = i + 1; j < trainLength; j++){
            if (neighborDistance[i][0] > neighborDistance[j][0] && neighborDistance[j][0] != 0){
                for(int k = 0; k < 2; k++){
                    temp[k] = neighborDistance[i][k];
                    neighborDistance[i][k] = neighborDistance[j][k];
                    neighborDistance[j][k] = temp[k];
                }
            }
        }
    }
    printf("\nsorted distances:\n");
    for (int i = 0; i < trainLength; i++) {
        for (int j = 0; j < 2; j++) {
            printf("%f\t", neighborDistance[i][j]);
        }
        printf("\n");
    }
    predict();
}

void getDistance(int trainLength, int testLength) {
    for (int i = 0; i < testLength; i++) {
        for (int j = 0; j < trainLength; j++) {
            neighborDistance[j][0] = sqrt(pow((testSet[i][0] - trainingSet[j][0]), 2));
            neighborDistance[j][1] = testSet[i][1] + trainingSet[j][1];
        }
    }
    printf("\ndistance of neighbors:\n");
    for (int i = 0; i < trainLength; i++) {
        for (int j = 0; j < 2; j++) {
            printf("%f\t", neighborDistance[i][j]);
        }
        printf("\n");
    }
    sorting(trainLength);
}

void loadData() {
    int l = 0;
    printf("enter prolonged\n");
    while (1) {
        float a;
        scanf("%f", &a);
        if (a == -3)break;
        trainingSet[l][0] = a;
        trainingSet[l][1] = 1;
        ++l;
    }
    printf("\nenter Right\n");
    while (1) {
        float a;
        scanf("%f", &a);
        if (a == -3)break;
        trainingSet[l][0] = a;
        trainingSet[l][1] = -1;
        ++l;
    }
    printf("\nenter Left\n");
    while (1) {
        float a;
        scanf("%f", &a);
        if (a == -3)break;
        trainingSet[l][0] = a;
        trainingSet[l][1] = -2;
        ++l;
    }
    length__ = l;
    printf("\nlength of training data set: %d\n", length__);

    printf("\nenter test data\n");
    scanf("%f", &testSet[0][0]);

    printf("\ntraining data:\n");
    printMatrix(trainingSet);
    printf("\ntest data:\n");
    printMatrix(testSet);

    getDistance(l, 1);
}

int main() {
    loadData();
}

