from math import radians, sin, cos
from random import randint as rnd, random


def angle_to_array(angle: float) -> list[float, float, float]:
    """
    Converts the angle into a set of 3 parameters, which is better suited for the perception of the neural network
    :param angle: angle value from 0 to 180 degrees
    :return: set of 3 parameters
    """
    if 0 <= angle < 60:
        return [1 - angle / 60, angle / 60, 0]
    if 60 <= angle < 120:
        angle -= 60
        return [0, 1 - angle / 60, angle / 60]
    if 120 <= angle <= 180:
        angle -= 120
        return [angle / 60, 0, 1 - angle / 60]


def array_to_angle(array: list[float, float, float]) -> float:
    """
    Deconverts the angle from a set of 3 parameters to default angle
    :param array: set of 3 parameters
    :return: angle value from 0 to 180 degrees
    """
    array[array.index(min(array))] = 0
    array = [i / sum(array) for i in array]
    if array[2] == 0:
        return array[1] * 60
    if array[0] == 0:
        return 60 + array[2] * 60
    if array[1] == 0:
        return 120 + array[0] * 60


def angle_to_line(angle: float) -> tuple[float, float, float]:
    """
    Get the line in ax + by + c = 0 representation from angle
    :param angle: float value from 0 to 180
    :return: parameters a,b and c in ax + by + c=0 representation
    """
    angle = radians(angle)
    x1, y1 = cos(angle), sin(angle)
    x2, y2 = -x1, -y1
    b = x2 - x1
    a = y1 - y2
    c = -(a * x1 + b * y1)
    return a, b, c


def get_color(*others: tuple[int, int, int]) -> tuple[int, int, int]:
    """
    Get new color, that not equals to other colors
    :param others: tuple of colors
    :return: new color
    """
    color = (rnd(0, 255), rnd(0, 255), rnd(0, 255))
    while any(sum(abs(i - j) for i, j in zip(color, other)) < 50 for other in others):
        color = (rnd(0, 255), rnd(0, 255), rnd(0, 255))
    return color


def noise(color: tuple[int, int, int]) -> tuple[int, int, int]:
    """
    Add the noise to color
    :param color: input color
    :return: input color with noise
    """
    return tuple(min(max(i + rnd(-20, 20), 0), 255) for i in color)


def probability(chance: float) -> bool:
    """
    Return True with {chance} probability
    :param chance: chance of True
    :return: True if chance worked else False
    """
    return random() < chance
