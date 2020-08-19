import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
plt.style.use('seaborn-white')
import random as rn


dt = 0.001

def ddx(function, x, y, t, h):
    return  (function(x + h, y, t) - function(x, y, t))/h

def ddy(function, x, y, t, h):
    return  (function(x, y + h, t) - function(x, y, t))/h

def fieldStrength(positionx, positiony, time):
    #return 10*np.sin(positionx*10 - 10*time*dt) + 10*positionx*np.cos(positiony*10 + 10*time*dt)
    return (positionx) ** 4 + (positiony) ** 4 - (positionx) ** 2 - (positiony) ** 2


def interactx(part1,part2):
    if (((part1.x-part2.x)**2 + (part1.y - part2.y)**2) > 0.01):
        return (part1.x - part2.x)*(part1.charge)*(part2.charge)*(100)/((part1.x-part2.x)**2 + (part1.y - part2.y)**2)
    else:
        return (part1.x - part2.x)*(part1.charge)*(part2.charge)*(100)/(0.01)

def interacty(part1, part2):
    if (((part1.x-part2.x)**2 + (part1.y - part2.y)**2) > 0.01):
        return (part1.y - part2.y)*(part1.charge)*(part2.charge)*(100)/((part1.x-part2.x)**2 + (part1.y - part2.y)**2)
    else:
        return (part1.y - part2.y)*(part1.charge)*(part2.charge)*(100)/(0.01)




class particle:
    def __init__(self, x, y, xvelocity, yvelocity, charge, mass, accelerationx, accelerationy):
        self.x = x
        self.y = y
        self.xvelocity = xvelocity
        self.yvelocity = yvelocity
        self.charge = charge
        self.mass = mass
        self.accelerationx = 0
        self.accelerationy = 0
        self.time = 0

    def field(self):
        accelerationx = (self.charge)*(-ddx(fieldStrength, self.x, self.y, self.time, 0.001))/(self.mass)
        self.accelerationx = accelerationx
        accelerationy = (self.charge)*(-ddy(fieldStrength, self.x, self.y, self.time, 0.001))/(self.mass)
        self.accelerationy = accelerationy
        
    def motion(self):
        xvelocity = self.xvelocity
        x = self.x
        yvelocity = self.yvelocity
        y = self.y
        accelerationx = self.accelerationx
        accelerationy = self.accelerationy

        xvelocity = xvelocity + accelerationx*dt
        x = x + xvelocity*dt

        yvelocity = yvelocity + accelerationy*dt
        y = y + yvelocity*dt

        self.xvelocity = xvelocity
        self.x = x
        self.yvelocity = yvelocity
        self.y = y





p1 = particle(0, 0, rn.uniform(-0.2,0.2), rn.uniform(-0.2,0.2), 1, 10, 0, 0)
p2 = particle(rn.uniform(-0.5,0.5), rn.uniform(-0.5,0.5), rn.uniform(-0.1,0.1), rn.uniform(-0.1,0.1), 1, rn.uniform(1,100), 0, 0)
p3 = particle(rn.uniform(-0.5,0.5), rn.uniform(-0.5,0.5), rn.uniform(-0.1,0.1), rn.uniform(-0.1,0.1), -1, rn.uniform(1,100), 0, 0)

x1 = np.zeros(10000)
y1 = np.zeros(10000)

x2 = np.zeros(10000)
y2 = np.zeros(10000)

x3 = np.zeros(10000)
y3 = np.zeros(10000)

t = np.zeros(10000)

for i in range(0,10000):
    p1.time = i
    p1.field()
    p1.accelerationx += interactx(p1, p2)/(p1.mass) + interactx(p1, p3)/(p1.mass)
    p1.accelerationy += interacty(p1, p2)/(p1.mass) + interacty(p1, p3)/(p1.mass)
    p1.motion()

    x1[i] = p1.x
    y1[i] = p1.y

    p2.time = i
    p2.field()
    p2.accelerationx += interactx(p2, p1)/(p2.mass) + interactx(p2, p3)/(p2.mass)
    p2.accelerationy += interacty(p2, p1)/(p2.mass) + interacty(p2, p3)/(p2.mass)
    p2.motion()

    x2[i] = p2.x
    y2[i] = p2.y

    p3.time = i
    p3.field()
    p3.accelerationx += interactx(p3, p1)/(p3.mass) + interactx(p3, p2)/(p3.mass)
    p3.accelerationy += interacty(p3, p1)/(p3.mass) + interacty(p3, p2)/(p3.mass)
    p3.motion()

    x3[i] = p3.x
    y3[i] = p3.y

    t[i] = i

gridx = np.linspace(-10, 10, 100)
gridy = np.linspace(-10, 10, 100)

A, B = np.meshgrid(gridx, gridy)
C = fieldStrength(A, B, 0)
plt.contour(A, B, C, colors = 'black')
plt.show()

fig = plt.figure()
ax = fig.gca(projection='3d')

ax.plot(x1, y1, t, 'y')
ax.plot(x2, y2, t, 'r')
ax.plot(x3, y3, t, 'g')


#plt.plot(x1, y1, 'yo')
#plt.plot(x2, y2, 'ro')
#plt.plot(x3, y3, 'go')

#plt.plot(x1[0], y1[0], 'ko')
#plt.plot(x2[0], y2[0], 'ko')
#plt.plot(x3[0], y3[0], 'ko')
plt.show()



        
