# Acquires real time data from EOG sensors for comparison and classification 


import numpy as np
import random
import time
import serial
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neighbors.nearest_centroid import NearestCentroid


ser = serial.Serial('COM7', 1000000)
model_knn = []
model_kncn = []
modelCreated_knn = False
modelCreated_kncn = False
predictBuf_knn = []
predictBuf_kncn = []
pbDetected_knn = 0
pbDetected_kncn = 0
inputWave = []

def euclideanDistance(x, y):
   return ((x - y)**2)**0.5

def oneMedoid(meanMat, waveMat, labels):
    costMat = []
    for j in range(len(meanMat)):
        cost = 0
        c = meanMat[j]
        for i in meanMat:
            dist = euclideanDistance(c, i)
            cost += dist
        avgCost = cost / len(meanMat)
        costMat.append(avgCost)
    print('average distance costs:')
    print(costMat)
    for i in range(len(costMat)):
        j = i + 1
        for j in range(len(costMat)):
            if costMat[i] < costMat[j]:
                tmp = costMat[i]
                costMat[i] = costMat[j]
                costMat[j] = tmp
                tmpL = labels[i]
                labels[i] = labels[j]
                labels[j] = tmpL
    print('sorted average distance costs:')
    print(costMat)
    print('sorted  labels:')
    print(labels)
    # meanMat = []
    # print('Medoid wave:')
    return waveMat[labels[0]]

def harmonicMean(sample, meanMat):
    a = 0
    for i in range(len(sample)):
        a += 1 / sample[i]
    return len(sample) / a


def DDTW(X, Y, lX, lY):
    derDist = np.zeros((lY, lX))
    # print('\nDistance of Derivatives:')
    for i in range(lY):
        a = []
        for j in range(lX):
            if (i == 0 and j == 0) or (i == 0 and j != 0) or (j == 0 and i != 0):
                derDist[i, j] = int((X[j] - Y[i]) ** 2)
            elif i + 1 >= lY or j + 1 >= lX:
                derDist[i, j] = int((X[j] - Y[i]) ** 2)
            else:
                dX = ((X[j] - X[j - 1]) + ((X[j + 1] - X[j - 1]) / 2.0)) / 2.0
                dY = ((Y[i] - Y[i - 1]) + ((Y[i + 1] - Y[i - 1]) / 2.0)) / 2.0
                derDist[i, j] = int((dX - dY) ** 2)
    # print(derDist)
    dtw = np.zeros((lY, lX))
    # print('\nAccumulated distances')
    for i in range(lY):
        b = []
        for j in range(lX):
            if i == 0 and j == 0:
                dtw[i, j] = derDist[i, j]
            elif i == 0 and j != 0:
                dtw[i, j] = derDist[i, j] + dtw[i, j - 1]
            elif j == 0 and i != 0:
                dtw[i, j] = derDist[i, j] + dtw[i - 1, j]
            else:
                dtw[i, j] = derDist[i, j] + min(min(dtw[i - 1, j], dtw[i - 1, j - 1]), dtw[i, j - 1])
    # print(dtw)
    path, cost = path_cost(X, Y, dtw, derDist)
    # print('\nWarping path')
    # print(path)
    # print('\nCost')
    # print(cost / 100000)
    return cost / 100000


def path_cost(x, y, accumulated_cost, distances):
    path = [[len(x) - 1, len(y) - 1]]
    cost = 0
    i = len(y) - 1
    j = len(x) - 1
    while i > 0 and j > 0:
        if i == 0:
            j = j - 1
        elif j == 0:
            i = i - 1
        else:
            if accumulated_cost[i - 1, j] == min(accumulated_cost[i - 1, j - 1], accumulated_cost[i - 1, j],
                                                 accumulated_cost[i, j - 1]):
                i = i - 1
            elif accumulated_cost[i, j - 1] == min(accumulated_cost[i - 1, j - 1], accumulated_cost[i - 1, j],
                                                   accumulated_cost[i, j - 1]):
                j = j - 1
            else:
                i = i - 1
                j = j - 1
        path.append([j, i])
    path.append([0, 0])
    # print('Cost indices:')
    for [m, n] in path:
        # print(m, '\t', n)
        cost += distances[n, m]
    return path, cost


def kNCN(x, Y, newData):
    global model_kncn, modelCreated_kncn, predictBuf_kncn, pbDetected_kncn
    if not modelCreated_kncn:
        print('Training Initiated. . .')
        feature = np.array(x, dtype=np.float32)
        label = np.array(Y, dtype=np.int)
        model_kncn = NearestCentroid(metric='euclidean', shrink_threshold=None)
        model_kncn.fit(feature, label)
        modelCreated_kncn = True
        print('Training Complete')
    else:
        predicted = model_kncn.predict(newData)
        predictBuf_kncn = np.array(predicted, dtype=np.int)
        for i in range(len(predictBuf_kncn)):
            if predictBuf_kncn[i] == 0:
                for j in newData:
                    print('>>>Cost:', j, '\n>>>Prediction: Prolonged')
                    pbDetected_kncn += 1
                    print('Prolonged detection number', pbDetected_kncn)
            elif predictBuf_kncn[i] == 1:
                for j in newData:
                    print('>>>Cost:', j, '\n>>>Prediction: Right')
            elif predictBuf_kncn[i] == 2:
                for j in newData:
                    print('>>>Cost:', j, '\n>>>Prediction: Left')
            else:
                print('>>>hmmm...')


def kNN(x, Y, newData):
    global model_knn, modelCreated_knn, predictBuf_knn, pbDetected_knn
    if not modelCreated_knn:
        print('Training Initiated. . .')
        feature = np.array(x, dtype=np.float32)
        label = np.array(Y, dtype=np.int)
        model_knn = KNeighborsClassifier(n_neighbors=10)
        model_knn.fit(feature, label)
        modelCreated_knn = True
        print('Training Complete')
    else:
        predicted = model_knn.predict(newData)
        predictBuf_knn = np.array(predicted, dtype=np.int)
        for i in range(len(predictBuf)):
            if predictBuf_knn[i] == 0:
                for j in newData:
                    print('>>>Cost:', j, '\n>>>Prediction: Prolonged')
                    pbDetected_knn += 1
                    print('Prolonged detection number', pbDetected_knn)
            elif predictBuf_knn[i] == 1:
                for j in newData:
                    print('>>>Cost:', j, '\n>>>Prediction: Right')
            elif predictBuf_knn[i] == 2:
                for j in newData:
                    print('>>>Cost:', j, '\n>>>Prediction: Left')
            else:
                print('>>>hmmm...')


def AcquireWave():
    global inputWave, ser
    readStream = str(ser.readline().strip(), 'utf-8')
    while not readStream.startswith('*******'):
        if readStream.isnumeric():
            if int(readStream) == 0: inputWave.append(1)
            else: inputWave.append(int(readStream))
            print(readStream)
        elif readStream.startswith('@@') or readStream.startswith('Neg'):
            print(readStream)
        readStream = str(ser.readline().strip(), 'utf-8')


def main():
    global inputWave, modelCreated_knn, modelCreated_kncn, predictBuf_knn, predictBuf_kncn
    waveMatrix = []
    meanMatrix = []
    labels = []
    labelCount = 0
    secondComing = False
    iterator = 0
    postTrainCount = 0
    medoidFound = False
    medoid = []
    n_test = 200
    n_train = 10
    n_forMedoid = 8
    n_total = n_forMedoid + n_train + n_test
    featureVector = []
    classVector = []
    testVector = []
    rlStart = False
    rightLimit = 10
    leftLimit = 10
    rlCounter = 0
    trainAgain = False

    while True:
        inputWave = []
        AcquireWave()
        if len(inputWave) <= 10:
            print('Improper Wave')
            continue
        else:
            print('Input Wave:')
            for i in inputWave: print(i)
            iterator += 1
            print('Iteration Number', iterator)
        if iterator <= n_forMedoid and not rlStart:
            waveMatrix.append(inputWave)
            meanMatrix.append(harmonicMean(inputWave, meanMatrix))
            labelCount += 1
            labels.append(labelCount)
        if iterator == n_forMedoid + 1 and not rlStart:
            print('set of waves:')
            print(waveMatrix)
            print('\nGenerating Medoid wave. . .')
            medoid = oneMedoid(meanMatrix, waveMatrix, labels)
            medoidFound = True
            print('Medoid Wave:')
            for i in medoid: print(i)
        elif iterator <= n_forMedoid + n_train and medoidFound and not rlStart:
            a = []
            a.append(DDTW(inputWave, medoid, len(inputWave), len(medoid)))
            # a.append(len(inputWave))
            featureVector.append(a)
            classVector.append(0)
            if iterator == n_forMedoid + n_train:
                rlStart = True
                print('--------------------------Prolonged waves obtained--------------------------')
        elif rlStart:
            if rlCounter == (rightLimit + leftLimit) - 1:
                print('Input samples\tClassses')
                for i, j in zip(featureVector, classVector): print(i, '\t', j)
                # kNN(featureVector, classVector, testVector)  # first call - model trained
                kNCN(featureVector, classVector, testVector)  # first call - model trained
                rlStart = False
                continue
            a = []
            a.append(DDTW(inputWave, medoid, len(inputWave), len(medoid)))
            # a.append(len(inputWave))
            featureVector.append(a)
            if rlCounter < rightLimit:
                classVector.append(1)
                print('Right Count:', rlCounter)
            elif rlCounter < rightLimit + leftLimit and rlCounter >= rightLimit:
                classVector.append(2)
                print('Left Count:', rlCounter - rightLimit)
            rlCounter += 1
        elif iterator <= n_total and medoidFound and not rlStart:
            a = []
            a.append(DDTW(inputWave, medoid, len(inputWave), len(medoid)))
            # a.append(len(inputWave))
            testVector.append(a)
            # kNN(featureVector, classVector, testVector)
            kNCN(featureVector, classVector, testVector)
            testVector = []



if __name__ == '__main__':
    main()
