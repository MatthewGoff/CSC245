# An Angry Birds game
# Author: Matthew  Goff, Nik Lockwood
# Winter 2017

import pygame
from GameEngine import game, util


class AngryBirds(game.Game):

    def __init__(self, window_width, window_height):
        game.Game.__init__(self, window_width, window_height)

        self.balls = []

angry_birds = AngryBirds(640*2, 480*2)
angry_birds.run_game()