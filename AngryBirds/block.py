# A block object for angy birds
# Author: Matthew  Goff, Nik Lockwood
# Winter 2017

import pygame
import pymunk


class Block(pymunk.Body, pygame.sprite.Sprite):

    def __init__(self,
                 position,
                 velocity,
                 height,
                 width,
                 mass,
                 moment,
                 image,
                 identifier,
                 body_type=pymunk.Body.DYNAMIC):
        pygame.sprite.Sprite.__init__(self)
        pymunk.Body.__init__(self, mass, moment, body_type)
        self.poly = pymunk.Poly.create_box(self, size=(width, height))
        self.position = position.x, position.y
        self.velocity = velocity.x, velocity.y
        self.identifier = identifier

        self.init_image = pygame.transform.smoothscale(
            image.convert_alpha(),
            (width, height))
        self.image = self.init_image

        self.update_rect()

    def update_rect(self):
        points = self.poly.get_vertices()
        top = float("inf")
        left = float("inf")
        for point in points:
            top = min(top, point.y)
            left = min(left, point.x)

        self.rect = pygame.Rect(self.position.x + left,
                                self.position.y + top,
                                self.poly.radius*2,
                                self.poly.radius*2)
