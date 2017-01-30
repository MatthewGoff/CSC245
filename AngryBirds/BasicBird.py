# An angry bird for the angry birds game
# Author: Matthew  Goff, Nik Lockwood
# Winter 2017
# Personal access token for Nik's computer
# 931d9542e4215563c5cc1532840f4cf36ff23e37

import pygame
from bird import Bird
import GameEngine.util
import pyganim

class BasicBird(Bird):

    def __init__(self, position, velocity, physics_environment, identifier):
        #self.image = pygame.image.load("images/Bird attacks sprite sheets/Transparent PNG/Bird B/frame-1.png")
        self.animate = pyganim.PygAnimation([('images/Bird attacks sprite sheets/Transparent PNG/Bird B/frame-1.png', 0.1),
                                             ('images/Bird attacks sprite sheets/Transparent PNG/Bird B/frame-2.png', 0.1),
                                             ('images/Bird attacks sprite sheets/Transparent PNG/Bird B/frame-3.png', 0.1),
                                             ('images/Bird attacks sprite sheets/Transparent PNG/Bird B/frame-4.png', 0.1),])
        self.animate.smoothscale((110,100))
        self.animate.play()

        Bird.__init__(self,
                      position,
                      velocity,
                      50,
                      0,
                      physics_environment,
                      identifier)

    def update(self, window):
        self.animate.blit(window, (self.position.get_x(), self.position.get_y()))