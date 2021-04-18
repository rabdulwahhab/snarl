# TODO move player + enemy

from Types import *
from Util import locationInBounds, getPlayer, getEnemy


def moveEntity(level: Level, name: str, currBoard: int, newBoardNum: int,
               destination: tuple, isPlayer: bool):
    """
    Move the Player/Enemy with the given name to the given destination
    in the level.
    :param level: Level
    :param name: str
    :param currBoard: int
    :param newBoardNum: int
    :param destination: tuple
    :param isPlayer: bool
    """
    board = level.boards[currBoard]
    entity = getPlayer(level, name) if isPlayer else getEnemy(level, name)
    destInBoard = locationInBounds(destination, board.origin,
                                   board.dimensions)

    if destInBoard:
        entity.location = destination
    else:
        boardEntities = board.players if isPlayer else board.enemies
        del boardEntities[name]
        if newBoardNum != -1:
            otherBoard = level.boards[newBoardNum]
            entity.location = destination

            if isPlayer:
                otherBoard.players[name] = entity
            else:
                otherBoard.enemies[name] = entity

            level.currBoard = newBoardNum

    return level
