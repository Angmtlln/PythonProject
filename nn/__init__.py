import numpy as np
from nn import activate_functions
from json import loads


class Net:
    """
    perceptron class
    creates a neural network, using weights, bias and activate function
    uses the error back propagation method for training
    """
    def __init__(self, *args, activate_function=activate_functions.Sigmoid, file=None):
        """
        creating a neural network or reading it from the file
        :param args: number of neurons on each layer
        :param activate_function: activate function for neurons
        :param file: if not None, then read weights and bias from file
        """
        self.function = activate_function
        if file:
            with open(file) as f:
                self.weights = [np.array(i) for i in loads(f.readline())]
                self.bias = [np.array(i) for i in loads(f.readline())]
        else:
            self.weights = [np.random.random((i, j)) - np.random.random((i, j)) for i, j in zip(args, args[1:])]
            self.bias = [np.random.random(i) - np.random.random(i) for i in args[1:]]

    def get(self, input):
        """
        gets the result of processing input by a neural network
        :param input: iterating class object input
        :return: the value on the last layer of the neural network
        """
        input = np.array(input)
        for weights, bias in zip(self.weights, self.bias):
            input = self.function.activate(input @ weights + bias)
        return input

    def train(self, input, output, k=1):
        """
        training of neural network on sample
        :param input: iterating class object input
        :param output: iterating class object output
        :param k: coefficient of training
        :return: None
        """
        input = np.array(input)
        z = []
        f = []
        for weights, bias in zip(self.weights, self.bias):
            f.append(input)
            input = input @ weights + bias
            z.append(input)
            input = self.function.activate(input)
        diff = []
        error = (input - np.array(output)).reshape(1, input.shape[0])
        for i, (Z, F) in enumerate(zip(z[::-1], f[::-1])):
            error *= self.function.derivative(Z)
            diff.append(k * F.reshape(F.shape[0], 1) @ error)
            self.bias[-i - 1] -= k * error[0]
            error = error @ self.weights[-i - 1].T
        for i, dif in enumerate(diff[::-1]):
            self.weights[i] -= dif

    def save(self, name):
        """
        save weights and bias in {name}.net file
        :param name: file name
        :return: None
        """
        with open(f'{name}.net', 'w') as f:
            f.write(str([[list(w) for w in weight] for weight in self.weights]))
            f.write('\n')
            f.write(str([list(i) for i in self.bias]))
