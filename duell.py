import datetime
import pygame
from configuration import *
from point import Point


def newgame(screen):
    from shapes.ship import Ship
    from shapes.bullet import Bullet
    from shapes.star import newConstellation

    # Loop-Stopper
    exitgame = False

    # Framerate
    clock = pygame.time.Clock()

    # Player One
    playerone = Ship(Point(200, 300), "ptwo")
    bulletsone = []
    keypushone = datetime.datetime.now()

    # Player Two
    playertwo = Ship(Point(600, 300), "pone")
    bulletstwo = []
    keypushtwo = datetime.datetime.now()


    # Kollision
    lastcollision = datetime.datetime.now()

    # Constellation
    stars = newConstellation()


    while not exitgame:

        # Control
        # Ways to exit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitwindow()
                if event.key == pygame.K_ESCAPE:
                    exitgame = True


        keys = pygame.key.get_pressed()

        # Player One
        if keys[pygame.K_UP]:
            playertwo.speedup()
            playertwo.move()
        else:
            playertwo.floating()
            playertwo.move()
        if keys[pygame.K_LEFT]:
            playertwo.rotate(-ROTATION_SENSITIVITY)
        if keys[pygame.K_RIGHT]:
            playertwo.rotate(+ROTATION_SENSITIVITY)

        # Shoot Player One
        if keys[pygame.K_m]:
            nowone = datetime.datetime.now()
            if nowone - keypushtwo > datetime.timedelta(seconds=SHOT_LIMITER):
                bulletstwo.append(Bullet(playertwo))
                keypushtwo = nowone


        # Player Two
        if keys[pygame.K_w]:
            playerone.speedup()
            playerone.move()
        else:
            playerone.floating()
            playerone.move()
        if keys[pygame.K_a]:
            playerone.rotate(-ROTATION_SENSITIVITY)
        if keys[pygame.K_d]:
            playerone.rotate(+ROTATION_SENSITIVITY)

        # Shoot Player Two
        if keys[pygame.K_f]:
            nowtwo = datetime.datetime.now()
            if nowtwo - keypushone > datetime.timedelta(seconds=SHOT_LIMITER):
                bulletsone.append(Bullet(playerone))
                keypushone = nowtwo



        # Collision
        # ... with Bullets
        for shootone in bulletsone:
            if playertwo.detect(shootone):
                playertwo.damaged()
                shootone.deactivate()
        for shootwo in bulletstwo:
            if playerone.detect(shootwo):
                playerone.damaged()
                shootwo.deactivate()
        # ... of both ships
        if playertwo.detect(playerone):
            nowcollision = datetime.datetime.now()
            if nowcollision - lastcollision > datetime.timedelta(seconds=COLLISION_TIMER):
                playertwo.damaged()
                playerone.damaged()
                lastcollision = nowcollision


        # Visual
        screen.fill(BLACK)

        # Stars
        for s in stars:
            s.draw(screen)

        # Game Over screen when player lost
        if playertwo.getLives() == 0 or playerone.getLives() == 0:
            gameover(screen, playerone, playertwo)
            exitgame = True

        # proceed normal game
        else:

            # Drawing of all objects in new positions
            playerone.draw(screen)
            playertwo.draw(screen)

            for shoot in list(bulletstwo):
                shoot.draw(screen)
            for shoot in list(bulletsone):
                shoot.draw(screen)

            # Drawing of statistics
            scoreone(playerone, screen)
            scoretwo(playertwo, screen)


        # Aktualisiert den Screen
        pygame.display.flip()

        # Framerate
        clock.tick(60)


# Statistics of Player One
def scoreone(ship, screen):
    # For better reading translucent black background
    background = pygame.Surface([150, 80])
    background.set_alpha(120)
    background.fill(BLACK)
    screen.blit(background, (0, 0))

    font = FONT_SIZE_TEXT

    # Player
    textstrength = "Player 1"
    textstrength = font.render(textstrength, True, WHITE)
    screen.blit(textstrength, (20, 20))

    # Strength of Ship
    textstrength = "Strenght: " + str(ship.getStrength()) + "%"
    textstrength = font.render(textstrength, True, WHITE)
    screen.blit(textstrength, (20, 40))

    # Lives
    textlives = "Lives: " + str(ship.getLives())
    textlives = font.render(textlives, True, WHITE)
    screen.blit(textlives, (20, 60))


# Statistics of Player Two
def scoretwo(ship, screen):
    # For better reading translucent black background
    background = pygame.Surface([150, 80])
    background.set_alpha(120)
    background.fill(BLACK)
    screen.blit(background, (650, 0))

    font = FONT_SIZE_TEXT

    # Player
    textstrength = "Player 2"
    textstrength = font.render(textstrength, True, WHITE)
    screen.blit(textstrength, (665, 20))

    # Strength of Ship
    textstrength = "Strenght: " + str(ship.getStrength()) + "%"
    textstrength = font.render(textstrength, True, WHITE)
    screen.blit(textstrength, (665, 40))

    # Lives
    textlives = "Lives: " + str(ship.getLives())
    textlives = font.render(textlives, True, WHITE)
    screen.blit(textlives, (665, 60))


# Screen when game is over
def gameover(screen, playerone, playertwo):

    font = pygame.font.Font(DEFAULT_FONT, 60)

    if playerone.getLives() == 0:
        text_head = font.render("PLAYER TWO WINS", True, WHITE)
        text_rect_head = text_head.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        screen.blit(text_head, text_rect_head)

    if playertwo.getLives() == 0:
        text_head = font.render("PLAYER ONE WINS", True, WHITE)
        text_rect_head = text_head.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        screen.blit(text_head, text_rect_head)

    font = pygame.font.Font(pygame.font.get_default_font(), 15)
    enterprompt = font.render("PRESS SPACE OR RETURN", True, WHITE)
    screen.blit(enterprompt, (293, 400))

    waiting = True

    while waiting:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                quitwindow()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    waiting = False


        pygame.display.update()
