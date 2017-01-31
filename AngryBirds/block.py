# A block object for angy birds
# Author: Matthew  Goff, Nik Lockwood
# Winter 2017

import pygame
import pymunk
import math


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
        self.position = position[0], position[1]
        self.velocity = velocity[0], velocity[1]
        self.poly = pymunk.Poly.create_box(self, (width, height))
        x = position[0]
        y = position[1]
        '''self.poly = pymunk.Poly(self, [(- width/2, - height/2),
                                       (width/2, - height/2),
                                       (width/2, height/2),
                                       (- width/2, height/2)])'''

        self.identifier = identifier

        self.init_image = pygame.transform.smoothscale(
            image.convert_alpha(),
            (width, height))
        self.image = self.init_image

        self.update_rect()

    def update_rect(self):
        '''
        Try to line up the bounds of the sprite with the physical object.
        Almost accomplishes that in an inexplicable way.
        :return:
        '''

        points = self.poly.get_vertices()
        top = float("inf")
        bottom = -1*float("inf")
        left = float("inf")
        right = -1*float("inf")
        for point in points:
            top = min(top, point.y)
            bottom = max(bottom, point.y)
            left = min(left, point.x)
            right = max(right, point.x)

        height = int(bottom - top)
        width = int(right - left)
        angle = math.degrees(-self.angle)
        self.image = pygame.transform.smoothscale(
            self.init_image,
            (width, height))
        self.image = pygame.transform.rotate(self.image, angle)

        self.rect = pygame.Rect(self.position.x + left/2,
                                self.position.y + top/2,
                                width,
                                height)
