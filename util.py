import math
import random
import sys
import pygame

seed = random.randint(0, sys.maxint)
print "seed = "+str(seed)
RandGen = random.Random(seed)

# Window Parameters
WINDOW_WIDTH = 640 * 2
WINDOW_HEIGHT = 480 * 2

# Ball parameters
NUM_BALLS = 100
INITIAL_SPEED = 1.2           # pixels per "tick"
RADIUS_RANGE = (10, 50)    # in pixels

# Physics parameters
DRAG = False
DRAG_COEFFICIENT = -0.0005  # Try making it positive ;)
INVERSE_MASS = False

# Display parameters
DRAW_VELOCITY = False
COLOR_SCHEME = "gradient"     # bounce, random, gradient, speed (yes, its a shitty enumerator)

def random_color():
    return pygame.color.Color(RandGen.randint(0, 255),
                              RandGen.randint(0, 255),
                              RandGen.randint(0, 255),
                              1)

class Vec2D:

    def __init__(self, x, y):
        self.vec = (x, y)

    def add(self, other):
        return Vec2D(self.get_x() + other.get_x(), self.get_y() + other.get_y())

    def sub(self, other):
        return Vec2D(self.get_x() - other.get_x(), self.get_y() - other.get_y())

    def scale(self, scalar):
        return Vec2D(self.get_x() * scalar, self.get_y() * scalar)

    def dot(self, other):
        return self.get_x()*other.get_x()+self.get_y()*other.get_y()

    def get_x(self):
        return self.vec[0]

    def get_y(self):
        return self.vec[1]

    def mag(self):
        return (self.get_x()**2+self.get_y()**2)**.5

    def angle(self):
        #Not working!
        print "calculating angle"
        print "x = "+str(self.get_x())
        print "y = "+str(self.get_y())

        angle = 0
        if self.get_x() == 0:
            if self.get_y() > 0:
                angle = math.pi/2
            else:
                angle = -1*math.pi/2
        elif self.get_x() < 0:
            print "need to revers"
            print "atan = "+str(math.atan(self.get_y()/self.get_x()))
            angle = math.atan(self.get_y()/self.get_x())+(math.pi)
        else:
            angle = math.atan(self.get_y()/self.get_x())

        print "returning "+str(angle)
        return angle

    def unit(self):
        if self.mag() == 0:
            return Vec2D(0, 0)
        else:
            return self.scale(1.0/self.mag())

    def perp(self):
        return Vec2D(-1 * self.get_y(), self.get_x())

    def __str__(self):
        return "<"+str(self.get_x())+","+str(self.get_y())+">"