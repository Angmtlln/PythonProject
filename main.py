#The code imports necessary modules: Net from nn, randint from random, pygame, and sin, cos, radians from math.
from nn import Net
from random import randint as rnd
import pygame
from math import sin, cos, radians


# An instance of the Net class is created with 49 input nodes, 30 hidden nodes, and 1 output node.
net = Net(49, 30, 1)

# A Pygame surface object is created with dimensions 7x7, which will be used to draw shapes.
sample = pygame.Surface((7, 7))


cnt = 0
while True:
    # The main loop of the program starts, which will continue indefinitely until interrupted.
    bg = rnd(1, 254)
    sample.fill((bg, bg, bg))
    # A random value between 1 and 254 is generated and used as the background color for the sample surface. It is filled with the chosen background color.
    color = bg
    while abs(color - bg) < 10:
        color = rnd(1, 254)
    # A random color is generated and assigned to color, ensuring that it is different enough from the background color by checking the absolute difference.
    angle = rnd(0, 180)
    output = [angle / 180]
    #A random angle between 0 and 180 is generated. This angle is then normalized to a value between 0 and 1 and assigned to output.
    x = int(cos(radians(angle)) * 10)
    y = int(sin(radians(angle)) * 10)
    # The generated angle is converted to radians and used to calculate the x and y coordinates of a point on a unit circle, which are then scaled by 10.
    if y > abs(x):
        pygame.draw.polygon(sample, [color] * 3, ((3 + x, 3 + y), (7, 7), (7, 0), (3 - x, 3 - y)))
    elif x > 0:
        pygame.draw.polygon(sample, [color] * 3, ((3 + x, 3 + y), (7, 7), (0, 7), (3 - x, 3 - y)))
    else:
        pygame.draw.polygon(sample, [color] * 3, ((3 + x, 3 + y), (0, 7), (7, 7), (3 - x, 3 - y)))
    # Depending on the values of x and y, a polygon is drawn on the sample surface using the chosen color. The shape of the polygon varies based on the relationship between x and y.
    input = []
    for x in range(7):
        for y in range(7):
            input.append((sum(sample.get_at((x, y))[:3])) / 765)
    # An empty list input is created. Then, for each pixel in the sample surface, the RGB values are summed and divided by 765 (255 * 3) to normalize the color values between 0 and 1. The resulting normalized color values are added to the input list.
    net.train(input, output)
    cnt += 1
    if cnt % 5000 == 0:
        net.save(f'weights/arts{cnt // 5000}')
        print(cnt)