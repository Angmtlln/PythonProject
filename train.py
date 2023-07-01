# Import necessary libraries
from math import radians, sin, cos
from nn import Net
from random import randint as rnd, random

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

# Function to convert angle to line representation
def angle_to_line(angle):
    angle = radians(angle)
    x1, y1 = cos(angle), sin(angle)
    x2, y2 = -x1, -y1
    b = x2 - x1
    a = y1 - y2
    c = -(a * x1 + b * y1)
    return a, b, c

# Create an instance of the neural network class with the specified dimensions
net = Net(7 * 7 * 3, 50, 4)

q = 0
while True:
    col1 = (rnd(0, 255), rnd(0, 255), rnd(0, 255))
    test = []
    
    # Generate test input and target output for training
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
                    test += [i / 255 for i in col]
                    
        # Train the neural network
        net.train(test, angle_to_array(angle) + (0,), 0.5)
    else:
        for x in range(-3, 4):
            for y in range(-3, 4):
                col = [min(max(i + rnd(-30, 30), 0), 255) for i in col1]
                test += [i / 255 for i in col]
        angle = list(net.get(test))
        angle[-1] = 1
        net.train(test, angle, 0.5)
    
    q += 1
    
    # Save weights every 5000 iterations
    if q % 5000 == 0:
        net.save(f'weights/art{q // 5000}')
        print(q)
