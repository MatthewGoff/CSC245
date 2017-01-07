# A simple pong game
# Author: Matthew Anderson, Kristina Striegnitz, John Rieffel
# Winter 2017

import pygame
import random
from vectors import Vec_2D

width = 640
height = 480
num_balls = 100

speed_limit = 0.5
size_limit = 10

class Ball:

    def __init__(self, position=None, velocity=None, rgb=None, radius=None):
        if radius is None:
            self.radius = size_limit
        else:
            self.radius = radius

        if position is None:
            self.position = Vec_2D(random.uniform(0+self.radius, width-self.radius),
                                   random.uniform(0+self.radius, height-self.radius))
        else:
            self.position = position

        if velocity is None:
            self.velocity = Vec_2D(random.uniform(-speed_limit, speed_limit),
                                   random.uniform(-speed_limit, speed_limit))
        else:
            self.velocity = velocity

        if rgb is None:
            self.color = pygame.color.Color(random.randint(0, 255),
                                            random.randint(0, 255),
                                            random.randint(0, 255))
        else:
            self.color = pygame.color.Color(rgb[0],rgb[1],rgb[2])

        self.next_position = self.position
        self.next_velocity = self.velocity
        self.next_color = self.color

    def update(self, balls):

        self.next_velocity = self.velocity

        collision = False
        if self.get_x() <= 0+self.radius:
            collision_vec = Vec_2D(-1,0)
            if collision_vec.dot(self.velocity) > 0:
                self.next_velocity = self.next_velocity.add(Vec_2D(-2*self.velocity.get_x(), 0))
                collision = True
        elif self.get_x() >= width-self.radius:
            collision_vec = Vec_2D(1, 0)
            if collision_vec.dot(self.velocity) > 0:
                self.next_velocity = self.next_velocity.add(Vec_2D(-2 * self.velocity.get_x(), 0))
                collision = True
        if self.get_y() <= 0+self.radius:
            collision_vec = Vec_2D(0, -1)
            if collision_vec.dot(self.velocity) > 0:
                self.next_velocity = self.next_velocity.add(Vec_2D(0, -2*self.velocity.get_y()))
                collision = True
        elif self.get_y() >= height-self.radius:
            collision_vec = Vec_2D(0, 1)
            if collision_vec.dot(self.velocity) > 0:
                self.next_velocity = self.next_velocity.add(Vec_2D(0, -2 * self.velocity.get_y()))
                collision = True

        self.next_position = self.position.add(self.next_velocity)

        if collision:
            self.next_color = pygame.color.Color(random.randint(0,255),random.randint(0,255),random.randint(0,255))
        else:
            self.next_color = self.color

    def simulate(self):
        self.velocity = self.next_velocity
        self.position = self.next_position
        self.color = self.next_color

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
        for ball in my_balls:
            ball.update(my_balls)

        # 3. Simulate the world
        for ball in my_balls:
            ball.simulate()

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