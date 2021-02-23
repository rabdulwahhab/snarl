# TODO move player + enemy

from Types import *
from Util import locationInBounds


# -> Level
# TODO test
def movePlayer(level: Level, playerName: str, currBoard: int,
               destination: tuple):
    board = level.boards[currBoard]
    player = board[playerName]
    destInBoard = locationInBounds(destination, board["origin"],
                                   board["dimensions"])

    if destInBoard:
        player.location = destination
    else:
        boardPlayers = board.players.copy()
        del boardPlayers[playerName]
        for i in range(len(level.boards)):
            otherBoard = level.boards[i]
            if locationInBounds(destination, otherBoard["origin"],
                                otherBoard["dimensions"]):
                player.location = destination
                boardPlayers[playerName] = player
                level.currBoard = i
                break

    return level

