from configuration import *


# takes highscore from game over screen an tests if it good enough for top ten
def write_highscore(score, name):
    file = open(LOCATION_HIGHSCORE, 'r')
    lines = file.readlines()
    file.close()

    scores = []

    for line in lines:
        highscore, scorer = line.strip('\n').split(',')
        highscore = int(highscore)

        scores.append((highscore, scorer))

    # Iterate trough scores
    # if higher than some value it gets added
    # lowest value gets dropped
    for x, y in scores:
        if x < score:
            scores.append((score, name))
            scores.sort(reverse=True)
            newscores = scores[:-1]

            file = open(LOCATION_HIGHSCORE, 'w')

            for i, j in newscores:
                file.write(str(i) + "," + j + "\n")

            file.close()

            return True

    return False


# Resets Highscore
def reset():
    file = open(LOCATION_HIGHSCORE, 'w')

    for i in range(10):
        file.write(str(0) + ',' + "XXXXXX\n")

    file.close()


# Reads textfile end transforms it in a better format
def read():
    file = open(LOCATION_HIGHSCORE, 'r')
    lines = file.readlines()
    file.close()

    highscore = []

    for line in lines:
        score, scorer = line.strip('\n').split(',')
        highscore.append((scorer, score))

    return highscore
