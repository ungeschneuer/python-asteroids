from configuration import *
from shapes.polygon import Polygon


class Bullet(Polygon):

    def __init__(self, ship):
        Polygon.__init__(self, BULLET_MODEL, ship.getPoints()[0],
                         ship.getRotation())

        self._speed = 3 + 0.5 * ship.getSpeed()

    def draw(self, screen):
        import pygame

        if self.isActive():
            self.move()
            pygame.draw.polygon(screen, WHITE, self.getPointsArray())

    def move(self):
        import math
        self._pos.x += math.sin(-math.radians(self._rot)) * self._speed
        self._pos.y += math.cos(math.radians(self._rot)) * self._speed

        # Shot gets deactivated when leaving window
        if 0 > self._pos.x > SCREEN_WIDTH or 0 > self._pos.y > SCREEN_HEIGHT:
            self.deactivate()
