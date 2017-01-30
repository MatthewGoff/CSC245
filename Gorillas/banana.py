# A simple banana class
# Author: Matthew Anderson
# Winter 2017

import pygame
from ball import Ball
from building import Building
from vector import Vector
from gorilla import Gorilla


class Banana(Ball, pygame.sprite.Sprite):

    def __init__(self, x, y, thrower):
        pygame.sprite.Sprite.__init__(self)
        Ball.__init__(self, x, y, 10, pygame.color.Color("Yellow"))
        self.init_image = pygame.transform.smoothscale(pygame.image.load("images/banana.png").convert_alpha(),
                                                  (self.radius*2, self.radius*2))
        self.image = self.init_image

        self.vel = Vector(0, 0)
        self.mass = 10
        self.update_rect()
        self.hit = False
        self.colliding = False
        self.angle = 0
        self.thrower = thrower

    def update_rect(self):
        self.rect = pygame.Rect(self.pos.x-self.radius,self.pos.y-self.radius,self.radius*2,self.radius*2)

    def simulate(self, dt):

        acc = Vector(0, 9.8) - self.vel.scale(0.1 / self.mass)

        self.vel += acc.scale(dt)
        if self.colliding:
            self.vel = self.vel.scale(.75)
            if self.vel.length() < 1:
                self.vel = Vector(0.0, 0.0)
        dpos = self.vel.scale(dt)
        self.rect.move_ip(dpos.x, dpos.y)
        self.pos += dpos
        self.update_rect()
        self.angle += 5
        self.image = pygame.transform.rotate(self.init_image,self.angle)

    def collide(self, objs):

            self.colliding = False

            if not self.hit and len(objs) > 0:

                if isinstance(objs[0], Building):

                    for building in objs:

                        for bumper in building.bumpers:
                            self.colliding = self.colliding or Ball.collideBumper(self, bumper)

                elif isinstance(objs[0], Gorilla):

                    for player in objs:
                        if player != self.thrower and Ball.collideBall(self, player):
                            player.lives -= 1
                            self.hit = True
                            self.colliding = True

            return self.colliding





