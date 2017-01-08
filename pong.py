import pygame
import random
from math import pi
from vectors import Vec_2D
import sys

seed = random.randint(0, sys.maxint)
print "seed = "+str(seed)
myRand = random.Random(seed)

# Window Parameters
width = 640*2
height = 480*2

# Ball parameters
num_balls = 50
initial_speed = 1           # pixels per "tick"
radius_range = (10, 80)    # in pixels

# Physics parameters
drag = False
drag_delay = 1000           # ticks to wait until drag starts
drag_coefficient = -0.0001  # Try making it positive ;)
inverse_mass = False

# Display parameters
color_scheme = "random"     # bounce, random, gradient, speed
draw_velocity = False

class Ball:
    def __init__(self, position=None, velocity=None, rgb=None, radius=None):
        if radius is None:
            self.radius = myRand.randint(radius_range[0], radius_range[1])
        else:
            self.radius = radius

        if position is None:
            self.position = Vec_2D(myRand.uniform(0 + self.radius, width - self.radius),
                                   myRand.uniform(0 + self.radius, height - self.radius))
        else:
            self.position = position

        if velocity is None:
            self.velocity = Vec_2D(myRand.uniform(-initial_speed, initial_speed),
                                   myRand.uniform(-initial_speed, initial_speed))
        else:
            self.velocity = velocity

        if rgb is None:
            self.color = pygame.color.Color(myRand.randint(0, 255),
                                            myRand.randint(0, 255),
                                            myRand.randint(0, 255),
                                            1)
        else:
            self.color = pygame.color.Color(rgb[0], rgb[1], rgb[2], 1)

        self.next_velocity = self.velocity
        self.next_color = self.color

    def collide(self, next_velocity):
        if color_scheme == "bounce":
            self.next_color = pygame.color.Color(myRand.randint(0, 255), myRand.randint(0, 255), myRand.randint(0, 255), 1)
        else:
            self.next_color = self.color
        self.next_velocity = next_velocity

    def simulate(self):
        acceleration = self.next_velocity.unit().scale(drag_coefficient*self.next_velocity.mag()**2)
        if drag:
            self.next_velocity = self.next_velocity.add(acceleration)
        self.velocity = self.next_velocity
        self.position = self.position.add(self.velocity)
        self.color = self.next_color

    def get_radius(self):
        return self.radius

    def get_position(self):
        return self.position

    def get_velocity(self):
        return self.velocity

    def get_next_velocity(self):
        return self.next_velocity

    def get_color(self):
        if color_scheme == "gradient" or color_scheme == "speed":
            if color_scheme == "speed":
                r = int((self.get_next_velocity().mag()*50)%255)
                g = r
                b = g
            else:
                r = int(255 * self.get_position().get_x() / width)
                g = int(255 * self.get_position().get_y() / height)
                b = int(255*self.get_radius()/radius_range[1])

            r = min(max(0, r), 255)     # encase it shoots over
            g = min(max(0, g), 255)
            b = min(max(0, b), 255)

            return pygame.color.Color(r, g, b, 1)
        else:
            return self.color

    def get_mass(self):
        if inverse_mass:
            return 1/(pi*self.get_radius()**2)
        else:
            return pi*self.get_radius()**2


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
    while keep_going:
        if drag_delay == 0:
            global drag
            drag = True
        elif drag_delay > 0:
            global drag_delay
            drag_delay -= 1

        # 1. Handle events.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keep_going = False

        # 2. Apply rules of game world
        for i in range(0,len(my_balls)):
            collide_walls(my_balls[i])
            for j in range(i+1,len(my_balls)):
                test_collision(my_balls[i], my_balls[j])

        # 3. Simulate the world
        for ball in my_balls:
            ball.simulate()

        # 4. Draw
        my_win.fill(pygame.color.Color("black"))

        for ball in my_balls:
            pos = ball.get_position()
            vel = ball.get_velocity().scale(50)
            pygame.draw.circle(my_win, ball.get_color(), (int(ball.get_position().get_x()), int(ball.get_position().get_y())), ball.get_radius())
            if draw_velocity:
                vec = pos.add(vel)
                pygame.draw.line(my_win, pygame.color.Color("white"), (pos.get_x(), pos.get_y()), (vec.get_x(),vec.get_y()), 3)

        # Swap display
        pygame.display.update()

    # The game loop ends here.

    pygame.quit()


def test_collision(ball1, ball2):
    # see if these two balls have collided and if so calc result

    normal = ball2.get_position().sub(ball1.get_position())  # towards ball2

    if normal.mag() < (ball1.get_radius() + ball2.get_radius()) and\
            (normal.dot(ball1.get_next_velocity()) > 0 or normal.dot(ball2.get_next_velocity()) < 0):

        m1 = ball1.get_mass()
        m2 = ball2.get_mass()
        v1 = ball1.get_next_velocity()
        v2 = ball2.get_next_velocity()

        unit_norm = normal.unit()
        unit_tang = unit_norm.perp()

        v1norm_mag = v1.dot(unit_norm)
        v1tang_mag = v1.dot(unit_tang)
        v2norm_mag = v2.dot(unit_norm)
        v2tang_mag = v2.dot(unit_tang)

        v1norm_mag_f = (v1norm_mag * (m1 - m2) + 2 * m2 * v2norm_mag) / (m1 + m2)
        v1tang_mag_f = v1tang_mag
        v2norm_mag_f = (v2norm_mag * (m2 - m1) + 2 * m1 * v1norm_mag) / (m1 + m2)
        v2tang_mag_f = v2tang_mag

        v1norm = unit_norm.scale(v1norm_mag_f)
        v1tang = unit_tang.scale(v1tang_mag_f)
        v2norm = unit_norm.scale(v2norm_mag_f)
        v2tang = unit_tang.scale(v2tang_mag_f)

        ball1.collide(v1norm.add(v1tang))
        ball2.collide(v2norm.add(v2tang))


def collide_walls(ball1):
    # see if the ball has collided with any walls and if so calc result
    if ball1.get_position().get_x() <= 0 + ball1.get_radius():
        collision_vec = Vec_2D(-1, 0)
        if collision_vec.dot(ball1.get_next_velocity()) > 0:
            ball1.collide(ball1.get_next_velocity().add(Vec_2D(-2 * ball1.get_next_velocity().get_x(), 0)))
    elif ball1.get_position().get_x() >= width - ball1.get_radius():
        collision_vec = Vec_2D(1, 0)
        if collision_vec.dot(ball1.get_next_velocity()) > 0:
            ball1.collide(ball1.get_next_velocity().add(Vec_2D(-2 * ball1.get_next_velocity().get_x(), 0)))
    if ball1.get_position().get_y() <= 0 + ball1.get_radius():
        collision_vec = Vec_2D(0, -1)
        if collision_vec.dot(ball1.get_next_velocity()) > 0:
            ball1.collide(ball1.get_next_velocity().add(Vec_2D(0, -2 * ball1.get_next_velocity().get_y())))
    elif ball1.get_position().get_y() >= height - ball1.get_radius():
        collision_vec = Vec_2D(0, 1)
        if collision_vec.dot(ball1.get_next_velocity()) > 0:
            ball1.collide(ball1.get_next_velocity().add(Vec_2D(0, -2 * ball1.get_next_velocity().get_y())))

# Start game
run_game()
