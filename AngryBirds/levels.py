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
        level1.blocks.add(Moss((150, 1030), (0, 0), 300, 100, "moss"))
        level1.blocks.add(Moss((450, 1030), (0, 0), 300, 100, "moss"))
        level1.blocks.add(Moss((550, 1030), (0, 0), 100, 100, "moss"))
        level1.blocks.add(Moss((650, 1030), (0, 0), 100, 100, "moss"))
        level1.blocks.add(Moss((750, 1030), (0, 0), 100, 100, "moss"))
        level1.blocks.add(Moss((850, 1030), (0, 0), 100, 100, "moss"))
        level1.blocks.add(Moss((950, 1030), (0, 0), 100, 100, "moss"))
        level1.blocks.add(Moss((950, 780), (0, 0), 100, 400, "moss"))
        level1.blocks.add(Moss((950, 380), (0, 0), 100, 400, "moss"))
        level1.blocks.add(Crate((600, 600), (0, 0), 100, 100, "crate"))
        level1.blocks.add(Stone((700, 700), (0, 0), 100, 100, "stone"))
        level1.blocks.add(Ice((800, 800), (0, 0), 100, 100, "Ice"))

        level2 = Level()
        level2.enemies.add(Sheep((900, 900), (0, 0), 100, 100, "sheep"))
        level2.enemies.add(Sheep((300, 900), (0, 0), 100, 100, "sheep"))
        level1.blocks.add(Moss((150, 1030), (0, 0), 300, 100, "moss"))
        level1.blocks.add(Moss((450, 1030), (0, 0), 300, 100, "moss"))
        level1.blocks.add(Moss((550, 1030), (0, 0), 100, 100, "moss"))
        level1.blocks.add(Moss((650, 1030), (0, 0), 100, 100, "moss"))
        level1.blocks.add(Moss((750, 1030), (0, 0), 100, 100, "moss"))
        level1.blocks.add(Moss((850, 1030), (0, 0), 100, 100, "moss"))
        level1.blocks.add(Moss((950, 1030), (0, 0), 100, 100, "moss"))
        level1.blocks.add(Moss((950, 780), (0, 0), 100, 400, "moss"))
        level1.blocks.add(Moss((950, 380), (0, 0), 100, 400, "moss"))
        level2.blocks.add(Crate((600, 600), (0, 0), 100, 100, "crate"))
        level2.blocks.add(Stone((700, 700), (0, 0), 100, 100, "stone"))
        level2.blocks.add(Ice((800, 800), (0, 0), 100, 100, "Ice"))

        level4 = Level()
        level4.blocks.add(Moss((800, 800), (0, 0), 200, 200, "The wall"))
        level4.blocks.add(Moss((100, 800), (0, 0), 200, 200, "back wall"))

        level3 = Level()
        level3.blocks.add(Moss((150, 1030), (0, 0), 300, 100, "moss"))
        level3.blocks.add(Moss((450, 1030), (0, 0), 300, 100, "moss"))
        level3.blocks.add(Moss((550, 1030), (0, 0), 100, 100, "moss"))
        level3.blocks.add(Moss((650, 1030), (0, 0), 100, 100, "moss"))
        level3.blocks.add(Moss((750, 1030), (0, 0), 100, 100, "moss"))
        level3.blocks.add(Moss((850, 1030), (0, 0), 100, 100, "moss"))
        level3.blocks.add(Moss((950, 1030), (0, 0), 100, 100, "moss"))
        level3.blocks.add(Moss((950, 780), (0, 0), 100, 400, "moss"))
        level3.blocks.add(Moss((950, 380), (0, 0), 100, 400, "moss"))
        level3.enemies.add(Sheep((300, 900), (0, 0), 100, 100, "sheep"))

        self.levels = [level1, level2, level3, level4]

    def get_level(self, i):
        self.init_levels()
        return self.levels[i%4]


class Level:

    def __init__(self):
        self.enemies = copy.copy(pygame.sprite.Group())
        self.blocks = copy.copy(pygame.sprite.Group())

    def get_enemies(self):
        return self.enemies

    def get_blocks(self):
        return self.blocks
