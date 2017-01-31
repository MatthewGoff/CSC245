import pygame
from crate import Crate
from ice import Ice
from moss import Moss
from stone import Stone
from sheep import Sheep
import copy

# Level generator class
# The first three levels are preprogrammed, after that random (within limitations) levels are generated
# Author: Nik Lockwood
# Winter 2017

class Levels:

    def __init__(self, window_width, window_height):
        self.window_width = window_width
        self.window_height = window_height

        self.levels = []
        self.init_levels()

    def init_levels(self):
        level1 = Level()
        level1.enemies.add(Sheep((400, 400), (0, 0), 100, 100, "sheep"))
        level1.blocks.add(Moss((500, 500), (0, 0), 100, 100, "moss"))
        level1.blocks.add(Crate((600, 600), (0, 0), 100, 100, "crate"))
        level1.blocks.add(Stone((700, 700), (0, 0), 100, 100, "stone"))
        level1.blocks.add(Ice((800, 800), (0, 0), 100, 100, "Ice"))

        level2 = Level()
        level2.enemies.add(Sheep((900, 900), (0, 0), 100, 100, "sheep"))
        level2.blocks.add(Moss((500, 500), (0, 0), 100, 100, "moss"))
        level2.blocks.add(Crate((600, 600), (0, 0), 100, 100, "crate"))
        level2.blocks.add(Stone((700, 700), (0, 0), 100, 100, "stone"))
        level2.blocks.add(Ice((800, 800), (0, 0), 100, 100, "Ice"))

        level3 = Level()
        level3.blocks.add(Moss((800, 800), (0, 0), 200, 200, "The wall"))

        self.levels = [level1, level2, level3]

    def get_level(self, i):
        self.init_levels()
        return self.levels[i]


class Level:

    def __init__(self):
        self.enemies = copy.copy(pygame.sprite.Group())
        self.blocks = copy.copy(pygame.sprite.Group())

    def get_enemies(self):
        return self.enemies

    def get_blocks(self):
        return self.blocks
