# A crate object for angy birds
# Author: Matthew  Goff, Nik Lockwood
# Winter 2017

import pygame
from block import Block


class Stone(Block, pygame.sprite.Sprite):
    MASS = 1
    MOMENT = 1

    def __init__(self,
                 position,
                 velocity,
                 height,
                 width,
                 listener,
                 identifier):
        pygame.sprite.Sprite.__init__(self)
        Block.__init__(self,
                       position,
                       velocity,
                       height,
                       width,
                       Stone.MASS,
                       Stone.MOMENT,
                       pygame.image.load(
                           "images/brick_game_asset_game_obstacles/PNG/brick_1.png"),
                       listener,
                       identifier)
