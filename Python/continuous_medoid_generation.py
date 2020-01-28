import matplotlib.pyplot as plt
from time import process_time

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
            i  = 0.00001
        a += 1 / i
    return (len(sample) / a)

def distance_between_waves(wave_means):
    cost_mat = []
    for j in wave_means:
        cost = 0
        for i in wave_means:
            cost += ((j - i)**2)**0.5
        cost_mat.append(cost / len(wave_means))
    return cost_mat

def sort_by_means(costs, labels):
    for i in range(len(costs)):
        j = i + 1
        for j in range(len(costs)):
            if costs[i] < costs[j]:
                tmp = costs[i]
                costs[i] = costs[j]
                costs[j] = tmp
                tmpL = labels[i]
                labels[i] = labels[j]
                labels[j] = tmpL
    return labels[0]

def medoid_wave(waves, labels):
    mean_mat = []
    for i in range(len(waves)):
        mean_mat.append(harmonic_mean(waves[i]))
    mean_costs = distance_between_waves(mean_mat)
    top_label = sort_by_means(mean_costs, labels)
    return waves[top_label]

def main():
    wave = []
    wave_mat = []
    medoid = []
    labels = []
    n_toMed = 5
    iterator = 0
    iterator_2 = 0
    while True:
        print('enter wave')
        if iterator == 5:
            print('Resetting . . .')
            iterator = 0
            plt.title('waves at this point')
            for s in wave_mat:
                plt.plot(range(0, len(s)), s)
            plt.draw()
            plt.figure()
            plt.title('medoid')
            plt.plot(range(0, len(medoid)), medoid)
            plt.show()
            print('Continue?')
            b = input()
            if b in ['y', 'Y']: continue
            else: break
        if iterator == 3:
            plt.title('middle examination')
            for s in wave_mat:
                plt.plot(range(0, len(s)), s)
            plt.draw()
            plt.figure()
            plt.title('middle examination')
            plt.plot(range(0, len(medoid)), medoid)
            plt.show()
        wave = accept_wave()
        if iterator_2 >= 5:
            wave_mat[iterator] = wave
            labels[iterator] = iterator
        else:
            wave_mat.append(wave)
            labels.append(iterator)
        medoid = medoid_wave(wave_mat, labels)
        iterator += 1
        iterator_2 += 1


main()
