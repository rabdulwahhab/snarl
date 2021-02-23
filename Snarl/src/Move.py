# TODO move player + enemy

from Types import *
from Util import locationInBounds


# -> Level
# TODO GIANT test
def moveEntity(level: Level, name: str, currBoard: int,
               destination: tuple, isPlayer: bool):
    board = level.boards[currBoard]
    entity = board.players[name] if isPlayer else board.enemies[name]
    destInBoard = locationInBounds(destination, board["origin"],
                                   board["dimensions"])

    if destInBoard:
        entity.location = destination
    else:
        boardEntities = board.players.copy() if isPlayer else board.enemies.copy()
        del boardEntities[name]
        for i in range(len(level.boards)):
            otherBoard = level.boards[i]
            if locationInBounds(destination, otherBoard["origin"],
                                otherBoard["dimensions"]):
                entity.location = destination
                boardEntities[name] = entity
                if isPlayer:
                    board.players = boardEntities
                else:
                    board.enemies = boardEntities
                level.currBoard = i
                break

    return level
