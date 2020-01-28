''''NN for classifying DTW cost outputs ***NEEDS MORE DATA AND FEATURES***'''

import numpy as np
from keras.models import Sequential
from keras.layers import Dense

print('enter training data:')
X = []
y = []
while True:
    a = []
    b = float(input())
    a.append(b)
    if b == -2:
        break
    else:
        X.append(a)
feature = np.array(X, dtype=np.float32)

print('enter targets:')
while True:
    a = []
    b = float(input())
    a.append(b)
    if b == -2:
        break
    else:
        y.append(a)
label = np.array(y, dtype=np.int)

model = Sequential()
model.add(Dense(12, input_dim=1, activation='relu'))
model.add(Dense(8, activation='relu'))
model.add(Dense(1, activation='sigmoid'))

model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

model.fit(feature, label, epochs=180, batch_size=10, verbose=0)
_, accuracy = model.evaluate(feature, label)
print('Accuracy: %.2f' % (accuracy*100))

print('enter new data:')
testSet = []
testBuf = []
while True:
    a = []
    b = float(input())
    a.append(b)
    if b == -2:
        break
    else:
        testBuf.append(a)
testSet = np.array(testBuf, dtype=np.float32)

print('length of test set is', len(testSet))

predictions = model.predict_classes(testSet)
pbDetected = 0
rightDetected = 0
leftDetected = 0
print('Prediction:')
for i in predictions: print(i)

print()
for i in range(len(predictions)):
    if predictions[i] == 0:
        print(testSet[i], 'is prolonged')
        pbDetected += 1
    elif predictions[i] == 1:
        print(testSet[i], 'is Right')
        rightDetected += 1
    else:
        print(testSet[i], 'is Left')
        leftDetected += 1

print('Number of prolonged detected:', pbDetected)
print('Number of right detected:', rightDetected)
print('Number of left detected:', leftDetected)
