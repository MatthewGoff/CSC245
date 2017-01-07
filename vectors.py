

class Vec_2D:

    def __init__(self, x, y):
        self.vec = (x, y)

    def add(self, other):
        return Vec_2D(self.get_x() + other.get_x(), self.get_y() + other.get_y())

    def sub(self, other):
        return Vec_2D(self.get_x() - other.get_x(), self.get_y() - other.get_y())

    def mult(self, scalar):
        return Vec_2D(self.get_x()*scalar, self.get_y()*scalar)

    def get_x(self):
        return self.vec[0]

    def get_y(self):
        return self.vec[1]

    def mag(self):
        return (self.get_x()**2+self.get_y()**2)**(.5)

    def unit(self):
        return self.mult(1.0/self.mag())

    def __str__(self):
        return "<"+str(self.get_x())+","+str(self.get_y())+">"