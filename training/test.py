import numpy as np
from functions import *
from neural_network import Net
from random import random
import pygame

net = Net(file='weights/art30.net')
dis = pygame.display.set_mode((350, 350))

q = 0
while True:
    col1 = get_color()
    input = []
    if probability(4 / 5):
        col2 = get_color(col1)
        angle = random() * 180
        a, b, c = angle_to_line(angle)
        if probability(2 / 3):
            c += (random() - 0.5) * 6
            for x in range(-3, 4):
                for y in range(-3, 4):
                    col = noise((col1, col2)[a * x + b * y + c > 0])
                    input += [i / 255 for i in col]
                    pygame.draw.rect(dis, col, ((x + 3) * 50, (y + 3) * 50, 50, 50))
        else:
            c += (random() - 0.5) * 3
            C = c
            c += 0.5 + random() * 2
            C -= 0.5 + random() * 2
            col3 = col1
            if probability(1 / 3):
                col3 = get_color(col1, col2)
            for x in range(-3, 4):
                for y in range(-3, 4):
                    col = col2
                    axby = a * x + b * y
                    if axby + c < 0 and axby + C < 0: col = col1
                    if axby + c > 0 and axby + C > 0: col = col3
                    col = noise(col)
                    input += [i / 255 for i in col]
                    pygame.draw.rect(dis, col, ((x + 3) * 50, (y + 3) * 50, 50, 50))
    else:
        for x in range(-3, 4):
            for y in range(-3, 4):
                col = noise(col1)
                input += [i / 255 for i in col]
                pygame.draw.rect(dis, col, ((x + 3) * 50, (y + 3) * 50, 50, 50))
    array = list(net.get(np.array(input)))
    if not round(array.pop()):
        angle = radians(array_to_angle(array))
        x, y = cos(angle) * 250, sin(angle) * 250
        pygame.draw.line(dis, (0, 0, 0), (175 + x, 175 + y), (175 - x, 175 - y), 10)
    pressed = False
    while not pressed:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                pressed = True
        pygame.display.update()
