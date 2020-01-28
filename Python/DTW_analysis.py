# DTW analysis and comparison of DTW algorithms
# inclusion of DTW-derivative for greater accuracy
# includes constrained DTW, memoized DTW, and LB_keogh

import numpy as np
import scipy as sp
import scipy.signal as signal
from scipy.signal import savgol_filter
from time import process_time


def DDTW_SakoeChiba(X, Y):
    m = len(X)
    n = len(Y)
    # print('\nDistance of Derivatives:')
    w = max(5, abs(m - n))
    path = []
    path_elements = []
    r = 0
    s = 0
    metric = 0
    ddtw = np.matrix(np.ones((n,m)) * np.inf)
    ddtw[0, 0] = 0
    for i in range(1, n):
        for j in range(max(1, i - w), min(m, i + w)):
            ddtw[i, j] = 0
    for i in range(1, n):
        for j in range(max(1, i - w), min(m, i + w)):
            # if (i == 0 and j == 0) or (i == 0 and j != 0) or (j == 0 and i != 0):
            #     continue
            if i + 1 >= n or j + 1 >= m:
                continue
            # elif ddtw[i, j + 1] == np.inf or ddtw[i, j - 1] == np.inf or ddtw[i + 1, j] == np.inf or ddtw[i - 1, j] == np.inf:
            #     continue
            else:
                if ddtw[i, j] == np.inf:
                    continue
                elif ddtw[i, j + 1] == np.inf or ddtw[i + 1, j] == np.inf:
                    derDist = float((X[j] - Y[i]) ** 2)
                else:
                    dX = ((X[j] - X[j - 1]) + ((X[j + 1] - X[j - 1]) / 2.0)) / 2.0
                    dY = ((Y[i] - Y[i - 1]) + ((Y[i + 1] - Y[i - 1]) / 2.0)) / 2.0
                    derDist = float((dX - dY) ** 2)
                ddtw[i, j] = derDist + min(min(ddtw[i - 1, j], ddtw[i - 1, j - 1]), ddtw[i, j - 1])
                if ddtw[i - 1, j] == min(min(ddtw[i - 1, j], ddtw[i - 1, j - 1]), ddtw[i, j - 1]):
                    r = i - 1
                elif ddtw[i, j - 1] == min(min(ddtw[i - 1, j], ddtw[i - 1, j - 1]), ddtw[i, j - 1]):
                    s = j - 1
                else:
                    r = i - 1
                    s = j - 1
        # path.append([s, r])
        # path_elements.append(ddtw[r, s])
        # metric += ddtw[r, s]
        if ddtw[r, s] == np.inf:
            print(i, '\t', metric)
        else:
            path.append([s, r])
            path_elements.append(ddtw[r, s])
            metric += ddtw[r, s]
    WarpingCost = (metric ** 0.5)
    print('Warping path with the Sakoe-Chiba constraint:')
    for [m, n], x in zip(path, path_elements):
        print(m, '\t', n, '\t', x)
    print()
    print('length of warping:', len(path))
    print()
    print('Sakoe-Chiba warping cost:\n', WarpingCost)


def DTW_memoization_SakoeChiba(X, Y):
    m = len(X)
    n = len(Y)
    w = max(7, abs(m - n))
    path = []
    r = 0
    s = 0
    metric = 0
    dtw = np.matrix(np.ones(2, m) * np.inf)
    dtw[1, 0] = np.inf
    dtw[0, 0] = 0
    p = 0
    c = 1
    for i in range(1, n):
        for j in range(max(1, i - w), min(m, i + w)):
            if i + 1 >= n or j + 1 >= m:
                break
            elif dtw[i, j + 1] == np.inf or dtw[i, j - 1] == np.inf:
                continue
            else:
                Dist = float((X[i - 1] - Y[j - 1]) ** 2)
                dtw[i, j] = Dist + min(min(dtw[p, j], dtw[p, j - 1]), dtw[c, j - 1])
                if dtw[i - 1, j] == min(dtw[p, j - 1], dtw[p, j],
                                                     dtw[c, j - 1]):
                    r = p
                elif dtw[i, j - 1] == min(dtw[p, j - 1], dtw[p, j],
                                                       dtw[c, j - 1]):
                    s = j - 1
                else:
                    r = p
                    s = j - 1
        temp = p
        p = c
        c = temp
        path.append([s, r])
        metric += ddtw[r, s]
    WarpingCost = (metric ** 0.5) / len(path)
    print('Warping path with memoization_Sakoe-Chiba constraint:')
    for [m, n] in path:
        print(m, '\t', n)
    print()
    print('memoization_Sakoe-Chiba warping cost:\n', WarpingCost)


def lower_bound_of_keogh(s1, s2_ref):
    LB_sum = 0
    r = 5
    best_ever = LB_sum
    print('Length of reference wave:', len(s2_ref))
    print('Length of wave to compare:', len(s1))
    for iterator, i in enumerate(s1):
        if (iterator + r) > len(s2_ref):
            lower_bound = min(s2_ref[(iterator - r if iterator - r >= 0 else 0):(iterator)])
            upper_bound = max(s2_ref[(iterator - r if iterator - r >= 0 else 0):(iterator)])
        else:
            lower_bound = min(s2_ref[(iterator - r if iterator - r >= 0 else 0):(iterator + r)])
            upper_bound = max(s2_ref[(iterator - r if iterator - r >= 0 else 0):(iterator + r)])

        if i > upper_bound:
            LB_sum = LB_sum + (i - upper_bound) ** 2
        elif i < lower_bound:
            LB_sum = LB_sum + (i - lower_bound) ** 2

    # return sqrt(LB_sum)
    print('------------------------------------------------------------------------')
    print('Warping cost of LB_Keogh:', LB_sum ** 0.5)


def main():
    X = []
    Y = []
    print('enter X wave')
    while True:
        a = float(input())
        if a == -79:
            break
        X.append(a)
    t1_start = process_time()
    X_sm = savgol_filter(X, 101, 4)
    t1_stop = process_time()
    print('Time taken to filter firt wave:', t1_stop - t1_start)
    print('enter Y wave')
    while True:
        a = float(input())
        if a == -79:
            break
        Y.append(a)
    t2_start = process_time()
    Y_sm = savgol_filter(Y, 101, 4)
    t2_stop = process_time()
    print('Time taken to filter second wave:', t2_stop - t2_start)
    t4_start = process_time()
    lower_bound_of_keogh(Y_sm, X_sm)
    t4_stop = process_time()
    print('------------------------------------------------------------------------')
    print('Time taken for LB_Keogh comparison:', t4_stop - t4_start)
    print('------------------------------------------------------------------------')
    # t3_start = process_time()
    # DDTW_SakoeChiba(X_sm, Y_sm)
    # t3_stop = process_time()
    # print('------------------------------------------------------------------------')
    # print('Time taken for Sakoe_Chiba_DDTW comparison:', t3_stop - t3_start)
    # print('------------------------------------------------------------------------')
    # DTW_memoization_SakoeChiba()

main()
