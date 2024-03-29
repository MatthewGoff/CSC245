# A crate object for angy birds
# Author: Matthew  Goff, Nik Lockwood
# Winter 2017

import pygame
import pymunk
from block import Block


class Moss(Block, pygame.sprite.Sprite):
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
                       Moss.MASS,
                       Moss.MOMENT,
                       pygame.image.load(
                           "images/moss square box tileset game obstacle/PNG/moss_tile.png"),
                       identifier,
                       body_type=pymunk.Body.STATIC)

