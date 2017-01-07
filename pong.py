# A simple pong game
# Author: Matthew Anderson, Kristina Striegnitz, John Rieffel
# Winter 2017

import pygame
import random

width = 1000
height = 1000
colors = []
speed_limit = 5

class ball:
    x_pos = 0
    y_pos = 0
    x_speed = 1
    y_speed = 1
    x_acc = -0.1;
    y_acc = -0.1;


    radius = 10
    color = pygame.color.Color(225,0,0)

    def __init__(self, x_pos_param, y_pos_param, x_speed_param, y_speed_param, r,g,b):
        self.x_pos=x_pos_param
        self.y_pos=y_pos_param
        self.x_speed = x_speed_param
        self.y_speed = y_speed_param
        self.color = pygame.color.Color(r, g, b)

    def tick(self):
        self.x_pos += self.x_speed
        self.y_pos += self.y_speed

        if (self.x_pos <= 0+(self.radius)) or (self.x_pos >= width-(self.radius)):
            self.x_speed = -1*self.x_speed
            self.bounce()

        if (self.y_pos <= 0+(self.radius)) or (self.y_pos >= height-(self.radius)):
            self.y_speed = -1*self.y_speed
            self.bounce()

    def bounce(self):
        self.color = pygame.color.Color(random.randint(0,255),random.randint(0,255),random.randint(0,255))

    def get_radius(self):
        return self.radius

    def get_pos(self):
        return (self.x_pos,self.y_pos)

    def get_color(self):
        return self.color

def run_game():

    # Initialize pygame and set up the display window.
    pygame.init()

    my_win = pygame.display.set_mode((width, height))

    # Initialize balls
    my_balls = []
    for i in range(0, random.randint(0,10000)):
        my_balls += [ball(random.randint(0,width),
                          random.randint(0,height),
                          random.randint(-speed_limit,speed_limit),
                          random.randint(-speed_limit,speed_limit),
                          random.randint(0,255), random.randint(0,255), random.randint(0,255))]


    # The game loop starts here.
    keep_going = True
    while (keep_going):

        # 1. Handle events.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keep_going = False


        # 2. Apply rules of game world
        for i in range(0,len(my_balls)):
            my_balls[i].tick()

        # 3. Simulate the world
        # None currently

        # 4. Draw frame
        # Draw Background
        my_win.fill(pygame.color.Color("black"))

        # Draw ball
        for i in range(0,len(my_balls)):
            pygame.draw.circle(my_win, my_balls[i].get_color(), my_balls[i].get_pos(), my_balls[i].get_radius())

        # Swap display
        pygame.display.update()

    # The game loop ends here.

    pygame.quit()


# Start game
run_game()