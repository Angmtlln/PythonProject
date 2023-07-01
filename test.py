# Import necessary libraries
from math import radians, sin, cos
from nn import Net
from random import randint as rnd, random
import pygame

# Function to convert angle to array representation
def angle_to_array(angle):
    if 0 <= angle < 60:
        return (1 - angle / 60, angle / 60, 0)
    if 60 <= angle < 120:
        angle -= 60
        return (0, 1 - angle / 60, angle / 60)
    if 120 <= angle <= 180:
        angle -= 120
        return (angle / 60, 0, 1 - angle / 60)

# Function to convert array representation to angle
def array_to_angle(array):
    if array[2] == 0:
        return array[1] * 60
    if array[0] == 0:
        return 60 + array[2] * 60
    if array[1] == 0:
        return 120 + array[0] * 60

# Function to convert angle to line representation
def angle_to_line(angle):
    angle = radians(angle)
    x1, y1 = cos(angle), sin(angle)
    x2, y2 = -x1, -y1
    b = x2 - x1
    a = y1 - y2
    c = -(a * x1 + b * y1)
    return a, b, c

# Load pre-trained model
net = Net(file='weights/art80.net')

# Initialize window
dis = pygame.display.set_mode((350, 350))

q = 0
while True:
    # Generate random color
    col1 = (rnd(0, 255), rnd(0, 255), rnd(0, 255))
    test = []
    
    # Generate test input and draw rectangles on the game window
    if rnd(0, 6):
        col2 = col1
        while sum(abs(i - j) for i, j in zip(col1, col2)) < 50:
            col2 = (rnd(0, 255), rnd(0, 255), rnd(0, 255))
        angle = random() * 180
        a, b, c = angle_to_line(angle)
        
        # Randomly adjust line position
        if rnd(0, 2):
            c += (random() - 0.5) * 6
            for x in range(-3, 4):
                for y in range(-3, 4):
                    col = [min(max(i + rnd(-20, 20), 0), 255) for i in (col1, col2)[a * x + b * y + c > 0]]
                    pygame.draw.rect(dis, col, ((x + 3) * 50, (y + 3) * 50, 50, 50))
                    test += [i / 255 for i in col]
        else:
            c += (random() - 0.5) * 3
            C = c
            c += 0.5 + random() * 2
            C -= 0.5 + random() * 2
            col3 = col1
            
            # Generate a third color if needed
            if not rnd(0, 3):
                while any(sum(abs(i - j) for i, j in zip(col3, cl)) < 50 for cl in (col1, col2)):
                    col3 = (rnd(0, 255), rnd(0, 255), rnd(0, 255))
                    
            for x in range(-3, 4):
                for y in range(-3, 4):
                    col = col2
                    axby = a * x + b * y
                    
                    # Assign color based on line position
                    if axby + c < 0 and axby + C < 0: 
                        col = col1
                    if axby + c > 0 and axby + C > 0: 
                        col = col3
                    col = [min(max(i + rnd(-20, 20), 0), 255) for i in col]
                    pygame.draw.rect(dis, col, ((x + 3) * 50, (y + 3) * 50, 50, 50))
                    test += [i / 255 for i in col]
    else:
        for x in range(-3, 4):
            for y in range(-3, 4):
                col = [min(max(i + rnd(-30, 30), 0), 255) for i in col1]
                pygame.draw.rect(dis, col, ((x + 3) * 50, (y + 3) * 50, 50, 50))
                test += [i / 255 for i in col]
        
        # Use neural network to get predicted angle
        angle = list(net.get(test))
        angle[-1] = 1
        
    array = list(net.get(test))
    if not round(array.pop()):
        array[array.index(min(array))] = 0
        array = [i / sum(array) for i in array]
        angle = array_to_angle(array)
        x, y = cos(radians(angle)) * 250, sin(radians(angle)) * 250
        pygame.draw.line(dis, (0, 0, 0), (175 + x, 175 + y), (175 - x, 175 - y), 10)
    
    # Wait for mouse click to continue
    pressed = False
    while not pressed:
        for ev in pygame.event.get():
            if ev.type == pygame.MOUSEBUTTONDOWN:
                pressed = True
        pygame.display.update()
