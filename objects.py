from math import pi
import util


class Ball:
    def __init__(self, position, velocity, color, radius):
        self.position = position
        self.velocity = velocity
        self.color = color
        self.radius = radius
        self.next_velocity = self.velocity
        self.next_color = self.color

    def collide(self, next_velocity):
        if True:
            self.next_color = util.random_color()
        self.next_velocity = next_velocity

    def simulate(self):
        acceleration = self.next_velocity.unit().scale(util.DRAG_COEFFICIENT*self.next_velocity.mag()**2)
        if util.DRAG:
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
        return self.color

    def get_mass(self):
        if util.INVERSE_MASS:
            return 1/(pi*self.get_radius()**2)
        else:
            return pi*self.get_radius()**2