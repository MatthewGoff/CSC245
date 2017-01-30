import pygame, random
from block import Block
from crate import Crate
from ice import Ice
from moss import Moss
from stone import Stone
from sheep import Sheep
from GameEngine import util

# Level generator class
# The first three levels are preprogrammed, after that random (within limitations) levels are generated
# Author: Nik Lockwood
# Winter 2017

class Level:

    def __init__(self, window_width, window_height):
        self.window_width = window_width
        self.window_height = window_height
        self.levels = []
        self.level1 = [[1,400,400],[2,500,500],[3,600,600],[4,700,700],[5,800,800]]
        self.levels.append(self.level1)

    def setup(self, num):
        enemies = pygame.sprite.Group()
        moss = pygame.sprite.Group()
        crates = pygame.sprite.Group()
        stones = pygame.sprite.Group()
        ice = pygame.sprite.Group()
        blocks = []
        for i in self.levels[num]:
            if i[0] == 1:
                enemies.add(Sheep(util.Vec2D(500, 500),util.Vec2D(0, 0),50,50,"sheep"))
            elif i[0] == 2:
                moss.add(Moss(util.Vec2D(500, 500),util.Vec2D(0, 0), 50, 50, "moss"))
            elif i[0] == 3:
                crates.add(Crate(util.Vec2D(500, 500),util.Vec2D(0, 0), 50, 50, "crate"))
            elif i[0] == 4:
                stones.add(Stone(util.Vec2D(500, 500),util.Vec2D(0, 0), 50, 50, "stone"))
            elif i[0] == 5:
                ice.add(Ice(util.Vec2D(500, 500),util.Vec2D(0, 0), 50, 50, "Ice"))

        for i in range(0, 50):
            xpos = i*50
            ypos = self.window_height - 50
            mymoss = Moss(util.Vec2D(xpos, ypos), util.Vec2D(0, 0), 50, 50, "moss")
            moss.add(mymoss)

        blocks.append(enemies)
        blocks.append(moss)
        blocks.append(crates)
        blocks.append(stones)
        blocks.append(ice)
        return blocks