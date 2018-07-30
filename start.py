import pygame
from configuration import *
from shapes.star import newConstellation

#               _                 _     _
#              | |               (_)   | |
#      __ _ ___| |_ ___ _ __ ___  _  __| |
#     / _` / __| __/ _ \ '__/ _ \| |/ _` |
#    | (_| \__ \ ||  __/ | | (_) | | (_| |
#     \__,_|___/\__\___|_|  \___/|_|\__,_|
#             by Marcel Schneuer

# Display
size = (SCREEN_WIDTH, SCREEN_HEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Asteroid by Marcel Schneuer")

# Initialisierung
pygame.init()


def mainmenu():
    global screen
    import duell
    import classic

    # Menu
    index = 0
    options = [
        FONT_SIZE_HEADLINE.render("CLASSIC", 1, WHITE),
        FONT_SIZE_HEADLINE.render("DUELL", 1, WHITE),
        FONT_SIZE_HEADLINE.render("HIGHSCORE", 1, WHITE),
        FONT_SIZE_HEADLINE.render("EXIT", 1, WHITE)
    ]

    # Selector
    selector = pygame.Surface([SCREEN_WIDTH, 100])
    selector.set_alpha(100)
    selector.fill(WHITE)

    # Different background every time
    stars = newConstellation()

    while True:

        # Background
        screen.fill(BLACK)

        for s in stars:
            s.draw(screen)

        # Position of text
        for j in range(len(options)):
            screen.blit(options[j], (150, 114 + j * 100))

        # Position of selector
        screen.blit(selector, (0, 99 + index * 100))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitwindow()

            # Choosing Option
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    if index == 0:
                        index = 1
                    elif index == 1:
                        index = 2
                    elif index == 2:
                        index = 3
                    elif index == 3:
                        index = 0

                if event.key == pygame.K_UP:
                    if index == 0:
                        index = 3
                    elif index == 1:
                        index = 0
                    elif index == 2:
                        index = 1
                    elif index == 3:
                        index = 2

                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    # Game
                    if index == 0:
                        singlecontrol()
                        classic.newgame(screen)
                    # Multiplayer
                    elif index == 1:
                        multicontrol()
                        duell.newgame(screen)
                    # Highscore
                    elif index == 2:
                        highscore()
                    # Exit
                    elif index == 3:
                        quitwindow()


def highscore():
    import scoreboard
    global screen

    # Open highscore file
    screenrunning = True
    font = pygame.font.Font(DEFAULT_FONT, 38)
    scores = scoreboard.read()

    # Seperating by name and score
    name = []
    score = []

    for x in scores:
        scorer = font.render(x[0], 1, WHITE)
        points = font.render(x[1], 1, WHITE)

        name.append(scorer)
        score.append(points)

    screen.fill(BLACK)

    stars = newConstellation()
    for s in stars:
        s.draw(screen)

    # textposition
    for j in range(len(scores)):
        screen.blit(name[j], (164, 30 + j * 48))
        screen.blit(score[j], (423, 30 + j * 48))

    # Info
    infofont = pygame.font.Font(DEFAULT_FONT, 18)
    info = infofont.render("PRESS RETURN OR SPACE", 1, WHITE)
    screen.blit(info, (260, 535))

    while screenrunning:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    screenrunning = False

        pygame.display.flip()

# Shows Gaming Control for Classic Mode
def singlecontrol():
    global screen

    # Background
    screen.fill(BLACK)
    stars = newConstellation()
    for s in stars:
        s.draw(screen)

    # Header
    headfont = FONT_SIZE_HEADLINE
    text_head = headfont.render("ASTROID", True, WHITE)
    text_rect_head = text_head.get_rect(center=(SCREEN_WIDTH / 2, 110))
    screen.blit(text_head, text_rect_head)

    sublinefont = FONT_SIZE_TEXT

    text_subline = sublinefont.render("by Marcel Schneuer", True, WHITE)
    text_rect_subline = text_subline.get_rect(center=(SCREEN_WIDTH / 2, 155))
    screen.blit(text_subline, text_rect_subline)


    # Instructions
    font = pygame.font.Font(DEFAULT_FONT, 35)

    instructions = [
        "ROTATE LEFT",
        "ROTATE RIGHT",
        "ACCELERATE",
        "SHOOT",
        "PAUSE",
        "BACK TO MENU"
    ]

    key = [
        "LEFT ARROW",
        "RIGHT ARROW",
        "UP ARROW",
        "SPACEBAR",
        "P",
        "Q OR ESC"
    ]

    # textposition
    for j in range(len(instructions)):
        screen.blit(font.render(instructions[j], 1, WHITE), (100, 210 + j * 50))
        screen.blit(font.render(key[j], 1, WHITE), (450, 210 + j * 50))

    # Info
    infofont = pygame.font.Font(DEFAULT_FONT, 18)
    info = infofont.render("PRESS RETURN OR SPACE TO START", 1, WHITE)
    screen.blit(info, (260, 530))

    screenrunning = True

    while screenrunning:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    screenrunning = False

        pygame.display.flip()


# Shows Gaming Control for Duell Mode
def multicontrol():
    global screen

    screen.fill(BLACK)
    stars = newConstellation()
    for s in stars:
        s.draw(screen)

    headfont = FONT_SIZE_HEADLINE
    text_head = headfont.render("ASTROID", True, WHITE)
    text_rect_head = text_head.get_rect(center=(SCREEN_WIDTH / 2, 110))
    screen.blit(text_head, text_rect_head)

    sublinefont = FONT_SIZE_TEXT

    text_subline = sublinefont.render("by Marcel Schneuer", True, WHITE)
    text_rect_subline = text_subline.get_rect(center=(SCREEN_WIDTH / 2, 155))
    screen.blit(text_subline, text_rect_subline)

    font = pygame.font.Font(DEFAULT_FONT, 20)

    instructions = [
        "",
        "ROTATE LEFT",
        "ROTATE RIGHT",
        "ACCELERATE",
        "SHOOT",
        "MENU"
    ]

    pone = [
        "PLAYER ONE",
        "A",
        "D",
        "W",
        "F",
        "ESC"
    ]

    ptwo = [
        "PLAYER TWO",
        "LEFT ARROW",
        "RIGHT ARROW",
        "UP ARROW",
        "M",
        "ESC"
    ]


    # textposition
    for j in range(len(instructions)):
        screen.blit(font.render(instructions[j], 1, WHITE), (115, 210 + j * 50))
        screen.blit(font.render(pone[j], 1, WHITE), (335, 210 + j * 50))
        screen.blit(font.render(ptwo[j], 1, WHITE), (525, 210 + j * 50))

    # Info
    infofont = pygame.font.Font(DEFAULT_FONT, 18)
    info = infofont.render("PRESS RETURN OR SPACE TO START", 1, WHITE)
    screen.blit(info, (260, 530))

    screenrunning = True

    while screenrunning:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    screenrunning = False

        pygame.display.flip()


if __name__ == "__main__":
    mainmenu()
