import math


class Vec_2D:

    def __init__(self, x, y):
        self.vec = (x, y)

    def add(self, other):
        return Vec_2D(self.get_x() + other.get_x(), self.get_y() + other.get_y())

    def sub(self, other):
        return Vec_2D(self.get_x() - other.get_x(), self.get_y() - other.get_y())

    def scale(self, scalar):
        return Vec_2D(self.get_x()*scalar, self.get_y()*scalar)

    def dot(self, other):
        return self.get_x()*other.get_x()+self.get_y()*other.get_y()

    def get_x(self):
        return self.vec[0]

    def get_y(self):
        return self.vec[1]

    def mag(self):
        return (self.get_x()**2+self.get_y()**2)**.5

    def angle(self):
        #Not working!
        print "calculating angle"
        print "x = "+str(self.get_x())
        print "y = "+str(self.get_y())

        angle = 0
        if self.get_x() == 0:
            if self.get_y() > 0:
                angle = math.pi/2
            else:
                angle = -1*math.pi/2
        elif self.get_x() < 0:
            print "need to revers"
            print "atan = "+str(math.atan(self.get_y()/self.get_x()))
            angle = math.atan(self.get_y()/self.get_x())+(math.pi)
        else:
            angle = math.atan(self.get_y()/self.get_x())

        print "returning "+str(angle)
        return angle

    def unit(self):
        return self.scale(1.0/self.mag())

    def perp(self):
        return Vec_2D(-1*self.get_y(),self.get_x())

    def __str__(self):
        return "<"+str(self.get_x())+","+str(self.get_y())+">"