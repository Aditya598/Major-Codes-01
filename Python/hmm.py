import matplotlib.pyplot as plt
from matplotlib import style
from random import choices
from collections import Counter
import seaborn as sns
sns.set(color_codes=True)
plt.style.use('seaborn-bright')

end_training = False
state_1_all = [[], [], []]
state_2_all = [[], [], []]
state_3_all = [[], [], []]

def accept_wave():
    global end_training
    print('enter training sequence')
    wave = []
    _type = '0'
    while True:
        a = input()
        if a in ['p', 'u', 'n']:
            _type = a
            continue
        if a == '-10':
            break
        if a == '-20':
            end_training = True
            break
        wave.append(float(a))
    return wave, _type

def state_divider(wave):
    s1 = []
    s2 = []
    s3 = []
    a = []
    b = []
    c = []
    x = False
    _max = wave[0]
    _min = wave[0]
    state = []
    for i in range(len(wave)):
        if wave[i] > 0.05:
            x = False
            a.append(wave[i])
            _max = max(_max, wave[i])
        if (wave[i] < -0.05):
            x = False
            b.append(wave[i])
            _min = min(_min,wave[i])
        if x:
            if b:
                s2.append(b)
                b = []
                _min = wave[i]
            if a:
                s3.append(a)
                a = []
                _max = wave[i]
            if c:
                s1.append(c)
                c = []
        if wave[i] < 0.05 and wave[i] > -0.05:
            c.append(wave[i])
            x = True
    state.append(s1)
    state.append(s2)
    state.append(s3)
    return state

def get_all_state_elements(state, _type):
    global state_1_all, state_2_all, state_3_all
    ind = 0
    if _type == 'p': ind = 0
    if _type == 'u': ind = 1
    if _type == 'n': ind = 2
    for idx, i in enumerate(state):
        for j in i:
            if idx == 0:
                for k in j:
                    state_1_all[ind].append(k)
            if idx == 1:
                for k in j:
                    state_2_all[ind].append(k)
            if idx == 2:
                for k in j:
                    state_3_all[ind].append(k)

def get_graph(sample, is_nd, title, xlabel, ylabel, sns_flag, xy_flag):
    a = []
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    if is_nd and not xy_flag:
        for i in sample:
            plt.title(title)
            plt.xlabel(xlabel)
            plt.ylabel(ylabel)
            for j in i:
                plt.plot(j)
            plt.show()
    else:
        plt.plot(sample)
        plt.show()
    if is_nd and xy_flag:
        plt.plot(*zip(*sample))
        plt.show()
    if sns_flag:
        sns.distplot(samples, rug=True)
        plt.show()

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

def main():
    global end_training, state_1_all, state_2_all, state_3_all
    training_seq = []
    states_p = []
    states_u = []
    states_n = []
    while True:
        training_seq, train_type = accept_wave()
        if train_type == 'p':
            states_p = state_divider(training_seq)
            for i in states_p:
                print(i)
            get_all_state_elements(states_p, train_type)
            print(state_1_all[0])
            get_graph(states_p, True, 'P Test', 'EOG Vaues', '', False, False)
            get_graph(state_1_all[0], False, 'All of state 1', 'EOG values', '', False, False)
            get_graph(state_2_all[0], False, 'All of state 2', 'EOG values', '', False, False)
            get_graph(state_3_all[0], False, 'All of state 3', 'EOG values', '', False, False)
        if train_type == 'u':
            states_u = state_divider(training_seq)
            get_all_state_elements(states_u, train_type)
        if train_type == 'n':
            states_n = state_divider(training_seq)
            get_all_state_elements(states_n, train_type)



main()