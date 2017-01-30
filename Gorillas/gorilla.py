# A simple gorilla class
# Author: Matthew Anderson
# Winter 2017

import pygame, math
from vector import Vector
from building import Building
from ball import Ball


class Gorilla(Ball, pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        Ball.__init__(self, x, y, 25, pygame.color.Color("Red"))
        self.image = pygame.transform.smoothscale(pygame.image.load("images/donkey_kong.png").convert_alpha(),
                                                  (self.radius*2, self.radius*2))

        self.vel = Vector(0, 0)
        self.mass = 1
        self.update_rect()
        self.colliding = False
        self.lives = 5
        self.angle = -90
        self.power = 50

    def update_rect(self):
        self.rect = pygame.Rect(self.pos.x-self.radius,self.pos.y-self.radius,self.radius*2,self.radius*2)

    def update_aim(self,dangle,dpower):
        self.angle += dangle
        self.power +=dpower
        self.power = max(1, min(100, self.power))

    def aim_at(self, x,y):
        dx = x - self.pos.x
        dy = y - self.pos.y
        self.power = Vector(dx,dy).length()
        self.power = max(1, min(100, self.power))
        if dx >= 0:
            self.angle = math.degrees(math.atan(dy / dx))
        else:
            self.angle = -(180 - math.degrees(math.atan(dy / dx)))

    def draw_aim(self,window):

        x1 = self.pos.x
        y1 = self.pos.y
        x2 = x1 + self.power * math.cos(math.radians(self.angle))
        y2 = y1 + self.power * math.sin(math.radians(self.angle))

        pygame.draw.line(window, pygame.color.Color("Green"), (x1, y1), (x2, y2), 2)


    def simulate(self, dt):

        acc = Vector(0,9.8) - self.vel * (0.1 / self.mass)

        if self.colliding:
            self.vel *= 0.6
            if self.vel.length() < 1:
                self.vel = Vector(0.0, 0.0)

        dpos = self.vel * dt
        self.pos += dpos
        self.vel += acc * dt

        self.rect.move_ip(dpos.x, dpos.y)
        self.update_rect()

    def collide(self, objs):

        self.colliding = False

        if len(objs) > 0:

            if isinstance(objs[0], Building):

                for building in objs:

                    for bumper in building.bumpers:

                        self.colliding = self.colliding or Ball.collideBumper(self, bumper)


        return self.colliding


