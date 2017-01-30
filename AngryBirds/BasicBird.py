# An angry bird for the angry birds game
# Author: Matthew  Goff, Nik Lockwood
# Winter 2017

import pygame
from bird import Bird
import GameEngine.util
import pyganim

class BasicBird(Bird):

    def __init__(self, position, velocity, radius, mass, physics_environment, identifier):
        self.image = pygame.image.load("images/Bird attacks sprite sheets/Transparent PNG/Bird B/frame-1.png")
        self.animate = pyganim.PygAnimation([('images/Bird attacks sprite sheets/Gif previews/Bird-B.gif', 0.1)])
        self.animate.play()

        Bird.__init__(self,
                      position,
                      velocity,
                      radius,
                      mass,
                      physics_environment,
                      self.image,
                      identifier)
    def update(self, window):
        self.animate.blit(window, (self.position.x, self.position.y))