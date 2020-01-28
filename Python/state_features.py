# Program for extracting few of the features of the EOG waveform

def accept_wave():
    wave = []
    while True:
        a = float(input())
        if a == -10: break
        wave.append(a)
    return wave


def harmonic_mean(sample):
    a = 0
    for i in sample:
        if i == 0:
            i = 0.00001
        a += 1 / i
    return (len(sample) / a)


def arithmetic_mean(sample):
    avg = 0
    for i in range(len(sample)):
        avg += i
    avg = avg / len(sample)


def std_dev(sample):
    sample_moments = 0
    for i in sample:
        if i == 0:
            i = 0.00001
        sample_moments += 1 / i
    sample_moments = 1 / (sample_moments / len(sample))
    var_sq = 0
    for i in sample:
        if i == 0:
            i = 0.00001
        var_sq += ((1 / i) - sample_moments) ** 2
    var_sq = 1 / (var_sq / len(sample))
    sd = (var_sq / (len(sample) * (sample_moments ** 4))) ** 0.5


def main():
    wave = []
    wave_mat = []
    feature_vector_2 = []
    feature_vector_3 = []
    feature_mat_1 = []
    feature_mat_2 = []
    feature_mat_3 = []
    visible_states = []
    looper = True
    while looper:
        print('enter wave')
        wave = accept_wave()
        if -20 in wave:
            looper = False
            wave.remove(-20)
        minpos = wave.index(min(wave))
        visible_state_2 = wave[: minpos]
        visible_state_3 = wave[minpos:]
        wave_mat.append(wave)
        feature_vector_2.append(harmonic_mean(visible_state_2))
        feature_vector_2.append(std_dev(visible_state_2))
        # avg_samples_to_valley = arithmetic_mean(visible_state_2)
        feature_vector_2.append(len(visible_state_2))
        feature_vector_3.append(harmonic_mean(visible_state_3))
        feature_vector_3.append(std_dev(visible_state_3))
        # avg_samples_from_valley = arithmetic_mean(visible_state_3)
        feature_vector_3.append(len(visible_state_3))
        feature_mat_2.append(feature_vector_2)
        feature_mat_3.append(feature_vector_3)
        feature_vector_2 = []
        feature_vector_3 = []
    print('features of state 2:')
    for i in feature_mat_2:
        print(i)
    print('features of state 3:')
    for i in feature_mat_3:
        print(i)


main()
