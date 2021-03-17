import Globals
from Types import *
from more_itertools import flatten, all_unique
from functools import reduce


def validateLevels(level: Level):
    allBoardTiles = reduce(
        lambda acc, board: list(flatten([acc, getListOfTiles(board.tiles)])),
        level.boards, [])
    return all_unique(allBoardTiles) and checkHallways(
        level.boards) and allInRange(allBoardTiles)


def allInRange(tiles: dict):
    for row in tiles.keys():
        for col in row.keys():
            if row >= Globals.GAME_HEIGHT or col >= Globals.GAME_WIDTH:
                return False
    return True


def checkHallways(boards: list):
    # if hallway, check if door locations are at board dimensions
    #   and check if door locations are in
    for board in boards:
        if board.boardType == BoardEnum.HALLWAY:
            if len(board.doorLocations) < 2:
                return False
    return True


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


def removePlayersFromBoard(board: Board, players: dict):
    newPlayers = board.players.copy()
    for playerName in players.values():
        del newPlayers[playerName]
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


def createGenericBoardTiles(dimensions: tuple, origin: tuple,
                            doorLocations: list):
    rows, cols = dimensions
    boardTiles = dict()
    for r in range(rows):
        for c in range(cols):
            relRow, relCol = (origin[0] + r, origin[1] + c)
            tileType = TileEnum.DOOR if (relRow,
                                         relCol) in doorLocations else TileEnum.DEFAULT
            tileType = TileEnum.WALL if (r == 0 or r == rows - 1) or (
                    c == 0 or c == cols - 1) else tileType
            newTile = Tile(tileType)
            if relRow in boardTiles.keys():
                boardTiles[relRow].update({relCol: newTile})
            else:
                boardTiles[relRow] = {relCol: newTile}

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
