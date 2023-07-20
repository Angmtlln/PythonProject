from neural_network import Net
from functions import *
from random import random
import numpy as np

net = Net(7 * 7 * 3, 50, 4)
train_count = 0

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
        input = np.array(input)
        output = np.array(angle_to_array(angle) + [0])
        net.train(input, output, 0.4)
    else:
        for x in range(-3, 4):
            for y in range(-3, 4):
                input += [i / 255 for i in noise(col1)]
        input = np.array(input)
        output = list(net.get(input))
        output[-1] = 1
        output = np.array(output)
        net.train(input, output, 0.4)
    train_count += 1
    if train_count % 10000 == 0:
        net.save(f'weights/art{train_count // 10000}')
        print(train_count)
