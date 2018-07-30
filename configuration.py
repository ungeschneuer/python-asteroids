import os
import sys
from point import Point
from pygame import font
from pygame import init

# COLORS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)

# Dimension
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Control
ROTATION_SENSITIVITY = 6
SHOT_LIMITER = 0.30

# Design
init()
DEFAULT_FONT = font.get_default_font()
FONT_SIZE_HEADLINE = font.Font(DEFAULT_FONT, 80)
FONT_SIZE_TEXT = font.Font(DEFAULT_FONT, 14)

# Models
SHIP_MODEL = [Point(0, 24), Point(-18, -24), Point(0, -18), Point(18, -24)]
ASTROID_MODEL = [Point(0, 24), Point(-18, 24), Point(-23, -30), Point(0, -32), Point(18, 10)]
ROCK_MODEL = [Point(0, 13), Point(-9, 12), Point(-11, -8), Point(3, -11), Point(11, 13)]
BULLET_MODEL = [Point(0, 0.5), Point(-0.5, 0), Point(0, -0.5), Point(0.5, 0)]

# Ship
SHIP_START_LIVES = 3
SHIP_START_STRENGTH = 100
SHIP_ACCELERATION = 0.5
SHIP_BRAKE = 1.2
SHIP_DRIFT = 0.6

# Multiplayer
COLLISION_TIMER = 2

# Highscore
LOCATION_HIGHSCORE = os.path.join(sys.path[0], 'savedhighscore.txt')

# Game
START_LEVEL = 1


def quitwindow():
    import sys
    import pygame

    pygame.display.quit()
    pygame.quit()
    sys.exit()
