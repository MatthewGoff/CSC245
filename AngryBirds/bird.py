# An angry bird for the angry birds game
# Author: Matthew  Goff, Nik Lockwood
# Winter 2017

import pygame
from GameEngine import game_objects


class Bird(game_objects.Ball, pygame.sprite.Sprite):

    def __init__(self,
                 position,
                 velocity,
                 radius,
                 mass,
                 physics_environment,
                 identifier):

        pygame.sprite.Sprite.__init__(self)

        game_objects.Ball.__init__(self, position, velocity, radius, identifier)
        self.physics_environment = physics_environment
        self.mass = mass

        #self.image = pygame.transform.smoothscale(
        #    image,
        #    (self.radius * 2, self.radius * 2))

        self.update_rect()

    def update_rect(self):
        self.rect = pygame.Rect(self.position.get_x(),
                                self.position.get_y(),
                                self.radius*2,
                                self.radius*2)

    def simulate(self):
        acceleration = self.physics_environment.gravity
        self.velocity += acceleration
        self.position += self.velocity

        self.update_rect()