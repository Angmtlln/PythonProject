from math import cos, sin, radians
from random import random

import numpy as np
import pygame

from functions import array_to_angle
from neural_network import Net


def get_black_white(img: list[list[list[float]]]) -> pygame.Surface:
    """Get the image's black-white representation"""
    w, h = len(img), len(img[0])
    res = pygame.Surface((w, h))
    res.fill((200, 200, 200))
    im = pygame.Surface((w, h))
    for x in range(w):
        for y in range(h):
            im.set_at((x, y), [int(sum(img[x][y]) * 255 / 3)] * 3)
    im.set_alpha(50)
    res.blit(im, (0, 0))
    return res


def get_priority(img):
    df = 50
    w, h = len(img), len(img[0])
    priority = [[] for _ in range(766 - df)]
    for x in range(3, w - 3):
        for y in range(3, h - 3):
            dx = sum(abs(i - j) * 255 for i, j in zip(img[x][y], img[x + 1][y]))
            dy = sum(abs(i - j) * 255 for i, j in zip(img[x][y], img[x][y + 1]))
            d = min(766, int((dx ** 2 + dy ** 2) ** 0.5))
            d -= df
            if d <= 0: continue
            priority[-d].append((x, y))
    return priority


def convert():
    """Converts img.jpg to picture with strokes"""

    def fill(x, y, radius):
        """Fill the limit with circle starts from x,y with radius"""
        for i in range(max(0, x - radius), min(w, x + radius)):
            for j in range(max(0, y - radius), min(h, y + radius)):
                ln = ((x - i) ** 2 + (y - j) ** 2) ** 0.5
                if ln > radius: continue
                limit[i][j] = min(limit[i][j], ln)

    MX_DISTANCE = 10
    MX_LENGTH = 4
    img = pygame.image.load('img.jpg')
    w, h = img.get_size()
    img = [[[c / 255 for c in img.get_at((x, y))[:3]] for y in range(h)] for x in range(w)]
    img_np = np.array(img)
    res = get_black_white(img)
    limit = [[MX_DISTANCE + 1] * h for _ in range(w)]
    full = w - 6
    step = full // 10
    for p in get_priority(img):
        for x, y in p:
            k = sum(img[x][y]) / 3
            dist = MX_DISTANCE * k
            if limit[x][y] < dist: continue
            fill(x, y, int(dist))
            angle = list(net.get(np.reshape(img_np[x - 3:x + 4, y - 3:y + 4], (147,))))
            if round(angle.pop()):
                angle = random() * 180
            else:
                angle = array_to_angle(angle)
            angle = radians(angle)
            length = MX_LENGTH * (1 - k)
            i, j = cos(angle) * length, sin(angle) * length
            pygame.draw.aaline(res, [75] * 3, (x - i, y - j), (x + i, y + j))
    for x in range(3, w - 3):
        if (x - 3) % step == 0:
            yield 10 * (x - 3) // step
        for y in range(3, h - 3):
            k = sum(img[x][y]) / 3
            dist = MX_DISTANCE * k
            if limit[x][y] < dist: continue
            fill(x, y, int(dist))
            angle = list(net.get(np.reshape(img_np[x - 3:x + 4, y - 3:y + 4], (147,))))
            if round(angle.pop()):
                angle = random() * 180
            else:
                angle = array_to_angle(angle)
            angle = radians(angle)
            length = MX_LENGTH * (1 - k)
            i, j = cos(angle) * length, sin(angle) * length
            pygame.draw.aaline(res, [75] * 3, (x - i, y - j), (x + i, y + j))
    pygame.image.save(res, 'res.jpg')


net = Net(file='converter/art_weights.net')
