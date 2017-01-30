# An angry bird for the angry birds game
# Author: Matthew  Goff, Nik Lockwood
# Winter 2017

import pygame
from bird import Bird
import GameEngine.util
import pyganim

class BasicBird(Bird):

    def __init__(self, position, velocity, radius, mass, identifier):
        self.image = pygame.image.load("images/Bird attacks sprite sheets/Transparent PNG/Bird B/frame-1.png")
        self.anim = pyganim.PygAnimation([("images/Bird attacks sprite sheets/Gif previews/Bird-B.gif")])
        Bird.__init__(self, position, velocity, radius, mass, self.image, identifier)