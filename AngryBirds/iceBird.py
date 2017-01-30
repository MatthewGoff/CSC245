# An angry bird for the angry birds game
# Author: Matthew  Goff, Nik Lockwood
# Winter 2017

import pygame
from bird import Bird
import GameEngine.util
import pyganim

class iceBird(Bird):
    MASS = 2
    RADIUS = 50

    def __init__(self, position, velocity, identifier):
        #self.image = pygame.image.load("images/Bird attacks sprite sheets/Transparent PNG/Bird B/frame-1.png")
        self.animate = pyganim.PygAnimation([('images/Bird attacks sprite sheets/Transparent PNG/Bird C/frame-1.png', 0.1),
                                             ('images/Bird attacks sprite sheets/Transparent PNG/Bird C/frame-2.png', 0.1),
                                             ('images/Bird attacks sprite sheets/Transparent PNG/Bird C/frame-3.png', 0.1),
                                             ('images/Bird attacks sprite sheets/Transparent PNG/Bird C/frame-4.png', 0.1),])
        self.animate.smoothscale((110,100))
        self.animate.play()

        Bird.__init__(self,
                      position,
                      velocity,
                      iceBird.RADIUS,
                      iceBird.MASS,
                      identifier)


    def update(self, window):
        self.animate.blit(window, (self.position.x, self.position.y))
