import math as mt
from matplotlib import patches
from celluloid import Camera
from matplotlib import pyplot
import numpy as np

def F(n, X, Ay):
    f = np.zeros(n)
    f[0] = (X[0] + X[2] * mt.cos(3 * mt.pi / 2 - X[3]) + 0.353)
    f[1] = (X[1] + X[2] * mt.cos(3 * mt.pi / 2 + X[4]) - 0.353)
    f[2] = (X[2] + X[2] * mt.sin(3 * mt.pi / 2 - X[3]) - Ay)
    f[3] = ((X[3] + X[4]) * X[2] + (X[1] - X[0]) - (3 * mt.pi / 8))
    f[4] = (X[2] + X[2] * mt.sin(3 * mt.pi / 2 + X[4]) - Ay)    
    return f

def Condition(n, X, Ay):
    f = F(n, X, Ay)
    for i in range(n):
        if (abs(f[i]) > eps):
            return 0
    return 1

def Calculation(n, Ay):
    X = np.zeros(n)
    while (Condition(n, X, Ay) == False):
        for i in range(n):
            X[i] = X[i] - F(n, X, Ay)[i] * tau
    return X

Ay, Uy = 0.3, 0.0     

n = 5
eps, tau = 1e-3, 5e-3
dT, M, p, g = 1e-2, 100, 2000, 9.8066

fig = pyplot.figure()
ax = pyplot.axes(xlim = (-0.7, 0.7), ylim = (0, 0.4))
camera = Camera(fig)

for i in range(n ** 3):
    X = Calculation(n, Ay)
    x1, x2 = X[0], X[1]
    l = x2 - x1
    y, ph1, ph2 = X[2], X[3], X[4]
    if (i <= ((n ** 3) / 2)):
        Ay += Uy * dT
        Uy += (1 / M) * (p * l - M * g) * dT
    else:
        Ay -= Uy * dT
        Uy -= (1 / M) * (p * l - M * g) * dT
    f1 = patches.Arc((x1, y), 2 * y, 2 * y, angle = 0.0, theta1 = (3 * mt.pi / 2 - ph1) * (180 / mt.pi), theta2 = 3 * 180 / 2, 
                     linewidth = 1)
    f2 = patches.Arc((x2, y), 2 * y, 2 * y, angle = 0.0, theta1 = 3 * 180 / 2, theta2 = (3 * mt.pi / 2 + ph2), 
                     linewidth = 1)
    ax.add_patch(f1)
    ax.add_patch(f2)
    camera.snap()
    print(i + 1, X, Ay)

animation = camera.animate()
pyplot.show()
# animation.save('cylinders.gif', writer = 'imagemagick')
