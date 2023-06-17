from math import e


class Function:
    """
    abstract class
    activate function for neurons
    """

    @staticmethod
    def activate(x: float) -> float:
        """
        static method
        :param x: input of neuron
        :return: output of neuron
        """
        pass

    @staticmethod
    def derivative(x: float) -> float:
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
    def activate(x: float) -> float:
        x = max(min(x, 700), -700)
        return 1 / (1 + e ** -x)

    @staticmethod
    def derivative(x: float) -> float:
        f = Sigmoid.activate(x)
        return f * (1 - f)
