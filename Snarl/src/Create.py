import Globals
import Util
from Util import logInFile
from Types import *
from copy import deepcopy
from random import randint
from more_itertools import interleave, flatten, all_unique
from functools import reduce


def validateLevels(level: Level):
    allBoardTiles = reduce(lambda acc, board: list(flatten([acc, board.tiles])),
                           level.boards, [])
    return all_unique(allBoardTiles) and checkHallways(
        level.boards) and allInRange(allBoardTiles)


def allInRange(tiles: list):
    for tile in tiles:
        if tile.location.first >= Globals.GAME_WIDTH or tile.location.second >= Globals.GAME_HEIGHT:
            return False


def checkHallways(boards: list):
    # if hallway, check if door locations are at board dimensions
    #   and check if door locations are in
    for board in boards:
        if board.boardType == BoardEnum.HALLWAY:
            if len(board.doorLocations) < 2:
                return False
    return True


# TODO Today: Finish create Level and do a render

def addBoardToLevel(level: Level, board: Board):
    newBoards = level.boards + [board]
    updatedLevel = Level(level.keyLocation, level.exitLocation, newBoards,
                         level.exitUnlocked, level.playerTurn)
    return updatedLevel


def addPlayersToBoard(board: Board, players: dict):
    newPlayers = board.players.copy()
    newPlayers.update(players)
    updatedBoard = Board(board.tiles, board.origin, board.dimensions,
                         board.boardType, board.doorLocations, newPlayers,
                         board.enemies)
    return updatedBoard


def addEnemiesToBoard(board: Board, enemies: dict):
    newEnemies = board.enemies.copy()
    newEnemies.update(enemies)
    updatedBoard = Board(board.tiles, board.origin, board.dimensions,
                         board.boardType, board.doorLocations, board.players,
                         newEnemies)
    return updatedBoard


def convertJsonBoard(boardType: str, origin: list, boundaryData: tuple,
                     tileLayout: list):
    boardEnum = BoardEnum.ROOM if boardType == "room" else BoardEnum.HALLWAY
    upperLeftCorner = (origin[0], origin[1])
    tiles = []
    doorLocations = []
    for i in tileLayout:
        for j in tileLayout[i]:
            if tileLayout[i][j] == 0:
                temp = Tile(TileEnum.WALL, (i, j), False)
                tiles.append(temp)
            elif tileLayout[i][j] == 2:
                temp = Tile(TileEnum.DOOR, (i, j), False)
                tiles.append(temp)
                doorLocations.append((i, j))
            else:
                temp = Tile(TileEnum.DEFAULT, (i, j), False)
                tiles.append(temp)
    board = Board(tiles, upperLeftCorner, boundaryData, boardEnum,
                  doorLocations)
    return board


def createGenericBoardTiles(dimensions: tuple, origin: tuple,
                            doorLocations: list, keyLocation=None):
    w, h = dimensions
    boardTiles = []
    for i in range(w):
        for j in range(h):
            relX, relY = (origin[0] + i, origin[1] + j)
            tileType = TileEnum.DOOR if (relX,
                                         relY) in doorLocations else TileEnum.DEFAULT
            tileType = TileEnum.WALL if (i == 0 or i == w - 1) or (
                    j == 0 or j == h - 1) else tileType
            hasKey = (relX, relY) == keyLocation
            newTile = Tile(tileType, (relX, relY), hasKey)
            boardTiles.append(newTile)
    return boardTiles


def createLevel(keyLoc: tuple, exitLoc: tuple, boards: list):
    # TODO rand generation at some point?
    level = Level(keyLoc, exitLoc, boards, False, 0)
    return level


# TODO test
def createDungeon(level: Level, players: dict, enemies: dict):
    """
    Creates a Dungeon with the given levels, players, and enemies.
    :param level: Level
    :param players: List(Player)
    :param enemies: List(Enemy)
    :return: Dungeon
    """
    boardWithPlayers = addPlayersToBoard(level.boards[0], players)
    boardWithEnemies = addEnemiesToBoard(level.boards[len(level.boards) - 1],
                                         enemies)
    level.boards[0] = boardWithPlayers
    level.boards[len(level.boards) - 1] = boardWithEnemies

    return Dungeon([level], list(players.keys()), 0, False)
