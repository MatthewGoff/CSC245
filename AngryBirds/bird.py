# An angry bird for the angry birds game
# Author: Matthew  Goff, Nik Lockwood
# Winter 2017

import pygame
import pymunk


class Bird(pymunk.Body, pygame.sprite.Sprite):

    def __init__(self,
                 position,
                 velocity,
                 radius,
                 mass,
                 identifier):

        pygame.sprite.Sprite.__init__(self)
        pymunk.Body.__init__(self, 1, 1666)
        self.poly = pymunk.Circle(self, radius)

        self.position = position.x, position.y
        self.velocity = velocity.x, velocity.y
        self.identifier = identifier

        self.update_rect()

    def update_rect(self):
        self.rect = pygame.Rect(self.position.x - self.poly.radius,
                                self.position.y - self.poly.radius,
                                self.poly.radius*2,
                                self.poly.radius*2)

    def setVel(self, velocity):
        self.velocity = velocity.x, velocity.y

    def pullSpot(self, stretchPos):
        self.position = stretchPos.x, stretchPos.y