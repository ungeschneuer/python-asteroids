import random
from point import Point
import pygame
from configuration import *


class Star:

    def __init__(self):
        self.position = Point(0, 0)
        self.radius = 2
        self.color = (255, 255, 255)
        self.setRandomBrightness()
        self.setRandomPosition()

    def setRandomBrightness(self):
        b = random.randint(0, 255)
        self.color = (b, b, b)

    def setRandomPosition(self):
        self.position = Point(int(random.uniform(0, SCREEN_WIDTH - 1)), int(random.uniform(0, SCREEN_HEIGHT - 1)))

    def draw(self, screen):

        pygame.draw.circle(screen, self.color, (self.position.x, self.position.y), self.radius)


def newConstellation():
    stars = []

    for i in range(400):
        stars.append(Star())

    return stars
