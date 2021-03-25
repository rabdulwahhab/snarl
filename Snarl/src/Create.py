import Globals
from Types import *
from Util import log


def allInRange(tiles: dict):
    """
    Determines if all tiles are in range of the Gloval game height and width
    param: tiles
    returns: boolean
    """
    for row in tiles.keys():
        for col in row.keys():
            if row >= Globals.GAME_HEIGHT or col >= Globals.GAME_WIDTH:
                return False
    return True


def checkHallways(boards: list):
    """
    if hallway, check if door locations are at board dimensions and check if
    there are at least two door locations
    param: a list of boards
    returns: boolean
    """
    for board in boards:
        if board.boardType == BoardEnum.HALLWAY:
            if len(board.doorLocations) < 2:
                return False
    return True


def addBoardToLevel(level: Level, board: Board):
    """
    Adds the given board to the given level
    param: level
    param: board
    returns: updatedLevel
    """
    newBoards = level.boards + [board]
    updatedLevel = Level(level.keyLocation, level.exitLocation, newBoards,
                         level.exitUnlocked, level.playerTurn)
    return updatedLevel


def addPlayersToBoard(board: Board, players: dict):
    """
    Adds the given player dictionaries to the board.
    param: board
    param: players
    returns: new board
    """
    newPlayers = board.players.copy()
    newPlayers.update(players)
    updatedBoard = Board(board.tiles, board.origin, board.dimensions,
                         board.boardType, board.doorLocations, newPlayers,
                         board.enemies)
    return updatedBoard


def removePlayersFromBoard(board: Board, players: dict):
    """
    Removes the given players from a board
    param: board
    param: players
    returns: new board
    """
    newPlayers = board.players.copy()
    for playerName in players.keys():
        del newPlayers[playerName]
    updatedBoard = Board(board.tiles, board.origin, board.dimensions,
                         board.boardType, board.doorLocations, newPlayers,
                         board.enemies)
    return updatedBoard


def addEnemiesToBoard(board: Board, enemies: dict):
    """
    Adds the given enemy dictionaries to the board.
    param: board
    param: enemies
    returns: new board
    """
    newEnemies = board.enemies.copy()
    newEnemies.update(enemies)
    updatedBoard = Board(board.tiles, board.origin, board.dimensions,
                         board.boardType, board.doorLocations, board.players,
                         newEnemies)
    return updatedBoard


def createGenericBoardTiles(dimensions: tuple, origin: tuple,
                            doorLocations: list):
    """
    Creates a generic board with walls on all sides and a given door location.
    :param dimensions: tuple
    :param origin: tuple
    :param doorLocations: list
    """
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
    """
    Creates a level from the given key location, exit location, and
    list of boards.
    :param keyLoc: tuple
    :param exitLoc: tuple
    :param boards: list
    """
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
