from Types import *
from Util import whichBoardInLevel, getLocationsAround, locationInBounds
from more_itertools import unique_everseen


def playerCanMoveTo(destination: tuple, player: Player, level: Level,
                    numMoves: int):
    """
    Check if the destination given can be moved to by a given player
    """
    # NOTE this gets all locations in the board
    destBoardNumber = whichBoardInLevel(level, destination)
    playerBoardNumber = whichBoardInLevel(level, player.location)
    possibleMoves = playerPossibleCardinalMoves(player.location, numMoves,
                                                level, playerBoardNumber)
    if destination not in possibleMoves:
        return False

    board = level.boards[destBoardNumber]
    for tile in board.tiles:
        if tile == destination \
                and tile.tileType is not TileEnum.WALL \
                and not destHasPlayer(destination, board):
            return True

    return False


def enemyCanMoveTo(destination: tuple, enemy: Enemy, level: Level):
    """
    Check if the destination given can be moved to by a given enemy
    """
    # Return name as playerCanMoveTo for now
    # TODO:
    #  possMoves: call playerPossibleMoves using player's location
    #  check if destination is in possMoves
    return True


def playerPossibleCardinalMoves(location: tuple, numMoves: int, level: Level,
                                boardNumber: int):
    """
    Outputs the possible moves for a player given the number of cardinal moves
    """
    board = level.boards[boardNumber]
    possibleMoves = []
    while numMoves > 0:
        if len(possibleMoves) == 0:
            possibleMoves += list(filter(
                lambda lamLoc: locationInBounds(lamLoc, board.origin,
                                                board.dimensions),
                getLocationsAround(location)))
        else:
            for loc in possibleMoves:
                possibleMoves += list(filter(
                    lambda lamLoc: locationInBounds(lamLoc, board.origin,
                                                    board.dimensions),
                    getLocationsAround(loc)))

        numMoves -= 1
        possibleMoves = unique_everseen(possibleMoves)
    return possibleMoves


def enemyPossibleCardinalMoves(location: tuple, enemy: Enemy, level: Level):
    """
    Outputs the possible moves for an enemy (given the Enemy may have different
    rules for movement)
    """
    # TODO: NO NUM MOVES, SO STANDARD + 2
    #  Call playerPossibleMoves(with numMoves = 2)
    return []


def destHasEnemy(destination: tuple, board: Board):
    """
    Checks if moving to the destination will cause an interaction with an enemy
    """
    for enemy in board.enemies:
        if destination == enemy.location:
            return True
    return False


def destHasPlayer(destination: tuple, board: Board):
    """
    Checks if moving to the destination will cause an interaction with another
    player
    """
    # TODO:
    #  ESSENTIALLY: check if board's players have a location equal to that of dest
    for player in board.players:
        if destination == player.location:
            return True
    return False


def destHasKey(destination: tuple, level: Level):
    """
    Checks if moving to the destination will cause an interaction with a key
    """
    keyLoc = level.keyLocation
    return destination == keyLoc


def destHasItem(destination: tuple, board: Board):
    """
    Checks if moving to the destination will cause an interaction with an item
    """
    for item in board.items:
        if destination == item.location:
            return True
    return False


def isLevelOver(level: Level):
    return level.exitUnlocked


def isGameOver(dungeon: Dungeon):
    return dungeon.isGameOver


def isGameWon(dungeon: Dungeon):
    levelsUnlocked = [level.exitUnlocked for level in dungeon.levels]
    return all(levelsUnlocked)
