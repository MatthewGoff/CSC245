# An Minesweeper game
# Author: Matthew  Goff
# Winter 2017

import pygame
from GameEngine import util
from square import Square

class Minesweeper:
    WINDOW_COLOR = pygame.Color("grey")
    WIDTH = 10
    HEIGHT = 10

    MARGIN = 10
    SQUARE_SIZE = 16

    def __init__(self):
        print "Seed = " + str(util.get_seed())
        pygame.init()
        self.window_width = (Minesweeper.SQUARE_SIZE*Minesweeper.WIDTH
                             + 2*Minesweeper.MARGIN)
        self.window_height = (Minesweeper.SQUARE_SIZE*Minesweeper.HEIGHT
                              + 2*Minesweeper.MARGIN)
        self.window = pygame.display.set_mode((self.window_width,
                                               self.window_height))

        self.squares = pygame.sprite.Group()
        square = Square((20, 20), 16, 16)
        self.running = False

    def run_game(self):
        self.running = True
        while self.running:
            self.tick()
        pygame.quit()

    def tick(self):
        self.handle_events()
        self.apply_rules()
        self.update_display()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                pass

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pass

            elif event.type == pygame.MOUSEBUTTONUP:

                button_pressed = event.dict['button']
                target = event.dict['pos']

                if button_pressed == 1: # Left click targets
                    mouse_end = util.Vec2D(target[0], target[1])

                elif button_pressed == 3: # Right click fires
                    pass

    def apply_rules(self):
        pass

    def update_display(self):
        self.window.fill(Minesweeper.WINDOW_COLOR)
        self.squares.draw(self.window)
        pygame.display.update()


minesweeper = Minesweeper()
minesweeper.run_game()