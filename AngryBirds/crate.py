# A crate object for angy birds
# Author: Matthew  Goff, Nik Lockwood
# Winter 2017

import pygame
from block import Block


class Crate(Block, pygame.sprite.Sprite):
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
                       Crate.MASS,
                       Crate.MOMENT,
                       pygame.image.load(
                           "images/wooden brick tile game obstacle/PNG/1.png"),
                       identifier)