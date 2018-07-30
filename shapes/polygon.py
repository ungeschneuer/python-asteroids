import math
from point import Point
from configuration import WHITE


class Polygon:

    def __init__(self, shape, position, rotation, speed=0):
        if len(shape) < 2:
            raise ValueError('Polygon must have at least two vertices')
        self._shape = shape  # A list of points
        self._pos = position  # The offset mentioned above
        self._rot = rotation  # Zero degrees is due east
        self._radius = self._radius()
        self._speed = speed
        self._active = True

        # ~ First, we find the shape's top-most left-most boundary, its origin.
        origin = Point(self._shape[0].x, self._shape[0].y)
        for p in self._shape:
            if p.x < origin.x:
                origin.x = p.x
            if p.y < origin.y:
                origin.y = p.y

        # ~ Then, we orient all of its points relative to the real origin.
        for p in self._shape:
            p.x -= origin.x
            p.y -= origin.y

    def getPosition(self):
        return self._pos

    def getPositionList(self):
        return self._pos.x, self._pos.y

    def setPosition(self, position):
        self._pos = position

    def getRotation(self):
        return self._rot

    def rotate(self, degrees=0):
        self._rot = (self._rot + degrees) % 360

    def getRadius(self):
        return self._radius

    def getSpeed(self):
        return self._speed

    # Laesst das Schiff in Richtung des Winkels fliegen
    def move(self):
        self._pos.x += math.sin(-math.radians(self._rot)) * self._speed
        self._pos.y += math.cos(math.radians(self._rot)) * self._speed

        if 0 > self._pos.x:
            self._pos.x += 800
        if self._pos.x > 800:
            self._pos.x -= 800
        if 0 > self._pos.y:
            self._pos.y += 600
        if self._pos.y > 600:
            self._pos.y -= 600

    def activate(self):
        self._active = True

    def deactivate(self):
        self._active = False

    def isActive(self):
        return self._active

    def draw(self, screen):
        import pygame

        if self.isActive():
            self.move()
            pygame.draw.polygon(screen, WHITE, self.getPointsArray(), 1)

    # ~ "getPoints" applies the rotation and offset to the shape of the polygon.
    def getPoints(self):
        import stdarray, math
        center = self._findCenter()
        points = stdarray.create1D(len(self._shape))
        for i in range(len(self._shape)):
            p = self._shape[i]
            x = ((p.x - center.x) * math.cos(math.radians(self._rot))) - (
                    (p.y - center.y) * math.sin(math.radians(self._rot))) + center.x / 2 + self._pos.x
            y = ((p.x - center.x) * math.sin(math.radians(self._rot))) + (
                    (p.y - center.y) * math.cos(math.radians(self._rot))) + center.y / 2 + self._pos.y
            points[i] = Point(x, y)
        return points

    def getPointsArray(self):
        import stdarray, math
        center = self._findCenter()
        points = stdarray.create1D(len(self._shape))
        for i in range(len(self._shape)):
            p = self._shape[i]
            x = ((p.x - center.x) * math.cos(math.radians(self._rot))) - (
                    (p.y - center.y) * math.sin(math.radians(self._rot))) + center.x / 2 + self._pos.x
            y = ((p.x - center.x) * math.sin(math.radians(self._rot))) + (
                    (p.y - center.y) * math.cos(math.radians(self._rot))) + center.y / 2 + self._pos.y
            points[i] = [x, y]
        return points

    def _radius(self):
        r = 0

        for po in self._shape:

            if abs(po.x) > r:
                r = abs(po.x)
            if abs(po.y) > r:
                r = abs(po.y)

        return r

    def detect(self, other):
        import math

        if not self.isActive() or not other.isActive():
            return False

        # Pretesting the plausability of a collision
        pos1 = self._pos
        pos2 = other.getPosition()

        distancex = pos1.x - pos2.x
        distancey = pos1.y - pos2.y

        # Pythagoras
        distance = math.sqrt((distancex * distancex) + (distancey * distancey))

        if distance < self._radius + other.getRadius():

            # if possible then 'real math'
            return self.intersects(other)

        return False

    def intersects(self, other):
        for point in self.getPoints():
            if other.contains(point):
                return True
        for point in other.getPoints():
            if self.contains(point):
                return True
        return False

    # ~ "contains" implements some magical math (i.e. the ray-casting algorithm).
    def contains(self, point):
        points = self.getPoints()
        crossingNumber = 0
        for i in range(-1, len(self._shape) - 1):
            if (((points[i].x < point.x) and (point.x <= points[i + 1].x)) or (
                    (points[i + 1].x < point.x) and (point.x <= points[i].x))) and (
                    point.y > points[i].y + (points[i + 1].y - points[i].y) / (points[i + 1].x - points[i].x) * (
                    point.x - points[i].x)):
                crossingNumber += 1
        return crossingNumber % 2 == 1

    # ~ "findArea" implements some more magic math.
    def _findArea(self):
        summe = 0
        for i in range(-1, len(self._shape) - 1):
            summe += self._shape[i].x * self._shape[i + 1].y - self._shape[i + 1].x * self._shape[i].y
        return abs(summe / 2)

    # ~ "findCenter" implements another bit of math.
    def _findCenter(self):
        summe = Point(0, 0)
        for i in range(-1, len(self._shape) - 1):
            summe.x += (self._shape[i].x + self._shape[i + 1].x) * (
                    self._shape[i].x * self._shape[i + 1].y - self._shape[i + 1].x * self._shape[i].y)
            summe.y += (self._shape[i].y + self._shape[i + 1].y) * (
                    self._shape[i].x * self._shape[i + 1].y - self._shape[i + 1].x * self._shape[i].y)
        area = self._findArea()
        return Point(abs(summe.x / (6 * area)), abs(summe.y / (6 * area)))
