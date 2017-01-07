

class Vec_2D:

    def __init__(self, x_param, y_param):
        self.x = x_param
        self.y = y_param

    def add(self, other):
        self.x = self.get_x() + other.get_x()
        self.y = self.get_y() + other.get_y()

    def mult(self, scalar):
        self.x = self.get_x() * scalar
        self.y = self.get_y() * scalar

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def __str__(self):
        return "<"+str(self.x)+","+str(self.y)+">"