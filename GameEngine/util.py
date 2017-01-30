# Some utility methods for games using pygame.
# Author: Matthew Goff
# Winter 2017

import random
import sys
import pygame

seed = random.randint(0, sys.maxint)
#seed = 949109774
RandGen = random.Random(seed)

# Physics parameters
DRAG = False
DRAG_COEFFICIENT = -0.0005  # Try making it positive ;)


def get_seed():
    return seed


def random_color():
    return pygame.Color(RandGen.randint(0, 255),
                        RandGen.randint(0, 255),
                        RandGen.randint(0, 255),
                        255)


def random_velocity(range):
    x_mag = RandGen.uniform(range[0], range[1])
    y_mag = RandGen.uniform(range[0], range[1])
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

    @classmethod
    def from_pygame_rect(cls, pygame_rect):
        return cls(pygame_rect.top,
                   pygame_rect.bottom,
                   pygame_rect.left,
                   pygame_rect.right)

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

        if member.get_bottom() < self.bounds.get_v_median():
            if member.get_left() > self.bounds.get_h_median():
                return 0
            elif member.get_right() < self.bounds.get_h_median():
                return 1
        elif member.get_top() > self.bounds.get_v_median():
            if member.get_left() > self.bounds.get_h_median():
                return 3
            elif member.get_right() < self.bounds.get_h_median():
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


def draw_quadtree(window, quadtree):
    if quadtree.is_split():
        bounds = quadtree.get_bounds()
        pygame.draw.line(window,
                         pygame.color.Color("white"),
                         (bounds.get_h_median(), bounds.get_top()),
                         (bounds.get_h_median(), bounds.get_bottom()),
                         1)
        pygame.draw.line(window,
                         pygame.color.Color("white"),
                         (bounds.get_left(), bounds.get_v_median()),
                         (bounds.get_right(), bounds.get_v_median()),
                         1)
        for i in range(0, 4):
            draw_quadtree(window, quadtree.get_nodes()[i])

    draw_text(window,
              str(quadtree.get_population()),
              quadtree.get_bounds().get_center().to_tuple(),
              24)


def draw_text(window, text_param, center, size):
    basic_font = pygame.font.SysFont(None, size)
    text = basic_font.render(text_param, True, (255, 255, 255), (0, 0, 0))
    text_rect = text.get_rect()
    text_rect.centerx = center[0]
    text_rect.centery = center[1]
    window.blit(text, text_rect)


