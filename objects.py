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

    def get_position(self):
        return self.position

    def get_velocity(self):
        return self.velocity

    def set_velocity(self, velocity):
        self.velocity = velocity

    def simulate(self):
        self.position = self.position + self.velocity

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
