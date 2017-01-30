# A simple 2D vector class
# Author: Matt Anderson, Kristina Striegnitz, John Rieffel
# Winter 2017

class Vector:

    # Constructor
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)

    def __str__(self):
        return "<" + str(self.x) + "," + str(self.y) + ">"

    # Vector length
    def length(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5

    # Vector addition
    def __add__(self, v2):
        return Vector(self.x + v2.x, self.y + v2.y)

    # Vector subtraction
    def __sub__(self, v2):
        return Vector(self.x - v2.x, self.y - v2.y)

    # Vector dot product
    def __mul__(self, v2):
        if type(v2) in [int, float, long]:
            return self.scale(v2)
        return self.x * v2.x + self.y * v2.y

    ##  Extra functions that were useful after first version.

    # Scalar division
    def __div__(self, v2):
        return self.scale(1/float(v2))

    # Scalar product
    def scale(self, c):
        return Vector(self.x * c, self.y * c)

    # Returns parallel component of v with respect to self.
    def para_comp(self, v):
        para_len = (self * v) / self.length()
        return self * (para_len / self.length())

    # Returns perpendicular component of v with respect to self.
    def perp_comp(self, v):
        return v - self.para_comp(v)

    def normalize(self):
        return Vector(self.x / self.length(), self.y / self.length())


# v1 = Vector(2,2)
# v2 = Vector(4,4)
# print v1 / 4
# print v1 + v2
# print v2 - v1
# print v1 * v2
# print v1.length()
# v3 = v1.scale(100)
# print v3.length()
# print v1.perp_comp(v2)
# print v1.para_comp(v2)
# print v1.perp_comp(v1)
# print v1.para_comp(v1)
