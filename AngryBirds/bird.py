# An angry bird for the angry birds game
# Author: Matthew  Goff, Nik Lockwood
# Winter 2017

import pygame
from GameEngine import game_objects


class Bird(game_objects.Ball, pygame.sprite.Sprite):

    def __init__(self, position, velocity, radius, mass, image, identifier):
        pygame.sprite.Sprite.__init__(self)
        game_objects.Ball.__init__(self, position, velocity, radius, identifier)
        self.mass = mass

        self.image = pygame.transform.smoothscale(
            image.convert_alpha(),
            (self.radius * 2, self.radius * 2))

        self.update_rect()

    def update_rect(self):
        self.rect = pygame.Rect(self.position.get_x()-self.radius,
                                self.position.get_y()-self.radius,
                                self.radius*2,
                                self.radius*2)

    def simulate(self):
        game_objects.Ball.simulate(self)
        self.update_rect()