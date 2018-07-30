import datetime
import pygame
from configuration import *


def newgame(screen):
    from shapes.ship import Ship
    from shapes.asteroid import Asteroid
    from shapes.asteroid import Rock
    from shapes.bullet import Bullet
    from shapes.star import newConstellation
    global level

    # Loop-Stopper
    exitgame = False

    # Framerate
    clock = pygame.time.Clock()

    # Bullets
    bullets = []
    keypush = datetime.datetime.now()

    # Asteroids
    hurdles = cannonfodder()

    # Ship
    ship = Ship()

    # Constellation
    stars = newConstellation()

    # Level Up
    destroyed = 0
    level = START_LEVEL

    while not exitgame:

        # Control
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitwindow()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused(screen)
                if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                    exitgame = True

        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            ship.speedup()
            ship.move()
        else:
            ship.floating()
            ship.move()
        if keys[pygame.K_LEFT]:
            ship.rotate(-ROTATION_SENSITIVITY)
        if keys[pygame.K_RIGHT]:
            ship.rotate(+ROTATION_SENSITIVITY)

        # Shoot mit Schusslimitierung
        if keys[pygame.K_SPACE]:
            now = datetime.datetime.now()
            if now - keypush > datetime.timedelta(seconds=SHOT_LIMITER):
                bullets.append(Bullet(ship))
                keypush = now

        # Kollisionen
        for asteroid in hurdles:
            if ship.detect(asteroid):
                destroyed += 1
                ship.damaged()
                asteroid.deactivate()
            for shoot in list(bullets):
                if shoot.detect(asteroid):
                    shoot.deactivate()
                    if type(asteroid) is Asteroid:
                        ship.setScore(5)
                        destroyed += 1
                        breaktwo(asteroid, hurdles, level)
                    if type(asteroid) is Rock:
                        ship.setScore(10)
                        destroyed += 1
                    asteroid.deactivate()

        # Visual
        screen.fill(BLACK)

        # Stars
        for s in stars:
            s.draw(screen)

        # Game Over screen when player lost
        if ship.getLives() == 0:
            gameover(screen, ship)
            exitgame = True

        # Level up when every asteroid is destroyed
        elif destroyed == len(hurdles):
            level += 1

            # Generating the Level
            hurdles = cannonfodder(level)
            ship.resetPosition()
            bullets = []
            stars = newConstellation()
            destroyed = 0

            # Bonus
            if level % 5 == 0:
                ship.setLives(1)

            nextlevel(screen, datetime.datetime.now(), level)

        # proceed normal game
        else:

            # Drawing of all objects in new positions
            ship.draw(screen)

            for asteroid in hurdles:
                asteroid.draw(screen)

            for shoot in list(bullets):
                shoot.draw(screen)

            score(ship, level, screen)

        # Aktualisiert den Screen
        pygame.display.flip()

        # Framerate
        clock.tick(60)


# If big rock is destroyed it breaks in two
def breaktwo(asteroid, hurdles, level):
    from shapes.asteroid import Rock
    from point import Point
    rot = asteroid.getRotation()
    pos = asteroid.getPosition()
    speed = level * 0.3 + 0.3
    rockone = Rock(Point(pos.x + 15, pos.y + 15), speed, 360 - rot)
    rocktwo = Rock(Point(pos.x - 15, pos.y - 15), speed, rot)
    hurdles.append(rockone)
    hurdles.append(rocktwo)


# Pausing the game with Info on the screen
def paused(screen):
    font = FONT_SIZE_HEADLINE
    text_head = font.render("PAUSE", True, WHITE)
    text_rect_head = text_head.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
    screen.blit(text_head, text_rect_head)

    pause = True

    while pause:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                quitwindow()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pause = False

        pygame.display.update()


# Random position of asteroids in the field
def cannonfodder(level=1):
    from shapes.asteroid import Asteroid
    from shapes.asteroid import Rock
    import random
    from point import Point

    # Astroids of all kind
    hurdles = []
    for i in range(random.randint(7, 13)):
        x, y = 400, 300
        while 350 < x < 450:
            x = random.randint(0, SCREEN_WIDTH)
        while 250 < y < 350:
            y = random.randint(0, SCREEN_HEIGHT)
        rot = random.randint(0, 360)
        speed = level * 0.25 + 0.6
        hurdles.append(Asteroid(Point(x, y), speed, rot))

    # Rocks
    for i in range(random.randint(10, 25)):
        x, y = 400, 300
        while 350 < x < 450:
            x = random.randint(0, SCREEN_WIDTH)
        while 250 < y < 350:
            y = random.randint(0, SCREEN_HEIGHT)
        rot = random.randint(0, 360)
        speed = level * 0.25 + 0.3
        hurdles.append(Rock(Point(x, y), speed, rot))

    return hurdles


def score(ship, level, screen):
    # For better reading translucent black background
    background = pygame.Surface([135, 103])
    background.set_alpha(120)
    background.fill(BLACK)
    screen.blit(background, (0, 0))

    font = FONT_SIZE_TEXT

    # Strangth of Ship
    textstrength = "Strenght: " + str(ship.getStrength()) + "%"
    textstrength = font.render(textstrength, True, WHITE)
    screen.blit(textstrength, (20, 20))

    # Lives
    textlives = "Lives: " + str(ship.getLives())
    textlives = font.render(textlives, True, WHITE)
    screen.blit(textlives, (20, 40))

    # Points
    textscores = "Score: " + str(ship.getScore())
    textscores = font.render(textscores, True, WHITE)
    screen.blit(textscores, (20, 60))

    # Level
    textscores = "Level: " + str(level)
    textscores = font.render(textscores, True, WHITE)
    screen.blit(textscores, (20, 80))


# Screen when game is over
def gameover(screen, ship):
    from textbox import inputbox
    from scoreboard import write_highscore

    font = FONT_SIZE_HEADLINE

    text_head = font.render("GAME OVER", True, WHITE)
    text_rect_head = text_head.get_rect(center=(SCREEN_WIDTH / 2, 130))
    screen.blit(text_head, text_rect_head)

    font = pygame.font.Font(pygame.font.get_default_font(), 40)
    scoreinfo = font.render("Score: " + str(ship.getScore()), True, WHITE)
    text_rect_score = scoreinfo.get_rect(center=(SCREEN_WIDTH / 2, 210))
    screen.blit(scoreinfo, text_rect_score)

    font = pygame.font.Font(pygame.font.get_default_font(), 25)
    nameprompt = font.render("PLEASE ENTER YOUR NAME", True, WHITE)
    screen.blit(nameprompt, (219, 300))

    font = pygame.font.Font(pygame.font.get_default_font(), 15)
    enterprompt = font.render("PRESS RETURN TO CONFIRM", True, WHITE)
    screen.blit(enterprompt, (293, 500))

    # Input for Highscore
    name = inputbox(screen)
    if len(name) != 0:
        write_highscore(ship.getScore(), name)


def nextlevel(screen, timepoint, level):
    screen.fill(BLACK)

    font = FONT_SIZE_HEADLINE
    text_head = font.render(("Level " + str(level)), True, WHITE)
    text_rect_head = text_head.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
    screen.blit(text_head, text_rect_head)

    font = pygame.font.Font(pygame.font.get_default_font(), 15)
    enterprompt = font.render("PRESS ANY KEY TO CONTINUE", True, WHITE)
    screen.blit(enterprompt, (282, 400))

    # Waits for user to acknowledge the screen
    waitforinput = True
    while waitforinput:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitwindow()
            if event.type == pygame.KEYDOWN and datetime.datetime.now() - timepoint > datetime.timedelta(seconds=0.5):
                waitforinput = False

        pygame.display.flip()
