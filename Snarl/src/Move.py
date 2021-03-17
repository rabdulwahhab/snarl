# TODO move player + enemy

from Types import *
from Util import locationInBounds


def moveEntity(level: Level, name: str, currBoard: int,
               destination: tuple, isPlayer: bool):
    """
    Move the Player/Enemy with the given name to the given destination
    in the level.
    :param level: Level
    :param name: str
    :param currBoard: int
    :param destination: tuple
    :param isPlayer: bool
    """
    board = level.boards[currBoard]
    entity = board.players[name] if isPlayer else board.enemies[name]
    destInBoard = locationInBounds(destination, board.origin,
                                   board.dimensions)

    if destInBoard:
        entity.location = destination
    else:
        boardEntities = board.players if isPlayer else board.enemies
        del boardEntities[name]
        for i in range(len(level.boards)):
            otherBoard = level.boards[i]
            if locationInBounds(destination, otherBoard.origin,
                                otherBoard.dimensions):
                entity.location = destination

                if isPlayer:
                    otherBoard.players[name] = entity
                else:
                    otherBoard.enemies[name] = entity
                level.currBoard = i
                break

    return level
