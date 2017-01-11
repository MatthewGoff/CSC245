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
        acceleration = self.velocity.unit().scale(util.DRAG_COEFFICIENT * self.velocity.mag() ** 2)
        if util.DRAG:
            self.velocity = self.velocity.add(acceleration)
        self.position = self.position.add(self.velocity)

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
