from math import radians, sin, cos
from nn import Net
from random import randint as rnd, random


def angle_to_array(angle):
    if 0 <= angle < 60:
        return (1 - angle / 60, angle / 60, 0)
    if 60 <= angle < 120:
        angle -= 60
        return (0, 1 - angle / 60, angle / 60)
    if 120 <= angle <= 180:
        angle -= 120
        return (angle / 60, 0, 1 - angle / 60)


def angle_to_line(angle):
    angle = radians(angle)
    x1, y1 = cos(angle), sin(angle)
    x2, y2 = -x1, -y1
    b = x2 - x1
    a = y1 - y2
    c = -(a * x1 + b * y1) + (random() - 0.5) * 6
    return a, b, c


net = Net(7 * 7 * 3, 50, 3)

q = 0
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
            test += [i / 255 for i in col]
    net.train(test, angle_to_array(angle), 0.5)
    q += 1
    if q % 5000 == 0:
        net.save(f'weights/art{q // 5000}')
        print(q)
