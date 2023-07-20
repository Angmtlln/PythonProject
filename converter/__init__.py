from math import cos, sin, radians
from random import random
from time import time

import numpy as np
import pygame

from functions import array_to_angle
from neural_network import Net


def get_black_white(img: list[list[list[float]]]) -> pygame.Surface:
    """Get the black white version with alpha argument 50 on canvas with color (200,200,200)"""
    w, h = len(img), len(img[0])
    res = pygame.Surface((w, h))
    res.fill((200, 200, 200))
    im = pygame.Surface((w, h))
    for x in range(w):
        for y in range(h):
            im.set_at((x, y), [min(255, int(sum(img[x][y]) * 255 / 3))] * 3)
    im.set_alpha(50)
    res.blit(im, (0, 0))
    return res


def convert():
    """Converts the img.jpg"""
    def fill(x, y, radius):
        for i in range(max(0, x - radius), min(w, x + radius)):
            for j in range(max(0, y - radius), min(h, y + radius)):
                ln = ((x - i) ** 2 + (y - j) ** 2) ** 0.5
                if ln > d: continue
                mas[i][j] = min(mas[i][j], ln)

    t = time()
    MX_LENGTH = 10
    img = pygame.image.load('img.jpg')
    w, h = img.get_size()
    img = [[[c / 255 for c in img.get_at((x, y))[:3]] for y in range(h)] for x in range(w)]
    img_np = np.array(img)
    res = get_black_white(img)
    mas = [[MX_LENGTH + 1] * h for _ in range(w)]
    full = w - 6
    step = full // 10
    for x in range(3, w - 3):
        if (x - 3) % step == 0:
            yield 10 * (x - 3) // step
        for y in range(3, h - 3):
            k = sum(img[x][y]) / 3
            d = MX_LENGTH * k
            if mas[x][y] < d: continue
            fill(x, y, int(d))
            angle = list(net.get(np.reshape(img_np[x - 3:x + 4, y - 3:y + 4], (147,))))
            if round(angle.pop()):
                angle = random() * 180
            else:
                angle = array_to_angle(angle)
            angle = radians(angle)
            d = 4 * (1 - k)
            i, j = cos(angle) * d, sin(angle) * d
            pygame.draw.aaline(res, [75] * 3, (x - i, y - j), (x + i, y + j))
    pygame.image.save(res, 'res.jpg')
    print(time() - t)


net = Net(file='converter/art_weights.net')
