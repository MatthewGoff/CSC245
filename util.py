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
INITIAL_SPEED = 1.0        # pixels per "tick"
RADIUS_RANGE = (10, 50)    # in pixels

# Physics parameters
DRAG = False
DRAG_COEFFICIENT = -0.0005  # Try making it positive ;)
INVERSE_MASS = False

# Display parameters
DRAW_VELOCITY = False
DRAW_QUADTREE = True
COLOR_SCHEME = "gradient"     # bounce, random, gradient, speed (enumerators were released in python 3.4)


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
            angle = math.atan(self.get_y()/self.get_x())+math.pi
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


class Rectangle:

    def __init__(self, top, bottom, left, right):
        self.top = top
        self.bottom = bottom
        self.left = left
        self.right = right

        self.v_median = (self.top + self.bottom) / 2.0
        self.h_median = (self.left + self.right) / 2.0

    def get_top(self):
        return self.top

    def get_bottom(self):
        return self.bottom

    def get_left(self):
        return self.left

    def get_right(self):
        return self.right

    def get_v_median(self):
        return self.v_median

    def get_h_median(self):
        return self.h_median

    def get_center(self):
        return Vec2D(self.h_median, self.v_median)

    def __str__(self):
        return "("+str(self.top)+","+str(self.bottom)+","+str(self.left)+","+str(self.right)+")"


class Quadtree:
    MAX_OBJECTS = 4
    MAX_LEVELS = 7

    def __init__(self, level, bounds):
        self.level = level
        self.members = []
        self.bounds = bounds
        self.nodes = [None, None, None, None]

    def clear(self):
        self.members = []
        for i in range(0,4):
            if self.nodes[i] is not None:
                self.nodes[i].clear()
                self.nodes[i] = None

    def split(self):
        self.nodes[0] = Quadtree(self.level + 1, Rectangle(self.bounds.get_top(),
                                                           self.bounds.get_v_median(),
                                                           self.bounds.get_h_median(),
                                                           self.bounds.get_right()))
        self.nodes[1] = Quadtree(self.level + 1, Rectangle(self.bounds.get_top(),
                                                           self.bounds.get_v_median(),
                                                           self.bounds.get_left(),
                                                           self.bounds.get_h_median()))
        self.nodes[2] = Quadtree(self.level + 1, Rectangle(self.bounds.get_v_median(),
                                                           self.bounds.get_bottom(),
                                                           self.bounds.get_left(),
                                                           self.bounds.get_h_median()))
        self.nodes[3] = Quadtree(self.level + 1, Rectangle(self.bounds.get_v_median(),
                                                           self.bounds.get_bottom(),
                                                           self.bounds.get_h_median(),
                                                           self.bounds.get_right()))


    def get_index(self, member):

        if member.get_position().get_y() < (self.bounds.get_v_median() - member.get_radius()):
            if member.get_position().get_x() > (self.bounds.get_h_median() + member.get_radius()):
                return 0
            elif member.get_position().get_x() < (self.bounds.get_h_median() - member.get_radius()):
                return 1
        elif member.get_position().get_y() > (self.bounds.get_v_median() + member.get_radius()):
            if member.get_position().get_x() > (self.bounds.get_h_median() + member.get_radius()):
                return 3
            elif member.get_position().get_x() < (self.bounds.get_h_median() - member.get_radius()):
                return 2

        return -1

    def insert(self, member):
        if self.nodes[0] is not None:
            index = self.get_index(member)
            if index != -1:
                self.nodes[index].insert(member)

                return

        self.members += [member]

        if (len(self.members) > self.MAX_OBJECTS) and (self.level < self.MAX_LEVELS):
            if self.nodes[0] is None:
                self.split()

            i = 0
            while i < len(self.members):
                index = self.get_index(self.members[i])
                if index != -1:
                    self.nodes[index].insert(self.members.pop(i))
                else:
                    i += 1

    def retrieve_neighbors(self, member):
        index = self.get_index(member)
        if (index != -1) and (self.nodes[0] is not None):
            return self.members + self.nodes[index].retrieve_neighbors(member)
        else:
            return self.members

    def get_nodes(self):
        return self.nodes

    def is_split(self):
        return self.nodes[0] is not None

    def get_bounds(self):
        return self.bounds

    def get_population(self):
        return len(self.members)

    def __str__(self):
        return self.to_string(0)

    def to_string(self, level):
        string = "\n" + "\t"*level
        string += "Quadtree at "+self.bounds.__str__()
        string += "(level "+str(level)+") ("+str(len(self.members))+" members)"
        if self.is_split():
            for i in range(0,4):
                string += self.nodes[i].to_string(level+1)
        else:
            string += "(Not split)"

        return string


