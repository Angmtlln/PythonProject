from nn import Net
from random import randint as rnd
import pygame
from math import sin, cos, radians


# A display window is created with dimensions 350x350 pixels. The neural network object is created using weights loaded from a file. A surface object is created with a size of 7x7 pixels. This surface will be used to draw polygons.
dis = pygame.display.set_mode((350, 350))
net = Net(file='weights/arts20.net')
sample = pygame.Surface((7, 7))
# An infinite loop is initiated to continuously update the graphics.
while True:
    # Random background color and polygon color are generated within a certain range of values. An angle is also randomly chosen, and the output value for the neural network is set based on the normalized angle.
    bg = rnd(1, 254)
    sample.fill((bg, bg, bg))
    color = bg
    while abs(color - bg) < 10:
        color = rnd(1, 254)
    angle = rnd(0, 180)
    output = [angle / 180]
    # The x and y components are calculated based on the angle using trigonometric functions.
    x = int(cos(radians(angle)) * 10)
    y = int(sin(radians(angle)) * 10)
    # Depending on the relative positions of x and y, a polygon is drawn on the sample surface using the calculated values.
    if y > abs(x):
        pygame.draw.polygon(sample, [color] * 3, ((3 + x, 3 + y), (7, 7), (7, 0), (3 - x, 3 - y)))
    elif x > 0:
        pygame.draw.polygon(sample, [color] * 3, ((3 + x, 3 + y), (7, 7), (0, 7), (3 - x, 3 - y)))
    else:
        pygame.draw.polygon(sample, [color] * 3, ((3 + x, 3 + y), (0, 7), (7, 7), (3 - x, 3 - y)))
    # The color information of each pixel in the sample surface is retrieved and normalized. The normalized color values are then added to the input list.
    input = []
    for x in range(7):
        for y in range(7):
            input.append((sum(sample.get_at((x, y))[:3])) / 765)
    angle = radians(net.get(input)[0] * 180)
    dis.blit(pygame.transform.scale(sample, (350, 350)), (0, 0))
    dx, dy = cos(angle) * 300, sin(angle) * 300
    pygame.draw.line(dis, (255, 0, 0), (175 - dx, 175 - dy), (175 + dx, 175 + dy), 10)
    # The neural network is used to predict the angle based on the input data. The sample surface is scaled up to the size of the display window and blitted onto it. A line is drawn on the display window indicating the predicted angle.
    pressed = False
    while not pressed:
        for ev in pygame.event.get():
            if ev.type == pygame.KEYDOWN:
                pressed = True
        pygame.display.update()