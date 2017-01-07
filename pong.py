# A simple pong game
# Author: Matthew Anderson, Kristina Striegnitz, John Rieffel
# Winter 2017

import pygame
import random
from vectors import Vec_2D

width = 640
height = 480
num_balls = 100

speed_limit = 0.1
size_limit = 10

viscocity = 2
bounce = 0.01

advanced_physics = False;

class Ball:

    def __init__(self, position = None, velocity = None, rgb = None, radius = None):
        if radius == None:
            self.radius = size_limit
        else:
            self.radius = radius

        if position == None:
            self.position = Vec_2D(random.uniform(0+self.radius, width-self.radius),
                                    random.uniform(0+self.radius, height-self.radius))
        else:
            self.position = position

        if velocity == None:
            self.velocity = Vec_2D(random.uniform(-speed_limit, speed_limit),
                                    random.uniform(-speed_limit, speed_limit))
        else:
            self.velocity = velocity

        if rgb == None:
            self.color = pygame.color.Color(random.randint(0, 255),
                                            random.randint(0, 255),
                                            random.randint(0, 255))
        else:
            self.color = pygame.color.Color(rgb[0],rgb[1],rgb[2])


    def tick(self):
        acceleration = Vec_2D(0,0)

        if self.get_x() <= 0+self.radius:
            self.bounce()
            acceleration.add(Vec_2D(-2*self.velocity.get_x(), 0))
        elif self.get_x() >= width-self.radius:
            self.bounce()
            acceleration.add(Vec_2D(-2*self.velocity.get_x(), 0))

        if self.get_y() <= 0+self.radius:
            self.bounce()
            acceleration.add(Vec_2D(0, -2*self.velocity.get_y()))
        elif self.get_y() >= height-self.radius:
            self.bounce()
            acceleration.add(Vec_2D(0, -2*self.velocity.get_y()))

        self.velocity.add(acceleration)
        self.position.add(self.velocity)


    def bounce(self):
        self.color = pygame.color.Color(random.randint(0,255),random.randint(0,255),random.randint(0,255))

    def get_radius(self):
        return self.radius

    def get_pos(self):
        return (self.get_x(),self.get_y())

    def get_x(self):
        return self.position.get_x()

    def get_y(self):
        return self.position.get_y()

    def get_color(self):
        return self.color

def run_game():

    # Initialize pygame and set up the display window.
    pygame.init()

    my_win = pygame.display.set_mode((width, height))

    # Initialize balls
    my_balls = []
    for i in range(0, num_balls):
        my_balls += [Ball()]


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
        for ball in my_balls:
            pygame.draw.circle(my_win, ball.get_color(), (int(ball.get_x()),int(ball.get_y())), ball.get_radius())

        # Swap display
        pygame.display.update()

    # The game loop ends here.

    pygame.quit()

# Start game
run_game()