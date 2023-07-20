import numpy as np


class Function:
    """Activate f/ unction(abstract class)"""

    @staticmethod
    def activate(x: np.ndarray) -> np.ndarray:
        """
        Activate of function
        :param x: input
        :return: activation for argument x
        """
        pass

    @staticmethod
    def derivative(x: np.ndarray) -> np.ndarray:
        """
        Derivative of function
        :param x: input
        :return: derivative for argument x
        """
        pass


class Sigmoid(Function):
    """Sigmoid activate function"""

    @staticmethod
    def activate(x: np.ndarray) -> np.ndarray:
        return 1 / (1 + np.exp(-x))

    @staticmethod
    def derivative(x: np.ndarray) -> np.ndarray:
        f = Sigmoid.activate(x)
        return f * (1 - f)
