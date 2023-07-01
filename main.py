from nn import Net
from math import cos, sin, radians
from random import random
import pygame
from time import time


def array_to_angle(array):
    if array[2] == 0:
        return array[1] * 60
    if array[0] == 0:
        return 60 + array[2] * 60
    if array[1] == 0:
        return 120 + array[0] * 60


def get_bw(img) -> pygame.Surface:
    w, h = img.get_size()
    res = pygame.Surface((w, h))
    res.fill((200, 200, 200))
    im = pygame.Surface((w, h))
    for x in range(w):
        for y in range(h):
            im.set_at((x, y), [sum(img.get_at((x, y))[:3]) // 3] * 3)
    im.set_alpha(50)
    res.blit(im, (0, 0))
    return res


def convert(img: pygame.Surface) -> pygame.Surface:
    def check(x, y, d):
        for i in range(max(0, x - d), min(w, x + d)):
            for j in range(max(0, y - d), min(h, y + d)):
                if mas[i][j]: return True
        return False

    t = time()
    w, h = img.get_size()
    priority = tuple([] for _ in range(766))
    for x in range(3, w - 4):
        for y in range(3, h - 4):
            cur = img.get_at((x, y))
            rt = img.get_at((x + 1, y))
            dn = img.get_at((x, y + 1))
            dx = sum(abs(i - j) for i, j in zip(cur, rt))
            dy = sum(abs(i - j) for i, j in zip(cur, dn))
            g = int(min(755, (dx ** 2 + dy ** 2) ** 0.5))
            priority[755 - g].append((x, y))
        print(f'{x}/{w}')
    res = get_bw(img)
    mas = [[False] * h for _ in range(w)]
    for k in range(766):
        for x, y in priority[k]:
            input = []
            for i in range(x - 3, x + 4):
                for j in range(y - 3, y + 4):
                    input += [c / 255 for c in img.get_at((i, j))[:3]]
            K = sum(img.get_at((x, y))[:3]) / 765
            d = int((K * 10) * k / 765)
            if check(x, y, d): continue
            mas[x][y] = True
            angle = list(net.get(input))
            if round(angle.pop()):
                angle = random() * 180
            else:
                angle[angle.index(min(angle))] = 0
                angle = [i / sum(angle) for i in angle]
                angle = array_to_angle(angle)
            angle = radians(angle)
            d = 4 * (1 - K)
            i, j = cos(angle) * d, sin(angle) * d
            pygame.draw.aaline(res, [75] * 3, (x - i, y - j), (x + i, y + j))
        print(f'{k}/765')
    print(time() - t)
    return res


net = Net(file='weights/art80.net')
img = pygame.image.load('img.png')
img = convert(img)
pygame.image.save(img, 'ress.jpg')
