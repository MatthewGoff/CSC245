# A simple 1D wall class
# Author: Matthew Anderson, Kristina Striegnitz, John Rieffel
# Winter 2017

import pygame
from vector import Vector

class Bumper:

    def __init__(self, sx, sy, ex, ey, color):
        self.start = Vector(sx, sy)
        self.end = Vector(ex, ey)
        self.color = color
        self.vel = Vector(0.0, 0.0)  # Used to move paddles

    def draw(self, window):
        pygame.draw.line(window, self.color, (self.start.x, self.start.y), (self.end.x, self.end.y), 4)

    def simulate(self, dt):
        dpos = self.vel.scale(dt)
        self.start += dpos
        self.end += dpos

    def set_vel(self,dx,dy):
        self.vel = Vector(dx,dy)