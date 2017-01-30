# A simple Gorillas game
# Author: Matthew Anderson
# Winter 2017

import pygame, math
from building import Building
from gorilla import Gorilla
from banana import Banana

class Gorillas(object):

    width = 640
    height = 480
    my_win = pygame.display.set_mode((width, height))
    buildings = pygame.sprite.Group()
    players = pygame.sprite.Group()
    bananas = pygame.sprite.Group()
    t = 0
    dangle = 0
    dpower = 0
    firing = False
    winner = None

    @classmethod
    def init(cls):
        pygame.init()
        cls.buildings.add(Building(-100, 0, 100, cls.height, 1, 1))
        cls.buildings.add(Building(0, 280, 100, 200, 5, 5))
        cls.buildings.add(Building(100, 380, 200, 100, 5, 3))
        cls.buildings.add(Building(300, 330, 150, 150, 10, 10))
        cls.buildings.add(Building(450, 200, 190, 280, 10, 8))
        cls.buildings.add(Building(cls.width, 0, cls.width+100, cls.height, 1, 1))
        cls.player1 = Gorilla(50,50)
        cls.player1.set_vel(10,10)
        cls.player2 = Gorilla(cls.width-50-50,50)
        cls.players.add(cls.player1)
        cls.players.add(cls.player2)
        cls.curr_player = cls.player1


    @classmethod
    def handle_events(cls):

        keep_going = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keep_going = False

            elif cls.winner != None:
                cls.dangle = 0
                cls.dpower = 0

            elif event.type == pygame.KEYDOWN:
                # Key pressed event
                key_pressed = chr(event.dict['key'] % 256)
                # print "Key pressed = %s" % key_pressed

                if key_pressed == "a":
                    cls.dangle = -0.5
                elif key_pressed == "d":
                    cls.dangle = 0.5
                elif key_pressed == "w":
                    cls.dpower = 0.1
                elif key_pressed == "s":
                    cls.dpower = -0.1
                elif key_pressed == " ":
                    cls.firing = True

            elif event.type == pygame.KEYUP:

                # Key released event
                key_released = chr(event.dict['key'] % 256)
                #print "Key released = %s" % key_released

                if key_released == "a" or key_released == "d":
                    cls.dangle = 0
                if key_released == "s" or key_released == "w":
                    cls.dpower = 0

            elif event.type == pygame.MOUSEBUTTONDOWN:

                #print "Button pressed:", event.dict['button'], "@", event.dict['pos']
                button_pressed = event.dict['button']
                target = event.dict['pos']
                if button_pressed == 1: # Left click targets
                    cls.curr_player.aim_at(target[0],target[1])
                elif button_pressed == 3: # Right click fires
                    cls.firing = True



            elif event.type == pygame.MOUSEBUTTONUP:

                #print "Button released:", event.dict['button'], "@", event.dict['pos']
                button_pressed = event.dict['button']
                target = event.dict['pos']


        return keep_going

    @classmethod
    def apply_rules(cls):

        if cls.winner == None and cls.player1.lives <= 0:
            cls.winner = cls.player2
        if cls.winner == None and cls.player2.lives <= 0:
            cls.winner = cls.player1

        if cls.firing:
            b = Banana(cls.curr_player.pos.x, cls.curr_player.pos.y, cls.curr_player)
            b.set_vel(cls.curr_player.power * math.cos(math.radians(cls.curr_player.angle)), cls.curr_player.power * math.sin(math.radians(cls.curr_player.angle)))
            cls.bananas.add(b)
            cls.firing = False
            cls.curr_player = cls.player2 if cls.curr_player == cls.player1 else cls.player1


        for banana in cls.bananas.sprites():
            hit = banana.collide(cls.players.sprites())
            hit = hit or banana.collide(cls.buildings.sprites())
            if hit:
                cls.bananas.remove(banana)
        for player in cls.players.sprites():
            player.collide(cls.buildings.sprites())


    @classmethod
    def simulate(cls,dt):
        cls.curr_player.update_aim(cls.dangle, cls.dpower)
        for player in cls.players.sprites():
            player.simulate(dt)
        for banana in cls.bananas.sprites():
            banana.simulate(dt)


    @classmethod
    def draw(cls):
        # Draw Background
        cls.my_win.fill(pygame.color.Color("LightBlue"))

        cls.buildings.draw(cls.my_win)
        # Old drawing code
        #for building in cls.buildings:
        #    building.draw(cls.my_win)
        cls.players.draw(cls.my_win)
        cls.bananas.draw(cls.my_win)


        font = pygame.font.SysFont("monospace", 50)
        score_left_display = font.render("%d" % cls.player1.lives, 0, (0, 0, 0))
        score_right_display = font.render("%d" % cls.player2.lives, 0, (0, 0, 0))
        cls.my_win.blit(score_left_display, (20, 20))
        cls.my_win.blit(score_right_display, (cls.width - 20 - 50, 20))

        cls.curr_player.draw_aim(cls.my_win)

        if cls.winner == cls.player1:
                win_display = font.render("Player 1 Wins!", 0, (0, 0, 0))
                cls.my_win.blit(win_display, (100, 175))
        if cls.winner == cls.player2:
                win_display = font.render("Player 2 Wins!", 0, (0, 0, 0))
                cls.my_win.blit(win_display, (100, 175))

        # Swap display
        pygame.display.update()

    @classmethod
    def quit(cls):
        pygame.quit()

    @classmethod
    def run(cls):

        frame_rate = 240
        tick_time = int(1.0 / frame_rate * 1000)

        # The game loop starts here.
        keep_going = True
        while keep_going:

            pygame.time.wait(tick_time)

            # 1. Handle events.
            keep_going = cls.handle_events()

            # 2. Apply rules of game world
            cls.apply_rules()

            # 3. Simulate the world
            cls.simulate(0.1)

            # 4. Draw frame
            cls.draw()

        cls.quit()



Gorillas.init()
Gorillas.run()
