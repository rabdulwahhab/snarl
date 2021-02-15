from Snarl.src.Util import Globals
from random import randint
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
        newCoord = (randint(0, Globals.GAME_WIDTH), randint(0, Globals.GAME_HEIGHT))
        if newCoord not in alreadyCreated:
            alreadyCreated.add(newCoord)
            yield newCoord

#-----------------------------------
# Sample board
# (0,0) (1,0) (2,0)
# (0,1) (1,1) (2,1)
# (0,2) (1,2) (2,2)

# (width, height)
def genDoorCoords(roomWidth, roomHeight):
    borderSide = (randint(0, 3))
    if borderSide == 0: #LEFT
        newCoord = (0, randint(0, roomHeight))
    elif borderSide == 1: #TOP
        newCoord = (randint(0, roomWidth), 0)
    elif borderSide == 2: #RIGHT
        newCoord = (roomWidth, randint(0, roomHeight))
    else: #BOTTOM
        newCoord = (randint(0, roomWidth), roomHeight)
    return newCoord


def genXRandCoords(numRandCoord, rejectCoords):
    newCoordinates = {}

    i = 0
    while i < numRandCoord:
        newCoord = (randint(0, Globals.GAME_WIDTH), randint(0, Globals.GAME_HEIGHT))
        if newCoord not in newCoordinates and (newCoord not in rejectCoords):
            newCoordinates.add(newCoord)
            i += 1
    return newCoordinates

