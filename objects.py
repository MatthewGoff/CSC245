from math import pi
import util
import pygame


class GameObject(object):

    def __init__(self, identifier):
        self.identifier = identifier

    def get_id(self):
        return self.identifier

    def __str__(self):
        return "("+str(self.identifier)+")"


class Collidable(GameObject):

    def __init__(self, position, velocity, radius, mass, identifier):
        GameObject.__init__(self, identifier)
        self.position = position
        self.velocity = velocity
        self.radius = radius
        self.mass = mass

    def get_position(self):
        return self.position

    def get_velocity(self):
        return self.velocity

    def get_radius(self):
        return self.radius

    def get_mass(self):
        return self.mass


class Ball(Collidable):

    def __init__(self, position, velocity, radius, identifier):
        Collidable.__init__(self, position, velocity, radius, pi*radius**2, identifier)

    def collide(self, next_velocity, partner):
        self.velocity = next_velocity

    def simulate(self):
        acceleration = self.velocity.unit()*(util.DRAG_COEFFICIENT * self.velocity.mag())
        if util.DRAG:
            self.velocity += acceleration
        self.position += self.velocity

    def draw(self, window, draw_velocity):

        pygame.draw.circle(window,
                           self.color,
                           (int(self.position.get_x()), int(self.position.get_y())),
                           self.get_radius())

        if draw_velocity:
            vec = self.position + self.velocity * 50
            pygame.draw.line(window, pygame.Color("white"), self.position.to_tuple(), vec.to_tuple(), 1)


class PongBall(Ball):
    BOUNCE = 0
    RANDOM = 1
    GRADIENT = 2
    SPEED = 3

    def __init__(self, position, velocity, color_scheme, radius, identifier):
        Ball.__init__(self, position, velocity, radius, identifier)
        self.color_scheme = color_scheme
        self.color = util.random_color()

    def collide(self, next_velocity, partner):
        if self.color_scheme == PongBall.BOUNCE:
            self.color = util.random_color()
        self.velocity = next_velocity

    def get_positional_color(self, window):
        r = int(255 * self.position.get_x() / window.get_clip().width) % 256
        g = int(255 * self.position.get_y() / window.get_clip().height) % 256
        b = int(255 * self.radius / 100) % 256

        return pygame.Color(r, g, b)

    def draw(self, window, draw_velocity):

        if self.color_scheme == PongBall.GRADIENT:
            pygame.draw.circle(window,
                               self.get_positional_color(window),
                               (int(self.position.get_x()), int(self.position.get_y())),
                               self.get_radius())

        elif self.color_scheme == PongBall.SPEED:

            s = pygame.Surface((self.radius * 2, self.radius * 2))
            s.fill((0, 0, 0))
            s.set_colorkey((0, 0, 0))
            pygame.draw.circle(s, self.get_positional_color(window), (self.radius, self.radius), self.radius)
            s.set_alpha(int((self.velocity.mag() * 500) % 255))

            window.blit(s, (int(self.position.get_x() - self.radius), int(self.position.get_y() - self.radius)))

        else:
            Ball.draw(self, window, draw_velocity)


class Block(GameObject):
    def __init__(self, position, velocity, height, width, color, identifier):
        GameObject.__init__(self, identifier)
        self.position = position
        self.velocity = velocity
        self.height = height
        self.width = width
        self.color = color
        self.mass = width*height

        self.walls = [Wall((self.position+util.Vec2D(width/2, 0)),
                           velocity,
                           util.Vec2D(1, 0),
                           height,
                           self.mass,
                           self.color,
                           "right",
                           self.notify_collision),
                      Wall(self.position+util.Vec2D(0, -height/2),
                           velocity,
                           util.Vec2D(0, -1),
                           width,
                           self.mass,
                           self.color,
                           "top",
                           self.notify_collision),
                      Wall(self.position+util.Vec2D(-width/2, 0),
                           velocity,
                           util.Vec2D(-1, 0),
                           height,
                           self.mass,
                           self.color,
                           "left",
                           self.notify_collision),
                      Wall(self.position+util.Vec2D(0, height/2),
                           velocity,
                           util.Vec2D(0, 1),
                           width,
                           self.mass,
                           self.color,
                           "bottom",
                           self.notify_collision)]

    def get_position(self):
        return self.position

    def get_velocity(self):
        return self.velocity

    def set_velocity(self, velocity):
        self.velocity = velocity
        for wall in self.walls:
            wall.set_velocity(velocity)

    def simulate(self):
        self.position += self.velocity
        for wall in self.walls:
                wall.simulate()

    def get_top(self):
        return self.position.get_y()-int(self.height/2)

    def get_bottom(self):
        return self.position.get_y()+int(self.height/2)

    def get_left(self):
        return self.position.get_x()-int(self.width/2)

    def get_right(self):
        return self.position.get_x()+int(self.width/2)

    def get_right_wall(self):
        return self.walls[0]

    def get_top_wall(self):
        return self.walls[1]

    def get_left_wall(self):
        return self.walls[2]

    def get_bottom_wall(self):
        return self.walls[3]

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def get_color(self):
        return self.color

    def notify_collision(self, wall, other):
        self.velocity = wall.get_velocity()
        for wall in self.walls:
            wall.set_velocity(self.velocity)

    def get_walls(self):
        return self.walls

    def draw(self, window):
        pygame.draw.rect(window,
                         self.get_color(),
                         pygame.Rect(self.get_left(),
                                     self.get_top(),
                                     self.get_width(),
                                     self.get_height()),
                         0)


class VerticalPaddle(Block):

    def __init__(self, position, velocity, height, width, bounds, color, identifier):
        Block.__init__(self, position, velocity, height, width, color, identifier)
        self.bounds = bounds
        self.get_right_wall().make_dense()
        self.get_left_wall().make_dense()

    def simulate(self):
        self.position += self.velocity
        if self.get_top() < self.bounds.get_top() or self.get_bottom() > self.bounds.get_bottom():
            self.position -= self.velocity
        else:
            for wall in self.walls:
                wall.simulate()


class HorizontalPaddle(Block):

    def __init__(self, position, velocity, height, width, bounds, color, identifier):
        Block.__init__(self, position, velocity, height, width, color, identifier)
        self.bounds = bounds
        self.get_top_wall().make_dense()
        self.get_bottom_wall().make_dense()

    def simulate(self):
        self.position += self.velocity
        if self.get_left() < self.bounds.get_left() or self.get_right() > self.bounds.get_right():
            self.position -= self.velocity
        else:
            for wall in self.walls:
                wall.simulate()


class Wall(Collidable):
    def __init__(self, position, velocity, normal, width, mass, color, identifier, listener):
        Collidable.__init__(self, position, velocity, width/2, mass, identifier)
        self.normal = normal
        self.color = color
        self.listener = listener

    def make_dense(self):
        self.mass = float("inf")

    def collide(self, velocity, partner):
        self.velocity = velocity
        self.listener(self, partner)

    def set_velocity(self, velocity):
        self.velocity = velocity

    def simulate(self):
        self.position += self.velocity

    def get_norm(self):
        return self.normal

    def get_tang(self):
        return self.normal.perp()

    def draw(self, window):
        leg = self.normal.perp()*self.radius
        pygame.draw.line(window, self.color, self.position - leg, self.position + leg, 1)
