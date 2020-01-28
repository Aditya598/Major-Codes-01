import numpy as np
from numpy import diff
import sys
import scipy.signal as signal
from scipy.signal import savgol_filter

np.set_printoptions(threshold=sys.maxsize)


def first_order_derivative(input_wave):
    dx = 0.001
    dy = diff(input_wave) / dx
    return dy


def desaturate(input_wave):
    for i in range(len(input_wave)):
        if input_wave[i] <= -5:
            input_wave[i] = 0.0
    # for i in input_wave:
    #     print(i)


def main():
    inner_break = False
    outer_break = False
    input_wave = []
    input_wave_matrix = []
    fod_matrix = []
    filtered_signal = []
    rows = 0
    while True:
        input_wave = []
        print('\nenter wave')
        while True:
            c = float(input())
            if c == 5:
                inner_break = True
                rows += 1
                break
            if c == 10:
                outer_break = True
                rows += 1
                break
            else:
                inner_break = False
                outer_break = False
                input_wave.append(c)
        desaturate(input_wave)
        input_wave = savgol_filter(input_wave, 101, 4)
        input_wave_matrix = np.append(input_wave_matrix, input_wave, axis=0)
        fod_matrix = np.append(fod_matrix, first_order_derivative(input_wave), axis=0)
        if inner_break: continue
        if outer_break: break
    # input_wave_matrix.reshape(rows, 2500)
    print('smoothed waves:')
    print(input_wave_matrix)
    print()


main()