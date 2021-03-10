import Globals
from Types import *
from random import randint
from functools import partial, reduce
from more_itertools import first_true


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


def intifyTuple(nonTupleOrTuple: tuple):
    i1 = int(nonTupleOrTuple[0])
    i2 = int(nonTupleOrTuple[1])
    return i1, i2


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


def getLocationsAround(location: tuple):
    x, y = location
    above = (x, y + 1)
    below = (x, y - 1)
    right = (x + 1, y)
    left = (x - 1, y)
    return [above, right, below, left]


def locationInLevelBounds(level: Level, location: tuple):
    for board in level.boards:
        if locationInBounds(location, board.origin, board.dimensions):
            return True
    return False


def locationInBounds(location: tuple, origin: tuple, dimension: tuple):
    x, y = location
    ox, oy = origin
    dx, dy = dimension
    mx = ox + dx
    my = oy + dy
    return ox <= x < mx and oy <= y < my


def getScreenLocation(location):
    return location[0] * Globals.TILE_WIDTH, location[1] * Globals.TILE_HEIGHT


def formatInitial(name):
    return " {} ".format(name[0])


def whichBoardInLevel(level: Level, givenPoint: tuple):
    pointX = int(givenPoint[0])
    pointY = int(givenPoint[1])
    point = (pointX, pointY)
    for i in range(len(level.boards)):
        currBoard: Board = level.boards[i]
        if currBoard.boardType == BoardEnum.ROOM:
            if locationInBounds(point, currBoard.origin, currBoard.dimensions):
                return i
        else:
            hallwayTiles = currBoard.tiles
            if first_true(hallwayTiles, default=None,
                          pred=lambda tile: tile.location == point) is not None:
                return i
    return -1
