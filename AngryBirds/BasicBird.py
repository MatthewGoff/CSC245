# An angry bird for the angry birds game
# Author: Matthew  Goff, Nik Lockwood
# Winter 2017

import pygame
from bird import Bird
import GameEngine.util
import pyganim

class BasicBird(Bird):

    def __init__(self, position, velocity, radius, mass, physics_environment, identifier):
        self.image_str = "images/Bird attacks sprite sheets/Transparent PNG/Bird B/frame-1.png"
        Bird.__init__(self,
                      position,
                      velocity,
                      radius,
                      mass,
                      physics_environment,
                      self.image_str,
                      identifier)
