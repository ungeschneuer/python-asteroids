from configuration import *


# Design of input box
def showbox(screen, string):
    import pygame

    font = pygame.font.Font(DEFAULT_FONT, 40)

    # Text Background
    pygame.draw.rect(screen, BLACK, (280, (SCREEN_HEIGHT / 2) + 60, 245, 44), 0)
    # Box Line
    pygame.draw.rect(screen, WHITE, (278, (SCREEN_HEIGHT / 2) + 62, 245, 46), 1)

    if len(string) != 0:
        screen.blit(font.render(string, 1, WHITE), (284, (SCREEN_HEIGHT / 2) + 65))

    pygame.display.flip()


# Input Box which shows and restricts input
def inputbox(screen):
    import pygame

    inputstring = []

    showbox(screen, "")
    waitforinput = True

    while waitforinput:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitwindow()
            if event.type == pygame.KEYDOWN:
                # Deleting
                if event.key == pygame.K_BACKSPACE:
                    if len(inputstring) > 0:
                        inputstring = inputstring[0:-1]
                elif event.key == pygame.K_RETURN:
                    waitforinput = False
                elif event.key == pygame.K_SPACE:
                    pass
                # Restriction to 6 characters
                elif len(inputstring) < 6 and characterlegal(event.key):
                    inputstring.append(str(event.unicode).upper())

        showbox(screen, "".join(inputstring))

    return "".join(inputstring)


# Checks if character is allowed as input
def characterlegal(code):
    if 33 <= code <= 126:
        return True
    else:
        return False
