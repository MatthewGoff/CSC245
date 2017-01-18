import random
import sys
import pygame

seed = random.randint(0, sys.maxint)
#seed = 1062520888
RandGen = random.Random(seed)

# Window Parameters
WINDOW_WIDTH = 640*2
WINDOW_HEIGHT = 480*2
WINDOW_COLOR = pygame.Color("black")

# Ball parameters
NUM_BALLS = 10
SPEED_RANGE = (.5,1)        # pixels per "tick"
RADIUS_RANGE = (10, 50)    # in pixels

# Physics parameters
DRAG = False
DRAG_COEFFICIENT = -0.0005  # Try making it positive ;)
INVERSE_MASS = False

# Play parameters
PADDLE_SPEED = 3
PADDLE_HEIGHT = 300
PADDLE_WIDTH = 20

# Display parameters
DRAW_VELOCITY = False
DRAW_QUADTREE = False
LABEL_OBJECTS = False
CONTINUOUS = True
COLOR_SCHEME = "random"     # bounce, random, gradient, speed (enumerators were released in python 3.4)


def get_seed():
    return seed


def random_color():
    return pygame.Color(RandGen.randint(0, 255),
                        RandGen.randint(0, 255),
                        RandGen.randint(0, 255),
                        255)


def random_velocity():
    x_mag = RandGen.uniform(SPEED_RANGE[0], SPEED_RANGE[1])
    y_mag = RandGen.uniform(SPEED_RANGE[0], SPEED_RANGE[1])
    if RandGen.uniform(0, 1) > 0.5:
        x_mag *= -1
    if RandGen.uniform(0, 1) > 0.5:
        y_mag *= -1

    return Vec2D(x_mag, y_mag)


def list_to_string(ls):
    string = "["
    for i in range(0, len(ls)-1):
        string += str(ls[i])+","

    if len(ls) != 0:
        string += str(ls[-1])

    string += "]"
    return string


class Vec2D:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vec2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vec2D(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar):
        return Vec2D(self.x * scalar, self.y * scalar)

    def __div__(self, scalar):
        return Vec2D(self.x / scalar, self.y / scalar)

    def dot(self, other):
        return self.x*other.x+self.y*other.y

    def mag(self):
        return (self.get_x()**2+self.get_y()**2)**.5

    def is_zero(self):
        return self.x == 0 and self.y == 0

    def unit(self):
        if self.is_zero():
            return Vec2D(0, 0)
        else:
            return self/self.mag()

    def perp(self):
        return Vec2D(-1 * self.y, self.x)

    def to_tuple(self):
        return self.x, self.y

    def get_y(self):
        return self.y

    def get_x(self):
        return self.x

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

    def __init__(self, bounds, level=0):
        self.level = level
        self.members = []
        self.bounds = bounds
        self.nodes = [None, None, None, None]

    def clear(self):
        self.members = []
        for i in range(0, 4):
            if self.nodes[i] is not None:
                self.nodes[i].clear()
                self.nodes[i] = None

    def split(self):
        self.nodes[0] = Quadtree(Rectangle(self.bounds.get_top(),
                                           self.bounds.get_v_median(),
                                           self.bounds.get_h_median(),
                                           self.bounds.get_right()),
                                 self.level + 1)
        self.nodes[1] = Quadtree(Rectangle(self.bounds.get_top(),
                                           self.bounds.get_v_median(),
                                           self.bounds.get_left(),
                                           self.bounds.get_h_median()),
                                 self.level + 1)
        self.nodes[2] = Quadtree(Rectangle(self.bounds.get_v_median(),
                                           self.bounds.get_bottom(),
                                           self.bounds.get_left(),
                                           self.bounds.get_h_median()),
                                 self.level + 1)
        self.nodes[3] = Quadtree(Rectangle(self.bounds.get_v_median(),
                                           self.bounds.get_bottom(),
                                           self.bounds.get_h_median(),
                                           self.bounds.get_right()),
                                 self.level + 1)

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

    def insert_many(self, ls):
        for e in ls:
            self.insert(e)

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

    def get_neighbors(self, member):
        index = self.get_index(member)
        if (index != -1) and (self.nodes[0] is not None):
            return self.members + self.nodes[index].get_neighbors(member)

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


