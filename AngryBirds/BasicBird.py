# An angry bird for the angry birds game
# Author: Matthew  Goff, Nik Lockwood
# Winter 2017

import pygame
from bird import Bird
import GameEngine.util

class BasicBird(Bird):

    def __init__(self, position, velocity, radius, mass, identifier):
        self.image_str = "images/basicBird.png"
        Bird.__init__(self, position, velocity, radius, mass, self.image_str, identifier)