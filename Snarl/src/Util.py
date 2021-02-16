import Globals
from random import randint
from functools import partial, reduce


def log(*args):
    out = reduce(lambda acc, s: acc + " " + s, args)
    color = '\033[106m'
    nocolor = '\033[0m'
    print("{color}log{nocolor} {out}".format(color=color, out=out,
                                             nocolor=nocolor))


def logInFile(fileName, fnName="-"):
    return partial(log, "[{file}] {fn} >>>>".format(file=fileName, fn=fnName))


# TODO: function that generates a random coord between WIDTH and HEIGHT that is
# unique from all the ones in given list


def genUniqueCoord():
    """
    # TODO generator here
    :param x: max x as a number
    :param y: max y as a number
    :param givenCoords: Array of Coordinates it should be unique from
    :return:
    """
    alreadyCreated = {}

    while len(alreadyCreated) != Globals.GAME_HEIGHT * Globals.GAME_WIDTH:
        newCoord = (
            randint(0, Globals.GAME_WIDTH), randint(0, Globals.GAME_HEIGHT))
        if newCoord not in alreadyCreated:
            alreadyCreated.add(newCoord)
            yield newCoord


# -----------------------------------
# Sample board
# (0,0) (1,0) (2,0)
# (0,1) (1,1) (2,1)
# (0,2) (1,2) (2,2)

# (width, height)
def genDoorCoords(roomWidth, roomHeight):
    borderSide = (randint(0, 3))
    if borderSide == 0:  # LEFT
        newCoord = (0, randint(0, roomHeight))
    elif borderSide == 1:  # TOP
        newCoord = (randint(0, roomWidth), 0)
    elif borderSide == 2:  # RIGHT
        newCoord = (roomWidth, randint(0, roomHeight))
    else:  # BOTTOM
        newCoord = (randint(0, roomWidth), roomHeight)
    return newCoord


def genXRandCoords(numRandCoord, rejectCoords, dimensions):
    newCoordinates = set()
    (maxWidth, maxHeight) = dimensions
    i = 0

    while i < numRandCoord:
        newCoord = (randint(0, maxWidth), randint(0, maxHeight))
        if newCoord not in newCoordinates and (newCoord not in rejectCoords):
            newCoordinates.add(newCoord)
            i += 1
    return newCoordinates


def getScreenLocation(location):
    return location[0] * Globals.TILE_WIDTH, location[1] * Globals.TILE_HEIGHT


def formatInitial(name):
    return " {} ".format(name[0])
