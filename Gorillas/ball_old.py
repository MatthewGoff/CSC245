# A simple 2D ball class
# Author: Matthew Anderson, Kristina Striegnitz, John Rieffel
# Winter 2017

import pygame
from vector import Vector
from bumper import Bumper

class Ball(object):

    def __init__(self, x, y, radius, color):
        self.pos = Vector(x, y)
        self.vel = Vector(0.0, 0.0)
        self.radius = radius
        self.color = color
        self.mass = 1

    def set_vel(self, dx, dy):
        self.vel = Vector(dx, dy)

    def simulate(self, dt):
        dpos = self.vel.scale(dt)
        self.pos = self.pos + dpos

    def draw(self, window):
        pygame.draw.circle(window, self.color, (int(self.pos.x), int(self.pos.y)), self.radius)

    def collide(self, obj, bounce=False):

        collided = False

        if isinstance(obj, Bumper):

            from_lc = self.pos - obj.left_corner
            from_rc = self.pos - obj.right_corner
            wall_vec = obj.left_corner - obj.right_corner

            if from_lc.length() <= self.radius:
                # Collide with left end of wall
                collided = True
                collision_vec = from_lc
            elif from_rc.length() <= self.radius:
                # Collide with right end of wall
                collided = True
                collision_vec = from_rc
            else:
                # Collide with middle of wall
                para_factor = (from_rc * wall_vec) / (wall_vec.length())
                from_rc_perp = wall_vec.perp_comp(from_rc)

                if 0 <= para_factor <= wall_vec.length() and from_rc_perp.length() <= self.radius:
                    collided = True
                    collision_vec = from_rc_perp

            if collided and bounce:
                #print "Bounced!"
                # Reflect velocity in direction of normal
                vel_para = collision_vec.para_comp(self.vel)
                if vel_para * collision_vec < 0:
                    self.vel += vel_para.scale(-2)

        elif isinstance(obj, Ball):

            dpos = self.pos - obj.pos
            dvel = self.vel - obj.vel
            if (dpos.length() <= self.radius + obj.radius) and dpos * dvel <= 0:
                collided = True
                if bounce:
                    dv1 = dpos.scale(- (2 * obj.mass) / (self.mass + obj.mass) * (dpos * dvel) / ((dpos.length())**2))
                    dv2 = dpos.scale((2 * self.mass) / (self.mass + obj.mass) * (dpos * dvel) / ((dpos.length())**2))
                    self.vel += dv1
                    obj.vel += dv2

        return collided

