from nn.activate_functions import Sigmoid, Function
from random import random as rnd
from copy import deepcopy
from json import loads


class Net:
    """
    perceptron class
    creates a neural network, using weights, bias and activate function
    uses the error back propagation method for training
    """

    def __init__(self, *args, activate_function: Function = Sigmoid, file=None):
        """
        creating a neural network or reading it from the file
        :param args: number of neurons on each layer
        :param activate_function: activate function for neurons
        :param file: if not None, then read weights and bias from file
        """
        if file:
            with open(file) as f:
                self.weights = loads(f.readline())
                self.bias = loads(f.readline())
        else:
            self.weights = [[[rnd() - 0.5 for __ in range(i)] for _ in range(j)] for i, j in zip(args, args[1:])]
            self.bias = [[rnd() - 0.5 for _ in range(i)] for i in args[1:]]
        self.function = activate_function

    def get(self, input):
        """
        gets the result of processing input by a neural network
        :param input: iterating class object input
        :return: the value on the last layer of the neural network
        """
        for layer, bias in zip(self.weights, self.bias):
            next = []
            for neuron, bias_neuron in zip(layer, bias):
                z = bias_neuron
                for weight, activator in zip(neuron, input):
                    z += weight * activator
                z = self.function.activate(z)
                next.append(z)
            input = next
        return input

    def train(self, input, output, k=1):
        """
        training of neural network on sample
        :param input: iterating class object input
        :param output: iterating class object output
        :param k: coefficient of training
        :return: None
        """
        all_layers = [list(input)]
        z_mas = []
        for layer, bias in zip(self.weights, self.bias):
            all_layers.append([])
            z_mas.append([])
            for neuron, bias_neuron in zip(layer, bias):
                z = bias_neuron
                for weight, activator in zip(neuron, all_layers[-2]):
                    z += weight * activator
                z_mas[-1].append(z)
                z = self.function.activate(z)
                all_layers[-1].append(z)
        err = [2 * (i - j) for i, j in zip(all_layers[-1], output)]
        new_w = deepcopy(self.weights)
        for j in range(len(z_mas) - 1, -1, -1):
            for i in range(len(err)):
                err[i] *= self.function.derivative(z_mas[j][i])
            for i in range(len(self.bias[j])):
                self.bias[j][i] -= err[i] * k
                for l in range(len(new_w[j][i])):
                    new_w[j][i][l] -= err[i] * all_layers[j][l] * k
            prev_err = [0] * len(all_layers[j])
            for i in range(len(err)):
                for l in range(len(self.weights[j][i])):
                    prev_err[l] += err[i] * self.weights[j][i][l]
            err = prev_err
        self.weights = new_w

    def save(self, name):
        """
        save weights and bias in {name}.net file
        :param name: file name
        :return: None
        """
        with open(f'{name}.net', 'w') as f:
            f.write(f'{self.weights}\n{self.bias}')
