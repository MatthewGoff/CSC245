# An slingshot object for angry birds
# Author: Matthew  Goff, Nik Lockwood
# Winter 2017

import pygame


class Slingshot(pygame.sprite.Sprite):

    def __init__(self, position, radius, identifier):
        pygame.sprite.Sprite.__init__(self)
        self.position = position
        self.radius = radius
        self.identifier = identifier

        self.image = pygame.transform.smoothscale(
            pygame.image.load("images/slingshot.png").convert_alpha(),
            (self.radius * 2, self.radius * 2))

        self.update_rect()

    def update_rect(self):
        self.rect = pygame.Rect(self.position.get_x()-self.radius,
                                self.position.get_y()-self.radius,
                                self.radius*2,
                                self.radius*2)