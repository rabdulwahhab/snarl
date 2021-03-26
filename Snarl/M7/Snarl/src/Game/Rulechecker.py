from Types import *
from Util import whichBoardInLevel, getLocationsAround, locationInBounds, \
    locationInLevelBounds, isTileOnBoard, logInFile
from more_itertools import unique_everseen

log = logInFile("Rulechecker.py")

def playerCanMoveTo(destination: tuple, player: Player, level: Level,
                    numMoves: int):
    """
    Check if the destination given can be moved to by a given player.
    (True if destination does not have a player and is traversable)
    :param destination: tuple
    :param player: Player
    :param level: Level
    :param numMoves: int
    """
    # NOTE this gets all locations in the board
    destBoardNumber = whichBoardInLevel(level, destination)
    playerBoardNumber = whichBoardInLevel(level, player.location)
    possibleMoves = playerPossibleCardinalMoves(player.location, numMoves,
                                                level)
    if destination not in possibleMoves:
        return False

    board = level.boards[destBoardNumber]

    if isTileOnBoard(destination, board):
        if board.tiles[destination[0]][
            destination[1]].tileType is not TileEnum.WALL \
                and not destHasPlayer(destination, board):
            return True
    return False


def enemyCanMoveTo(destination: tuple, enemy: Enemy, level: Level):
    """
    Check if the destination given can be moved to by a given enemy
    :param destination: tuple
    :param enemy: Enemy
    :param level: Level
    """
    # TODO: not needed yet
    destBoardNumber = whichBoardInLevel(level, destination)
    enemyBoardNumber = whichBoardInLevel(level, enemy.location)
    # TODO: will need to change to enemyPossibleCardinalMoves when specs for
    #  enemy movement come in, for now using player cardinal movement.
    possibleMoves = playerPossibleCardinalMoves(enemy.location, 2,
                                                level)

    if destination not in possibleMoves:
        return False

    board = level.boards[destBoardNumber]
    if isTileOnBoard(destination, board):
        if board.tiles[destination[0]][
            destination[1]].tileType is not TileEnum.WALL:
            return True
    return False


# TODO: FIX ME: Should see board number thing
def playerPossibleCardinalMoves(location: tuple, numMoves: int, level: Level):
    """
    Outputs the possible moves for a player given the number of cardinal moves.
    :param location: tuple
    :param numMoves: int
    :param level: Level
    """
    possibleMoves = []
    while numMoves > 0:
        if len(possibleMoves) == 0:
            possibleMoves += list(filter(
                lambda lamLoc: locationInLevelBounds(level, lamLoc),
                getLocationsAround(location)))
        else:
            temp = []
            for loc in possibleMoves:
                temp += list(filter(
                    lambda lamLoc: locationInLevelBounds(level, lamLoc),
                    getLocationsAround(loc)))
            possibleMoves += temp
        possibleMoves = list(unique_everseen(possibleMoves, key=tuple))
        numMoves -= 1
    return possibleMoves


def enemyPossibleCardinalMoves(location: tuple, enemy: Enemy, level: Level):
    """
    Outputs the possible moves for an enemy (given the Enemy may have different
    rules for movement).
    :param location: tuple
    :param enemy: Enemy
    :param level: Level
    """
    # TODO: will need this when zombie/ghost funtionality specs come in,
    #  until then assuming player carcinal move functionality for enemies
    return []


def destHasEnemy(destination: tuple, board: Board):
    """
    Checks if moving to the destination will cause an interaction with an enemy.
    :param destination: tuple
    :param board: Board
    """
    for enemyName in board.enemies.keys():
        enemy = board.enemies[enemyName]
        if destination == enemy.location:
            return True
    return False


def destHasPlayer(destination: tuple, board: Board):
    """
    Checks if moving to the destination will cause an interaction with another
    player.
    :param destination: tuple
    :param board: Board
    """
    for playerName in board.players.keys():
        player = board.players[playerName]
        if destination == player.location:
            return True
    return False


def destHasKey(destination: tuple, level: Level):
    """
    Checks if moving to the destination will cause an interaction with a key.
    :param destination: tuple
    :param level: Level
    """
    return destination == level.keyLocation


def destHasExit(destination: tuple, level: Level):
    """
    Checks if moving to the destination will cause an interaction with an exit.
    :param destination: tuple
    :param level: Level
    """
    return destination == level.exitLocation


def destHasItem(destination: tuple, board: Board):
    """
    Checks if moving to the destination will cause an interaction with an item
    :param destination: tuple
    :param board: Board
    """
    for item in board.items:
        if destination == item.location:
            return True
    return False


def isLevelOver(level: Level):
    """
    Determines if the level is over (all players no longer in level's boards.
    :param level: Level
    """
    currBoard: Board = level.boards[level.currBoard]
    return len(currBoard.players.values()) == 0


def isGameOver(dungeon: Dungeon):
    """
    Determines if the game is over.
    :param dungeon: Dungeon
    """
    return dungeon.isGameOver


def isGameWon(dungeon: Dungeon):
    """
    Determines if the game has been won (all levels' exits have been unlocked
    and current level is over).
    :param dungeon: Dungeon
    """
    levelsUnlocked = [level.exitUnlocked for level in dungeon.levels]
    currLevel: Level = dungeon.levels[dungeon.currLevel]
    return all(levelsUnlocked) and isLevelOver(currLevel)


def isCurrentLevelOver(game: Dungeon):
    currLevel: Level = game.levels[game.currLevel]
    currBoard: Board = currLevel.boards[currLevel.currBoard]
    return currLevel.exitUnlocked and len(currBoard.players) == 0





