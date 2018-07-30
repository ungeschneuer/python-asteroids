from configuration import *
from point import Point
from shapes.polygon import Polygon


class Asteroid(Polygon):

    def __init__(self, position=Point(400, 300), speed=1.0, rotation=90):
        Polygon.__init__(self, ASTROID_MODEL, position,
                         rotation, speed)


class Rock(Polygon):

    def __init__(self, position=Point(400, 300), speed=0.5, rotation=90):
        Polygon.__init__(self, ROCK_MODEL, position,
                         rotation, speed)
