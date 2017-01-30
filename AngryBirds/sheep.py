# A sheep object for angy birds
# Author: Matthew  Goff, Nik Lockwood
# Winter 2017

import pygame
from block import Block


class Sheep(Block, pygame.sprite.Sprite):
    MASS = 1
    MOMENT = 1

    def __init__(self,
                 position,
                 velocity,
                 height,
                 width,
                 identifier):
        pygame.sprite.Sprite.__init__(self)
        Block.__init__(self,
                       position,
                       velocity,
                       height,
                       width,
                       Sheep.MASS,
                       Sheep.MOMENT,
                       pygame.image.load(
                           "images/RoundAnimals/sheep.png"),
                       identifier)