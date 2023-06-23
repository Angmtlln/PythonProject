import numpy as np


class Function:
    """
    abstract class
    activate function for neurons
    """
    @staticmethod
    def activate(x):
        """
        static method
        :param x: input of neuron
        :return: output of neuron
        """
        pass

    @staticmethod
    def derivative(x):
        """
        static method
        :param x: input of neuron
        :return: derivative of the activate by unknown x
        """
        pass


class Sigmoid(Function):
    """
    limits the values of neurons between 0 and 1
    """
    @staticmethod
    def activate(x):
        return 1 / (1 + np.exp(-x))

    @staticmethod
    def derivative(x):
        f = Sigmoid.activate(x)
        return f * (1 - f)
