from configuration import *
from shapes.polygon import Polygon


class Ship(Polygon):

    def __init__(self, position=Point(400, 300), mode="single"):
        Polygon.__init__(self, SHIP_MODEL, position, 180)

        self._strength = SHIP_START_STRENGTH
        self._lives = SHIP_START_LIVES
        self._score = 0
        self._mode = mode

    def speedup(self):
        self._speed += SHIP_ACCELERATION

    # reduces speed when ship stops accelerating
    def floating(self):

        if self._speed > 20:
            self._speed -= SHIP_DRIFT * 2
        elif self._speed > 0:
            self._speed -= SHIP_DRIFT
        else:
            self._speed = 0


    # Back to starpoint
    def resetPosition(self):
        self._pos = Point(400, 300)
        self._speed = 0
        self._rot = 180

    def resetComplete(self):
        self._pos = Point(400, 300)
        self._speed = 0
        self._rot = 180
        self._strength = SHIP_START_STRENGTH
        self._lives = SHIP_START_LIVES
        self._score = 0

    # Damage after collision
    def damaged(self):
        self.setStrength(-20)
        if self._strength <= 0:
            self.resetPosition()
            self.setLives(-1)
            self.setStrength(100)

    def setStrength(self, number):
        self._strength += number
        if self._strength > 100:
            self._strength = 100

    def getStrength(self):
        return self._strength

    def getLives(self):
        return self._lives

    def setLives(self, number):
        self._lives += number
        if self._lives < 0:
            self._lives = 0

    def setScore(self, number):
        self._score += number
        if self._score < 0:
            self._score = 0

    def getScore(self):
        return self._score

    # Updating position and appeareance
    def draw(self, screen):
        import pygame

        if self._mode == "single":
            # Appearance defined by damage
            if self._strength > 60:
                pygame.draw.polygon(screen, GREEN, self.getPointsArray(), 4)
            elif 60 >= self._strength > 40:
                pygame.draw.polygon(screen, ORANGE, self.getPointsArray(), 2)
            elif self._strength <= 40:
                pygame.draw.polygon(screen, RED, self.getPointsArray(), 1)
        elif self._mode == "pone":
            pygame.draw.polygon(screen, GREEN, self.getPointsArray())
        elif self._mode == "ptwo":
            pygame.draw.polygon(screen, RED, self.getPointsArray())


