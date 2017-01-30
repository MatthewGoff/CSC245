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

    def __init__(self):
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
                enemies.add(Sheep(util.Vec2D(500, 500),0,50,50,self.notify_collision,"sheep"))
            elif i[0] == 2:
                moss.add(Moss(util.Vec2D(500, 500), 0, 50, 50, self.notify_collision, "moss"))
            elif i[0] == 3:
                crates.add(Crate(util.Vec2D(500, 500), 0, 50, 50, self.notify_collision, "crate"))
            elif i[0] == 4:
                stones.add(Stone(util.Vec2D(500, 500), 0, 50, 50, self.notify_collision, "stone"))
            elif i[0] == 5:
                ice.add(Ice(util.Vec2D(500, 500), 0, 50, 50, self.notify_collision, "Ice"))

        blocks.append(enemies)
        blocks.append(moss)
        blocks.append(crates)
        blocks.append(stones)
        blocks.append(ice)
        return blocks