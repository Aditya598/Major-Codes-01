import numpy as np
from numpy import trapz
import matplotlib.pyplot as plt
from matplotlib import style
from random import choices
from collections import Counter
import seaborn as sns
import sys
np.set_printoptions(threshold=sys.maxsize)
sns.set(color_codes=True)


end_training = False

def accept_wave():
    global end_training
    wave = []
    while True:
        a = float(input())
        if a == -10: break
        if a == -20:
            end_training = True
            break
        wave.append(a)
    # for i in wave: print(i)
    return wave

def divide_in_states(wave):
    state_x = []
    state_y = []
    state_z = []
    x = False
    y = False
    z = False
    a = []
    b = []
    c = []
    _max = wave[0]
    _min = wave[0]

    for i in range(len(wave)):
        if (wave[i] > 0.05):
            x = False
            a.append(wave[i])
            _max = max(_max, wave[i])

        if (wave[i] < -0.05):
            x = False
            b.append(wave[i])
            _min = min(_min,wave[i])

        if x and _min <= -0.15:
            state_y.append(b)
            b = []
            _min = wave[i]

        if x and _max >= 0.15:
            state_z.append(a)
            a = []
            _max = wave[i]

        if x:
            state_x.append(c)
            c = []

        if (wave[i] < 0.05 and wave[i] > -0.05):
            c.append(wave[i])
            x = True
    for i in range(len(state_y)):
        buf = state_y[i]
        mn = min(buf)
        if mn > -0.15:
            del state_y[i]
        elif (len(state_y) > len(state_z)):
            auc = []
            for i in range(len(state_y)):
                buf = trapz((state_y[i]), dx=1)
                auc.append(buf)
            del state_y[auc.index(min(auc))]
            break
    for i in range(len(state_z)):
        buf = state_z[i]
        mx = max(buf)
        if mx < 0.15:
            del state_z[i]
        elif (len(state_z) > len(state_y)):
            auc = []
            for i in range(len(state_z)):
                buf = trapz((state_z[i]), dx=1)
                auc.append(buf)
            del state_z[auc.index(min(auc))]
            break
    return state_x, state_y, state_z

def get_sample_frequencies(sample):
    tmp = Counter(sample)
    tmp_1 = []
    for key in tmp.keys():
        tmp_1.append([key, tmp[key]])
    return tmp_1

def get_sample_probabilities(sample):
    tmp = []
    _sum = 0
    for i in sample:
        _sum += i[1]
    for i in sample:
        tmp.append([i[0], i[1]/_sum])
    return tmp

def state_transition_elements(state):
    tmp = []
    for x in state:
        if len(x) > 1:
            tmp.append(x[len(x) - 1])
        else:
            tmp.append(x[0])
    freq_tmp = get_sample_frequencies(tmp)
    prob_tmp = get_sample_probabilities(freq_tmp)
    return prob_tmp

def get_future_elements(state, known_elements):
    tmp = []
    for idx, i in enumerate(known_elements):
        tmp.append([])
        tmp[idx].append(i)
        tmp[idx].append([])
        for j in range(len(state)):
            if state[j] == i:
                for k in range(j + 1, j + 1 + len(known_elements)):
                    if k >= len(state):
                        break
                    tmp[idx][1].append(state[k])
    freq_tmp = []
    for i in tmp:
        freq_tmp.append([i[0], get_sample_frequencies(i[1])])
    prob_tmp = []
    for i in freq_tmp:
        for x, j in enumerate(i):
            if x == 1:
                prob_tmp.append([i[0], get_sample_probabilities(j)])
    return prob_tmp, freq_tmp

def distributed_generation(population, weights, state_number, k_value):
    samples = choices(population, weights, k=k_value)
    plt.title('Randomly generated state %d values and their frequency'%state_number)
    plt.xlabel('EOG values')
    plt.ylabel('Frequency')
    sns.distplot(samples, rug=True)
    plt.show()

def main():
    global end_training
    training_seq = []
    s1 = []
    s2 = []
    s3 = []
    st_12_13 = []
    st_21 = []
    st_31 = []
    state_1_allsamples = []
    state_2_allsamples = []
    state_3_allsamples = []
    plt.style.use('seaborn-bright')
    # print('^^^^^^^^^^^^^^^^')
    # print(plt.style.available)

    while not end_training:
        print('enter training sequence')
        training_seq = accept_wave()
        s1, s2, s3 = divide_in_states(training_seq)
        st_12_13 = state_transition_elements(s1)
        st_21 = state_transition_elements(s2)
        st_31 = state_transition_elements(s3)
        for i in s1:
            for j in i:
                state_1_allsamples.append(j)
        for i in s2:
            for j in i:
                state_2_allsamples.append(j)
        for i in s3:
            for j in i:
                state_3_allsamples.append(j)

    state_1_freq = get_sample_frequencies(state_1_allsamples)
    state_2_freq = get_sample_frequencies(state_2_allsamples)
    state_3_freq = get_sample_frequencies(state_3_allsamples)
    print('state 1 elements and their frequencies')
    for i in state_1_freq:
        print(i)
    print('state 2 elements and their frequencies')
    for i in state_2_freq:
        print(i)
    print('state 3 elements and their frequencies')
    for i in state_3_freq:
        print(i)

    state_1_probs = get_sample_probabilities(state_1_freq)
    state_2_probs = get_sample_probabilities(state_2_freq)
    state_3_probs = get_sample_probabilities(state_3_freq)
    print('state 1 elements and their probabilities')
    for i in state_1_probs:
        print(i)
    print('state 2 elements and their probabilities')
    for i in state_2_probs:
        print(i)
    print('state 3 elements and their probabilities')
    for i in state_3_probs:
        print(i)

    print('state transition 1 -> 2, 1 -> 3 elements and their probabilities')
    for i in st_12_13:
        print(i)
    print('state transition 2 -> 1 elements and their probabilities')
    for i in st_21:
        print(i)
    print('state transition 3 -> 1 elements and their probabilities')
    for i in st_31:
        print(i)

    plt.title('State 1')
    plt.plot(state_1_allsamples)
    plt.show()
    plt.title('State 2')
    plt.plot(state_2_allsamples)
    plt.show()
    plt.title('State 3')
    plt.plot(state_3_allsamples)
    plt.show()

    plt.title('Histogram of EOG values')
    plt.xlabel('EOG Values')
    plt.ylabel('Frequencies')
    sns.distplot(state_1_allsamples, rug=True)
    sns.distplot(state_2_allsamples, rug=True)
    sns.distplot(state_3_allsamples, rug=True)
    plt.show()

    state_1_probs.sort()
    state_2_probs.sort()
    state_3_probs.sort()
    plt.title('Probability distribution of EOG values')
    plt.xlabel('EOG Values')
    plt.ylabel('Probability')
    plt.plot(*zip(*state_1_probs))
    plt.plot(*zip(*state_2_probs))
    plt.plot(*zip(*state_3_probs))
    plt.show()

    # buf_2 = [row[0] for row in state_2_probs]
    # buf_3 = [row[0] for row in state_3_probs]
    future_probs_state_2, future_freq_state_2 = get_future_elements(state_2_allsamples, [row[0] for row in state_2_probs])
    future_probs_state_3, future_freq_state_3 = get_future_elements(state_3_allsamples, [row[0] for row in state_3_probs])
    print()
    print('future state 2 elements and their frequencies')
    for i in future_freq_state_2:
        print(i)
    print('future state 3 elements and their frequencies')
    for i in future_freq_state_3:
        print(i)
    print()
    print('future state 2 elements and their probabilities')
    for i in future_probs_state_2:
        print(i)
    print('future state 3 elements and their probabilities')
    for i in future_probs_state_3:
        print(i)
       
    intra_state_2_st = []
    intra_state_3_st = []
    
    # V = [0.06, 0.1, 0.08, 0.12, 0.14, 0.14, 0.16, 0.18, 0.2]
    # forward_prob, likely_sequence_of_states = forward_algorithm(V, [row[1] for row in state_2_probs], [row[1] for row in state_3_probs],
    #                                                             )

    distributed_generation([row[0] for row in state_2_probs], [row[1] for row in state_2_probs], 2, 10 ** 3)
    distributed_generation([row[0] for row in state_3_probs], [row[1] for row in state_3_probs], 3, 10 ** 3)

    

main()