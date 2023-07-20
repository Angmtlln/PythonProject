import numpy as np
from neural_network import activate_functions
from json import loads


class Net:
    """Perceptron class"""

    def __init__(self, *args, activate_function: activate_functions.Function = activate_functions.Sigmoid,
                 file: str = None):
        """
        Initialization of perceptron class
        :param args: the number of neurons on the layers
        :param activate_function: activation function for a neuron(Sigmoid by default)
        :param file: filename with weights
        """
        self.function = activate_function
        if file:
            with open(file) as f:
                self.weights = [np.array(i) for i in loads(f.readline())]
                self.bias = [np.array(i) for i in loads(f.readline())]
        else:
            self.weights = [np.random.random((i, j)) - np.random.random((i, j)) for i, j in zip(args, args[1:])]
            self.bias = [np.random.random(i) - np.random.random(i) for i in args[1:]]

    def get(self, input: np.ndarray) -> np.ndarray:
        """
        Get the neural network result for input
        :param input: input of net
        :return: result of net
        """
        for weights, bias in zip(self.weights, self.bias):
            input = self.function.activate(input @ weights + bias)
        return input

    def train(self, input: np.ndarray, output: np.ndarray, k: float = 1.0):
        """
        Error back propagation method
        :param input: input of net
        :param output: correct result for input
        :param k: coefficient of training
        :return: None
        """
        z = []
        f = []
        for weights, bias in zip(self.weights, self.bias):
            f.append(input)
            input = input @ weights + bias
            z.append(input)
            input = self.function.activate(input)
        diff = []
        error = (input - output).reshape(1, input.shape[0])
        for i, (Z, F) in enumerate(zip(z[::-1], f[::-1])):
            error *= self.function.derivative(Z)
            diff.append(k * F.reshape(F.shape[0], 1) @ error)
            self.bias[-i - 1] -= k * error[0]
            error = error @ self.weights[-i - 1].T
        for i, dif in enumerate(diff[::-1]):
            self.weights[i] -= dif

    def save(self, name):
        """
        Save weights to file {name}.net
        :param name: filename
        :return: None
        """
        with open(f'{name}.net', 'w') as f:
            f.write(str([[list(w) for w in weight] for weight in self.weights]))
            f.write('\n')
            f.write(str([list(i) for i in self.bias]))
