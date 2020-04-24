# Python implementation of an ANN for our BE project. Based on the algorithm found at 
# https://machinelearningmastery.com/implement-backpropagation-algorithm-scratch-python/
# with major alterations to fit our needs

from math import exp
import random
from random import seed


def activation_function(x, derivative_flag):
    if not derivative_flag:
        return 1.0 / (1.0 + exp(-x))
    else:
        return x * (1.0 - x)
    

def activate_neuron(weights, inputs):
    activation = weights[-1]
    for i in range(len(weights) - 1):
        activation += weights[i] * inputs[i]
    return activation


def build_network(n_inputs, n_hidden_layers, n_hidden_nodes, n_outputs):
    network = []
    network.append([{'weights': [random.uniform(0, 1) for i in range(n_inputs + 1)]} for i in range(n_hidden_nodes)])
    for i in range(n_hidden_layers - 1):
        network.append([])
        for j in range(n_hidden_nodes):
            network[i + 1].append({'weights': []})
            for k in range(n_hidden_nodes + 1):
                network[i + 1][j]['weights'].append(random.uniform(0, 1))
    network.append([{'weights': [random.uniform(0, 1) for i in range(n_hidden_nodes + 1)]} for i in range(n_outputs)])
    return network


def get_dataset(n_samples):
    X = []
    for i in range(n_samples):
        if i <= int(n_samples / 2):
            X.append([random.uniform(-0.1, -0.2), random.uniform(0.1, 0.2), random.uniform(-0.1, -0.2),
                      random.uniform(0.3, 0.5),
                      random.uniform(-0.3, -0.5), random.uniform(1.5, 2.5), random.uniform(0.5, 1.5),
                      random.uniform(0.5, 1.5), random.uniform(0.8, 1.0), 1])
        else:
            X.append([random.uniform(-0.05, -0.15), random.uniform(0.05, 0.15), random.uniform(-0.05, -0.15),
                      random.uniform(0.3, 0.5),
                      random.uniform(-0.3, -0.5), random.uniform(1, 2), random.uniform(0.1, 1),
                      random.uniform(0.1, 1), random.uniform(0.5, 0.8), 0])
    return X


def forward_prop(network, feature_set):
    inputs = feature_set
    for layer in network:
        new_inputs = []
        for neuron in layer:
            activation = activate_neuron(neuron['weights'], inputs)
            neuron['output'] = activation_function(activation, derivative_flag=False)
            new_inputs.append(neuron['output'])
        inputs = new_inputs
    return inputs


def backprop(network, expected):
    new_network = network
    for i in reversed(range(len(new_network))):
        layer = new_network[i]
        errors = []
        if i != len(new_network) - 1:
            for j in range(len(new_network[i])):
                error = 0.0
                for neuron in new_network[i + 1]:
                    error += neuron['weights'][j] * neuron['delta']
                errors.append(error)
        else:
            for j in range(len(new_network[i])):
                errors.append(expected[j] - new_network[i][j]['output'])
        for j in range(len(new_network[i])):
            new_network[i][j]['delta'] = errors[j] * activation_function(new_network[i][j]['output'], True)
    return new_network


def update_weights(network, feature_set, alpha):
    new_network = network
    for i in range(len(new_network)):
        inputs = feature_set[: -1]
        if i != 0:
            inputs = [neuron['output'] for neuron in new_network[i - 1]]
        for k in range(len(new_network[i])):
            for j in range(len(inputs)):
                new_network[i][k]['weights'][j] += alpha * new_network[i][k]['delta'] * inputs[j]
            new_network[i][k]['weights'][-1] += alpha * new_network[i][k]['delta']
    return new_network


def predict(network, unknowns):
    outputs = forward_prop(network, unknowns)
    return outputs.index(max(outputs)), outputs


def get_dataset(n_samples):
    X = []
    for i in range(n_samples):
        if i <= int(n_samples / 2):
            X.append([random.uniform(-0.1, -0.2), random.uniform(0.1, 0.2), random.uniform(-0.1, -0.2),
                      random.uniform(0.3, 0.5),
                      random.uniform(-0.3, -0.5), random.uniform(1.5, 2.5), random.uniform(0.5, 1.5),
                      random.uniform(0.5, 1.5), random.uniform(0.8, 1.0), 1])
        else:
            X.append([random.uniform(-0.05, -0.15), random.uniform(0.05, 0.15), random.uniform(-0.05, -0.15),
                      random.uniform(0.3, 0.5),
                      random.uniform(-0.3, -0.5), random.uniform(1, 2), random.uniform(0.1, 1),
                      random.uniform(0.1, 1), random.uniform(0.5, 0.8), 0])
    return X


dataset = get_dataset(20)
test_dataset = get_dataset(100)
n_inputs = len(dataset[0]) - 1
n_outputs = len(set([row[-1] for row in dataset]))
n_epochs = 200
l_rate = 0.5
network = build_network(n_inputs, 1, 3, n_outputs)
for epoch in range(n_epochs):
    sum_error = 0
    for row in dataset:
        outputs = forward_prop(network, row)
        expected = [0 for i in range(n_outputs)]
        expected[row[-1]] = 1
        for t in range(n_outputs):
            sum_error += (expected[t] - outputs[t])
        network = backprop(network, expected)
        network = update_weights(network, row, l_rate)
    if epoch == 0: print('Initial error = {}'.format(sum_error))
print('Final error = {}'.format(sum_error))
print()
print('Final network output:')
print(*network, sep='\n')
print()
c_counter = 0
for row in test_dataset:
    prediction, net_out = predict(network, row)
    print('Extected = {0}\tGot = {1}\tNet out = {2}'.format(row[-1], prediction, net_out))
    if prediction == row[-1]: c_counter += 1

# print(*network, sep='\n')
print()
print('Prediction accuracy for {0} testing cases: {1} %'.format(len(test_dataset), (c_counter / len(test_dataset)) * 100))
