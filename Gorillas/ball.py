# A simple 2D ball class
# Author: Matthew Anderson, Kristina Striegnitz, John Rieffel
# Winter 2017

import pygame, random, math
from vector import Vector
from bumper import Bumper


def get_rand_color():

    return pygame.color.Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), 255)

def get_rand_vel(len_min,len_max):

    # Returns uniform random Vector between given lengths.
    theta = math.radians(random.uniform(0.0, 360.0))
    mag = random.uniform(len_min,len_max)
    return Vector(mag * math.cos(theta), mag * math.sin(theta))



class Ball(object):

    def __init__(self,x,y, radius, color):

        # Instance attributes (associated with an individual copy of Ball).
        self.radius = radius
        self.pos = Vector(x, y)
        self.vel = Vector(0, 0)
        self.color = get_rand_color()


    def __str__(self):

        return str(self.pos) + " @ " + str(self.vel)

    def set_vel(self,vx, vy):
        self.vel = Vector(vx, vy)

    def simulate(self, dt):
        dpos = self.vel.scale(dt)
        self.pos = self.pos + dpos

    def draw(self, window):
        pygame.draw.circle(window, self.color, (int(self.pos.x), int(self.pos.y)), self.radius)


    def collideBumper(self, bumper):

        collided = False

        l = bumper.end - bumper.start
        d = self.pos - bumper.start
        e = self.pos - bumper.end

        d_para_scalar = (d * l) / l.length()
        d_para = l * (d_para_scalar / l.length())
        d_perp = d - d_para

        if d_perp.length() <= self.radius and 0 <= d_para_scalar <= l.length():
            # Collides with rectangle around bumper
            collided = True
            norm = d_perp * (1.0/d_perp.length())
        elif d.length() <= self.radius:
            # Collides with circle around start
            collided = True
            norm = d * (1.0/d.length())
        elif e.length() <= self.radius: # Fixed bad style
            # Collides with circle around end
            collided = True
            norm = e * (1.0 /e.length())

        if collided:
            if self.vel * norm < 0:
                vel_para = norm * (norm * self.vel)
                vel_perp = self.vel - vel_para
                self.vel = vel_perp - vel_para

        return collided

    def collideBall(self, b2):

        collided = False
        b1 = self
        dpos = b1.pos - b2.pos
        dvel = b1.vel - b2.vel
        # Test if overlapping and moving into each other.
        # The part after the and prevent balls from "sticking" together.
        if (dpos.length() <= b1.radius + b2.radius) and dpos * dvel < 0:
            collided = True

            b1.vel = b1.vel - dpos * (2 * b2.mass / (b1.mass + b2.mass)) * ((dpos * dvel) / (dpos.length() ** 2))
            b2.vel = b2.vel + dpos * (2 * b1.mass / (b1.mass + b2.mass)) * ((dpos * dvel) / (dpos.length() ** 2))

        return collided