// A C implementation of an artificial neural network. 
// !! Work in progress: network can learn with sufficient accuracy. Prediction needs to be worked on.

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>
#include <stdbool.h>

int n_hidden_layers = 3;
int n_layers_inc_out = 4;   // first dimension of network_weights | first dim of network_neuron_activations
int n_input_features = 9;   // third dimension of network_weights
int n_outputs = 2;
int n_neurons = 3;          // second dimension of network_weights | second dim of network_neuron_activations
int n_training_samples = 20;
int n_testing_samples = 100;
float ***network_weights;
float **network_neuron_activations;
float **network_neuron_deltas;  // network_neuron_deltas shares same dimensions of network_neuron_activations

void initialize_network_parameters(int n_inputs, int n__outputs, int n_layers, int n_nodes, int n_train_set, int n_test_set){
    n_hidden_layers = n_layers;
    n_layers_inc_out = n_hidden_layers + 1;
    n_outputs = n__outputs;
    n_input_features = n_inputs;
    n_neurons = n_nodes;
    n_training_samples = n_train_set;
    n_testing_samples = n_test_set;
}

float randrange(float min, float max) {
    float my_rand = rand()/(double)RAND_MAX;
    return (max - min) * my_rand + min;
}

double activation_function(double x) {return (1 / (1 + exp(-x))); }
double activation_function_derivative(float x) {return (1.0 * (1.0 - x)); }

float loss_function(float *actual, int *predicted, _Bool mse, _Bool cross_entropy){
    float loss;
    if (mse == true){
        float sum_square_error = 0;
        for (int i = 0; i < n_outputs; i++) sum_square_error += pow((actual[i] - predicted[i]), 2);
        loss = 1.0 / n_outputs * sum_square_error;
    }
    if (cross_entropy == true){
        float sum_score = 0.0;
        for (int i = 0; i < n_outputs; i++) sum_score += actual[i] * log((exp(-15) + predicted[i]));
        loss = -(1.0 / n_outputs * sum_score);
    }
    return loss;
}

void build_network(){
    network_weights = (float ***)malloc(n_layers_inc_out * sizeof(float **));
    for (int i = 0; i < n_layers_inc_out; i++){
        network_weights[i] = (float **)malloc(n_neurons * sizeof(float *));
        for (int j = 0; j < n_neurons; j++){
            network_weights[i][j] = (float *)malloc((n_input_features + 1) * sizeof(float));
            for (int k = 0; k < (n_input_features + 1); k++){
                if(i == 0) network_weights[i][j][k] = randrange(0, 1);
                else if (i == (n_layers_inc_out - 1)){
                    if (j >= n_outputs) network_weights[i][j][k] = 0;
                    else{
//                        if (k >= n_outputs + 1) network_weights[i][j][k] = 0;
//                        else network_weights[i][j][k] = randrange(0, 1);
                        if (k >= n_neurons + 1) network_weights[i][j][k] = 0;
                        else network_weights[i][j][k] = randrange(0, 1);
                    }
                }
                else{
                    if (k >= n_neurons + 1) network_weights[i][j][k] = 0;
                    else network_weights[i][j][k] = randrange(0, 1);
                }
            }
        }
    }
}

void neuron_init(){
    network_neuron_activations = (float **)malloc(n_layers_inc_out * sizeof(float *));
    network_neuron_deltas = (float **)malloc(n_layers_inc_out * sizeof(float *));
    for (int i = 0; i < n_layers_inc_out; i++){
        network_neuron_activations[i] = (float *)malloc(n_neurons * sizeof(float));
        network_neuron_deltas[i] = (float *)malloc(n_neurons * sizeof(float));
        for (int j = 0; j < n_neurons; j++){
            network_neuron_activations[i][j] = 0;
            network_neuron_deltas[i][j] = 0;
        }
    }
}

float* forward_propogate(const float *input_row){
    float *inputs = (float *)malloc(n_input_features * sizeof(float));
    for (int t = 0; t < n_input_features; t++) inputs[t] = input_row[t];
    int input_length = n_input_features;
    for (int i = 0; i < n_layers_inc_out; i++){
        for (int j = 0; j < n_neurons; j++){
            if (i == (n_layers_inc_out - 1) && j > (n_outputs - 1)) break;
            network_neuron_activations[i][j] = network_weights[i][j][0];
            for (int k = 0; k < input_length; k++){
                if (network_weights[i][j][k + 1] == 0 || network_neuron_activations[i][j] == 0) break;
                network_neuron_activations[i][j] += network_weights[i][j][k + 1] * inputs[k];
            }
            network_neuron_activations[i][j] = (float)activation_function(network_neuron_activations[i][j]);
        }
//        free(inputs);
        if (i == 0) {
            inputs = realloc(inputs, n_neurons * sizeof(float));
            input_length = n_neurons;
        }
        for (int t = 0; t < n_neurons; t++) inputs[t] = network_neuron_activations[i][t];
//        inputs = network_neuron_activations[i];
//        printf("\nInputs in forward prop at at layer %d = ", i + 1);
//        for (int t = 0; t < input_length; t++) printf("%f ", inputs[t]);
    }
    return inputs;
}

void backpropogate(const int *expected){
    float *errors = (float *)malloc(n_neurons * sizeof(float));
    for (int i = (n_layers_inc_out - 1); i >= 0; i--){
        for (int t = 0; t < n_neurons; t++) errors[t] = 0;
        if (i != (n_layers_inc_out - 1)){
            for (int j = 0; j < n_neurons; j++){
                float error = 0;
                for (int k = 0; k < n_neurons; k++){
                    if (i + 1 == (n_layers_inc_out - 1) && k == n_outputs) break;
                    error += network_weights[i + 1][k][k + 1] * network_neuron_deltas[i + 1][k];
                }
                errors[j] = error;
            }
        }
        else for (int j = 0; j < n_outputs; j++) errors[j] = (float)(expected[j] - network_neuron_activations[i][j]);
        for (int j = 0; j < n_neurons; j++){
            if (i == (n_layers_inc_out - 1) && j == n_outputs) break;
            network_neuron_deltas[i][j] = errors[j] * activation_function_derivative(network_neuron_activations[i][j]);
        }
    }
    free(errors);
}

void update_weights(float *feature_set, int n_inputs, float alpha){
    float *inputs = feature_set;
    int input_length = n_inputs;
    for (int i = 0; i < n_layers_inc_out; i++){
        if (i != 0){
            input_length = 0;
            for (int j = 0; j < n_neurons; j++){
                if (i == (n_layers_inc_out - 1) && j == n_outputs) break;
                inputs[j] = network_neuron_activations[i - 1][j];
                input_length++;
            }
        }
        for (int j = 0; j < n_neurons; j++){
            for (int k = 0; k < input_length; k++){
                network_weights[i][j][k + 1] += alpha * network_neuron_deltas[i][j] * inputs[j];
            }
            network_weights[i][j][0] += alpha * network_neuron_deltas[i][j];
        }
    }
}

float* predict(float *test_data){
    float *outputs = forward_propogate(test_data);
    float m = outputs[0];
    int index = 0;
//    for (int i = 0; i < n_outputs; i++){
//        if (outputs[i] > m){
//            m = outputs[i];
//            index = i;
//        }
//    }
//    return index;
    return outputs;
}

float** get_dataset(int n_samples){
    float **X = (float **)malloc(n_samples * sizeof(float *));
    for(int row = 0; row < n_samples; row++) {
        float PB[] = {randrange(-0.2, -0.1), randrange(0.1, 0.2), randrange(-0.2, -0.1),
                      randrange(0.3, 0.5), randrange(-0.5, -0.3), randrange(1.5, 2.5),
                      randrange(0.5, 1.5), randrange(0.5, 1.5), randrange(0.8, 1.0), 1};
        float UP[] = {randrange(-0.15, -0.05), randrange(0.05, 0.15), randrange(-0.15, -0.05),
                      randrange(0.3, 0.5), randrange(-0.5, -0.3), randrange(1, 2),
                      randrange(0.1, 1), randrange(0.1, 1), randrange(0.5, 0.8), 0};
        X[row] = (float *) malloc((n_input_features + 1) * sizeof(float));
        for(int col = 0; col < (n_input_features + 1); col++){
            if (row < (int)(n_samples / 2)) X[row][col] = PB[col];
            else X[row][col] = UP[col];

        }
    }
    return (X);
}

int main() {
    srand((long)time(0));
    float l_rate = 0.5;
    int n_epochs = 20;
    float sum_error = 0;
    initialize_network_parameters(9, 2, 3, 3, 20, 100);
    int expected[n_outputs];
    build_network();
    neuron_init();
    float **train_set = get_dataset(n_training_samples);
    float **test_data = get_dataset(n_testing_samples);
    for (int i = 0; i < n_epochs; i++){
        sum_error = 0;
        for (int j = 0; j < n_training_samples; j++){
            float *net_out = forward_propogate(train_set[j]);
            for (int t = 0; t < n_outputs; t++) expected[t] = 0;
            expected[(int)train_set[j][n_input_features]] = 1;
            for (int t = 0; t < n_outputs; t++) sum_error += (expected[t] - net_out[t]);
//            printf("\nExpected values:\t");
//            for (int t = 0; t < n_outputs; t++)printf("%d : %f\t", expected[t], net_out[t]);
            backpropogate(expected);
            update_weights(train_set[j], n_input_features, l_rate);
        }
        if (i == 0) printf("Initial error  = %f\n", sum_error);
    }
    printf("Final error = %f\n", sum_error);
//    printf("Training data:\n");
//    for (int i = 0; i < n_training_samples; i++){
//        for (int j = 0; j < (n_input_features + 1); j++){
//            printf("%f ", train_set[i][j]);
//        }
//        printf("\n");
//    }
    printf("\n");
    printf("Network weights:\n");
    for (int i = 0; i < n_layers_inc_out; i++){
        printf("Layer #%d:\n", i + 1);
        for (int j = 0; j < n_neurons; j++){
            printf("Neuron #%d:\t", j + 1);
            for (int k = 0; k < (n_input_features + 1); k++){
                printf("%f ", network_weights[i][j][k]);
            }
            printf("\n");
        }
        printf("\n");
    }
    printf("\n");
    printf("Network neuron outputs:\n");
    for (int i = 0; i < n_layers_inc_out; i++){
        printf("Layer #%d:\t", i + 1);
        for (int j = 0; j < n_neurons; j++){
            printf("%f ", network_neuron_activations[i][j]);
        }
        printf("\n");
    }
    printf("\n");
    printf("Network delta values:\n");
    for (int i = 0; i < n_layers_inc_out; i++){
        printf("Layer #%d:\t", i + 1);
        for (int j = 0; j < n_neurons; j++){
            printf("%f ", network_neuron_deltas[i][j]);
        }
        printf("\n");
    }
//    printf("Testing data:\n");
//    for (int i = 0; i < n_training_samples; i++){
//        for (int j = 0; j < (n_input_features + 1); j++){
//            printf("%f ", test_data[i][j]);
//        }
//        printf("\n");
//    }
    printf("\n");
    for (int i = 0; i < n_training_samples; i++){
        float *prediction = predict(train_set[i]);
//        printf("Expected = %d\tGot = %d\n", (int)test_data[i][n_input_features], prediction);
        for (int j = 0; j < n_outputs; j++) printf("%f\t", prediction[j]);
        printf("\n");
    }
    return 0;
}
