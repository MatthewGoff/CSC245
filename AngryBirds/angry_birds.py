# An Angry Birds game
# Author: Matthew  Goff, Nik Lockwood
# Winter 2017

import pygame
from GameEngine import game, util
from bird import Bird
from BasicBird import BasicBird
from slingshot import Slingshot


class AngryBirds(game.Game):
    WINDOW_COLOR = pygame.Color("lightblue")

    def __init__(self, window_width, window_height):
        game.Game.__init__(self, window_width, window_height)

        self.balls = []

        self.bird = BasicBird(util.Vec2D(50, 50), util.Vec2D(0, 0), 50, 0, "bird")
        self.slingshot = Slingshot(util.Vec2D(200, 200), 50, "slingshot")

        self.game_objects = pygame.sprite.Group()
        self.game_objects.add(self.bird)
        self.game_objects.add(self.slingshot)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_m:
                self.mute = not self.mute

        keys = pygame.key.get_pressed()

    def update_display(self):
        self.window.fill(AngryBirds.WINDOW_COLOR)
        self.game_objects.draw(self.window)

        pygame.display.update()

angry_birds = AngryBirds(640*2, 480*2)
angry_birds.run_game()