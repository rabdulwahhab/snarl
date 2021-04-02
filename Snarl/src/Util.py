import Globals
from Types import *
from random import randint
from functools import partial, reduce
import math
import random
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


def genXRandCoords(numRandCoord, rejectCoords, origin, dimensions):
    newCoordinates = set()
    (row, col) = origin
    (width, height) = dimensions
    (maxRow, maxCol) = (width + row - 1, height + col - 1)
    i = 0

    while i < numRandCoord:
        # NOTE forbids wall locations. Can remove if boards no longer
        # quadrilaterals
        newCoord = (randint(row + 1, maxRow - 1), randint(col + 1, maxCol - 1))
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


def getAllTiles(level: Level):
    tiles = {}
    for board in level.boards:
        for row in board.tiles:
            for col in board.tiles[row]:
                if row in tiles.keys():
                    tiles[row].update({col: board.tiles[row][col]})
                else:
                    tiles[row] = {col: board.tiles[row][col]}
    return tiles


def locationInLevelBounds(level: Level, location: tuple):
    for board in level.boards:
        if board.boardType == BoardEnum.HALLWAY:
            if location[0] in board.tiles.keys():
                if location[1] in board.tiles[location[0]].keys():
                    return True
        else:  # TODO the minute levels aren't rectangles, fix this
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
    return location[1] * Globals.TILE_HEIGHT, location[0] * Globals.TILE_WIDTH


def translateScreenLocation(absLoc: tuple):
    return math.floor((absLoc[1] - Globals.STATUS_BAR_HEIGHT) / Globals.TILE_HEIGHT), math.floor(
        absLoc[0] / Globals.TILE_WIDTH)


def formatInitial(name):
    return " {} ".format(name[0])


def getListOfTiles(tiles: dict):
    acc = []
    for row in tiles.keys():
        for col in row.keys():
            acc += tiles[row][col]

    return acc


def whichBoardInLevel(level: Level, givenPoint: tuple):
    row, column = intifyTuple(givenPoint)
    for i in range(len(level.boards)):
        board = level.boards[i]
        if row in board.tiles.keys():
            if column in board.tiles[row].keys():
                return i
    return -1


def isTileOnBoard(location: tuple, board: Board):
    if location[0] in board.tiles.keys():
        if location[1] in board.tiles[location[0]].keys():
            return True
    return False


def getRandomRoomInLevel(level: Level):
    randBoardNum = random.randint(0, len(level.boards) - 1)
    randBoard: Board = level.boards[randBoardNum]
    if randBoard.boardType == BoardEnum.HALLWAY:
        return getRandomRoomInLevel(level)
    else:
        return randBoardNum, randBoard


def getPlayersInLevel(level: Level):
    acc = []
    for board in level.boards:
        acc += list(board.players.keys())
    return acc


def isDoorLocation(location: tuple, game: Dungeon):
    for level in game.levels:
        for board in level.boards:
            if location in board.doorLocations:
                return True
    return False


def isTraversable(location: tuple, game: Dungeon):
    for level in game.levels:
        for board in level.boards:
            if location[0] in board.tiles.keys():
                if location[1] in board.tiles[location[0]].keys():
                    tile: Tile = board.tiles[location[0]][location[1]]
                    if tile.tileType is not TileEnum.WALL:
                        return True
    return False


def isPlayerInGame(playerName: str, game: Dungeon):
    for level in game.levels:
        for board in level.boards:
            if playerName in board.players.keys():
                return True
    return False


def getPlayer(level: Level, playerName: str):
    for board in level.boards:
        if playerName in board.players.keys():
            return board.players[playerName]
    return None


def getEnemy(level: Level, enemyName: str):
    for board in level.boards:
        if enemyName in board.enemies.keys():
            return board.players[enemyName]
    return None

