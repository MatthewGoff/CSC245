from math import pi
import util


class Ball:
    def __init__(self, position, velocity, color, radius, name):
        self.position = position
        self.velocity = velocity
        self.color = color
        self.radius = radius
        self.name = name

    def collide(self, next_velocity):
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

    def __str__(self):
        return "("+str(self.name)+")"


class Paddle:
    def __init__(self, position, velocity, height, width, color):
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
                           float("inf"),
                           self.notify_collision),
                      Wall(self.position+util.Vec2D(0, -height/2),
                           velocity,
                           util.Vec2D(0, -1),
                           width,
                           self.mass,
                           self.notify_collision),
                      Wall(self.position+util.Vec2D(-width/2, 0),
                           velocity,
                           util.Vec2D(-1, 0),
                           height,
                           float("inf"),
                           self.notify_collision),
                      Wall(self.position+util.Vec2D(0, height/2),
                           velocity,
                           util.Vec2D(0, 1),
                           width,
                           self.mass,
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

    def notify_collision(self):
        print "collision on paddle"

    def get_walls(self):
        return self.walls



class Wall:
    def __init__(self, position, velocity, normal, width, mass, listener):
        self.position = position
        self.velocity = velocity
        self.normal = normal
        self.width = width
        self.mass = mass
        self.listeners = [listener]

    def add_listeners(self, listener):
        self.listeners += [listener]

    def collide(self):
        for listener in self.listeners:
            listener()

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
