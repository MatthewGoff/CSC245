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
        self.generate_ground(level1)
        for i in range(2, 8):
            level1.blocks.add(Crate((1200, self.window_height - 102*i), (0, 0), 100, 100, "crate"))
        level1.blocks.add(Stone((1500, self.window_height - 310), (0, 0), 200, 200, "stone"))
        level1.enemies.add(Sheep((1500, self.window_height - 400), (0, 0), 100, 100, "sheep"))

        level2 = Level()
        self.generate_ground(level2)
        level2.blocks.add(Crate((1200, self.window_height - 200), (0, 0), 100, 100, "crate"))
        level2.blocks.add(Stone((1300, self.window_height - 200), (0, 0), 100, 100, "stone"))
        level2.blocks.add(Ice((1400, self.window_height - 200), (0, 0), 100, 100, "Ice"))
        level2.enemies.add(Sheep((1500, self.window_height - 200), (0, 0), 100, 100, "sheep"))
        level2.enemies.add(Sheep((1000, self.window_height - 200), (0, 0), 100, 100, "sheep"))

        level3 = Level()
        self.generate_ground(level3)
        level3.enemies.add(Ice((400, 900), (0, 0), 100, 100, "Ice"))
        level3.enemies.add(Sheep((300, 900), (0, 0), 100, 100, "sheep"))

        self.levels = [level1, level2, level3]

    def generate_ground(self, level):
        for i in range(0, 20):
            level.blocks.add(Moss((25+i*100, self.window_height-100), (0, 0), 100, 100, "moss"))
        for i in range(2, 11):
            level.blocks.add(Moss((self.window_width - 75, self.window_height - 100*i), (0, 0), 100, 100, "moss"))

        level.blocks.add(Moss((225, self.window_height - 200), (0, 0), 100, 100, "moss"))


    def get_level(self, i):
        self.init_levels()
        return self.levels[i%3]


class Level:

    def __init__(self):
        self.enemies = copy.copy(pygame.sprite.Group())
        self.blocks = copy.copy(pygame.sprite.Group())

    def get_enemies(self):
        return self.enemies

    def get_blocks(self):
        return self.blocks
