# A crate object for angy birds
# Author: Matthew  Goff, Nik Lockwood
# Winter 2017

import pygame
from GameEngine import game_objects


class Crate(game_objects.Block, pygame.sprite.Sprite):

    def __init__(self,
                 position,
                 velocity,
                 height,
                 width,
                 mass,
                 physics_environment,
                 listener,
                 identifier):
        pygame.sprite.Sprite.__init__(self)
        game_objects.Block.__init__(self,
                                    position,
                                    velocity,
                                    height,
                                    width,
                                    pygame.Color("white"),
                                    identifier)
        self.physics_environment = physics_environment
        self.mass = mass
        self.listener = listener

        for wall in self.walls:
            wall.mass = self.mass

        image = pygame.image.load("images/Grumpy flappy bird/PNG/frame-1.png")
        self.image = pygame.transform.smoothscale(
            image.convert_alpha(),
            (self.width, self.height))

        self.update_rect()

    def update_rect(self):
        self.rect = pygame.Rect(self.get_top(),
                                self.get_left(),
                                self.width,
                                self.height)

    def notify_collision(self, wall, other):
        game_objects.Block.notify_collision(self, wall, other)
        self.listener(self, other)
