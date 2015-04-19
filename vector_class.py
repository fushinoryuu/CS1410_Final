__author__ = 'Steve'

import math

class vec2
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

    def __str__(self):
        return "(%s, %s)" %(self.x, self.y)

    @classmethod
    def fromPoints(cls, P1, P2):
        return cls(P2[0] - P1[0], P2[1] - P1[0])

    def magnitude(self):
        return math.sqrt(self.x**2 + self.y**2)

    def normalize(self):
        mag = self.magnitude()
        self.x /= mag
        self.y /= mag

    def __add__(self, right):
        return vec2(self.x + right.x, self.y + right.y)

    def __sub__(self, right):
        return vec2(self.x - right.x, self.y - right.y)

    def __neg__(self):
        return vec2(-self.x, -self.y)

    def __mul__(self, scalar):
        return vec2(self.x * scalar, self.y * scalar)

    def __truediv__(self, scalar):
        return vec2(self.x / scalar, self.y / scalar)

    def test(self):
        return "hi"