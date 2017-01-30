# a single field in a minesweeper game
# Author: Matthew Goff
# Winter 2017

import pygame


class Square(pygame.sprite.Sprite):
    pygame.sprite.Sprite.__init__()
    ONE = pygame.transform.smoothscale(
        pygame.image.load(
            "images/Mines/1.png").convert_alpha(),
        (16, 16))

    @classmethod
    def __init__(cls):
        pygame.sprite.Sprite.__init__(self)

    def __init__(self, position, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.image = Square.ONE

        self.rect = pygame.Rect(position[0],
                                position[1],
                                height,
                                width)
