from math import pi
import util


class GameObject(object):

    def get_id(self):
        return self.identifier

    def __str__(self):
        return "("+str(self.identifier)+")"


class Ball(GameObject):
    def __init__(self, position, velocity, color, radius, identifier):
        self.position = position
        self.velocity = velocity
        self.color = color
        self.radius = radius
        self.identifier = identifier

    def collide(self, next_velocity, partner):
        if util.COLOR_SCHEME == "bounce":
            self.color = util.random_color()
        self.velocity = next_velocity

    def simulate(self):
        acceleration = self.velocity.unit()*(util.DRAG_COEFFICIENT * self.velocity.mag() ** 2)
        if util.DRAG:
            self.velocity += + acceleration
        self.position += self.velocity

    def get_radius(self):
        return self.radius

    def get_position(self):
        return self.position

    def get_velocity(self):
        return self.velocity

    def get_color(self):
        return self.color

    def get_mass(self):
        if util.INVERSE_MASS:
            return 1/(pi*self.get_radius()**2)
        else:
            return pi*self.get_radius()**2


class Paddle(GameObject):
    def __init__(self, position, velocity, height, width, color, identifier):
        self.position = position
        self.velocity = velocity
        self.height = height
        self.width = width
        self.color = color
        self.identifier = identifier
        self.mass = width*height

        self.walls = [Wall((self.position+util.Vec2D(width/2, 0)),
                           velocity,
                           util.Vec2D(1, 0),
                           height,
                           float("inf"),
                           "right",
                           self.notify_collision),
                      Wall(self.position+util.Vec2D(0, -height/2),
                           velocity,
                           util.Vec2D(0, -1),
                           width,
                           self.mass,
                           "top",
                           self.notify_collision),
                      Wall(self.position+util.Vec2D(-width/2, 0),
                           velocity,
                           util.Vec2D(-1, 0),
                           height,
                           float("inf"),
                           "left",
                           self.notify_collision),
                      Wall(self.position+util.Vec2D(0, height/2),
                           velocity,
                           util.Vec2D(0, 1),
                           width,
                           self.mass,
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
        if self.get_top() < 0 or self.get_bottom() > util.WINDOW_HEIGHT:
            self.position -= self.velocity
        else:
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

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def get_color(self):
        return self.color

    def notify_collision(self, wall, other):
        self.velocity = wall.get_velocity()

    def get_walls(self):
        return self.walls


class Wall(GameObject):
    def __init__(self, position, velocity, normal, width, mass, identifier, listener):
        self.position = position
        self.velocity = velocity
        self.normal = normal
        self.width = width
        self.mass = mass
        self.identifier = identifier
        self.listeners = [listener]

    def add_listeners(self, listener):
        self.listeners += [listener]

    def collide(self, velocity, partner):
        self.velocity = velocity
        for listener in self.listeners:
            listener(self, partner)

    def set_velocity(self, velocity):
        self.velocity = velocity

    def simulate(self):
        self.position += self.velocity

    def get_position(self):
        return self.position

    def get_velocity(self):
        return self.velocity

    def get_norm(self):
        return self.normal

    def get_tang(self):
        return self.normal.perp()

    def get_width(self):
        return self.width

    def get_mass(self):
        if self.velocity.is_zero():
            return float("inf")
        else:
            return self.mass

    def get_radius(self):
        return self.width
