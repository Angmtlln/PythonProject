from math import radians, sin, cos
from nn import Net
from random import randint as rnd, random
import pygame


def angle_to_array(angle):
    if 0 <= angle < 60:
        return (1 - angle / 60, angle / 60, 0)
    if 60 <= angle < 120:
        angle -= 60
        return (0, 1 - angle / 60, angle / 60)
    if 120 <= angle <= 180:
        angle -= 120
        return (angle / 60, 0, 1 - angle / 60)


def array_to_angle(array):
    if array[2] == 0:
        return array[1] * 60
    if array[0] == 0:
        return 60 + array[2] * 60
    if array[1] == 0:
        return 120 + array[0] * 60


def angle_to_line(angle):
    angle = radians(angle)
    x1, y1 = cos(angle), sin(angle)
    x2, y2 = -x1, -y1
    b = x2 - x1
    a = y1 - y2
    c = -(a * x1 + b * y1) + (random() - 0.5) * 6
    return a, b, c


net = Net(file='weights/art40.net')
dis = pygame.display.set_mode((350, 350))

while True:
    col1 = (rnd(0, 255), rnd(0, 255), rnd(0, 255))
    col2 = col1
    while sum(abs(i - j) for i, j in zip(col1, col2)) < 60:
        col2 = (rnd(0, 255), rnd(0, 255), rnd(0, 255))
    angle = random() * 180
    a, b, c = angle_to_line(angle)
    test = []
    for x in range(-3, 4):
        for y in range(-3, 4):
            col = [min(max(i + rnd(-20, 20), 0), 255) for i in (col1, col2)[a * x + b * y + c > 0]]
            pygame.draw.rect(dis, col, ((x + 3) * 50, (y + 3) * 50, 50, 50))
            test += [i / 255 for i in col]
    array = list(net.get(test))
    array[array.index(min(array))] = 0
    array = [i / sum(array) for i in array]
    angle = array_to_angle(array)
    x, y = cos(radians(angle)) * 250, sin(radians(angle)) * 250
    pygame.draw.line(dis, (0, 0, 0), (175 + x, 175 + y), (175 - x, 175 - y), 10)
    pressed = False
    while not pressed:
        for ev in pygame.event.get():
            if ev.type == pygame.MOUSEBUTTONDOWN:
                pressed = True
        pygame.display.update()
