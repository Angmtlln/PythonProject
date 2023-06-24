from nn import Net
import pygame
from math import sin, cos, radians


def array_to_angle(array):
    if array[2] == 0:
        return array[1] * 60
    if array[0] == 0:
        return 60 + array[2] * 60
    if array[1] == 0:
        return 120 + array[0] * 60


def convert(image: pygame.Surface) -> pygame.Surface:
    w = image.get_width()
    h = image.get_height()
    res = pygame.Surface((w, h))
    res.fill((200, 200, 200))
    mas = [[False] * h for _ in range(w)]
    k = 75
    for x in range(3, w - 4):
        for y in range(3, h - 4):
            check = True
            d = sum(image.get_at((x, y))[:3]) // k
            for i in range(max(0, x - d), min(x + d, w)):
                for j in range(max(0, y - d), min(y + d, h)):
                    if mas[i][j]:
                        check = False
            if check:
                mas[x][y] = True
                input = []
                K = 0
                for i in range(x - 3, x + 4):
                    for j in range(y - 3, y + 4):
                        color = [c / 255 for c in image.get_at((i, j))[:3]]
                        input += color
                        K += sum(color)
                K /= 147
                output = list(net.get(input))
                output[output.index(min(output))] = 0
                output = [i / sum(output) for i in output]
                angle = array_to_angle(output)
                K = 4 * (1 - K)
                dx = round(cos(radians(angle)) * K)
                dy = round(sin(radians(angle)) * K)
                pygame.draw.aaline(res, (50, 50, 50), (x - dx, y - dy), (x + dx, y + dy))
        print(x, '/', w)
    return res


net = Net(file='weights/art40.net')
img = pygame.image.load('img.png')
pygame.image.save(convert(img), 'res.jpg')
