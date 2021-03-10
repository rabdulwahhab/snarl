from Types import *
from Rulechecker import playerCanMoveTo
from example2 import exampleLevel2, player1, player2

# TODO Cases: valid move; mvoe to a wall;
#  move to the void; move to a player; move to an exit


"""
destination: tuple, player: Player, level: Level,
                    numMoves: int):
"""


def testPlayerCanMoveToValid():
    dest = (12, 2)
    result = playerCanMoveTo(dest, player1, exampleLevel2, 2)
    assert result


def testPlayerCanMoveToWall():
    dest = (10, 1)
    result = playerCanMoveTo(dest, player2, exampleLevel2, 2)
    assert not result


def testPlayerCanMoveToVoid():
    dest = (5000, 1000)
    result = playerCanMoveTo(dest, player1, exampleLevel2, 2)
    assert not result


def testPlayerCanMoveToPlayer():
    dest = (11, 1)
    result = playerCanMoveTo(dest, player2, exampleLevel2, 2)
    assert not result


# def testPlayerCanMoveToExit():
#     dest = (360, 240)  # see exampleLevel2
#     player3 = Player("exit creep", (359, 240))
#     lastBoardNum = len(exampleLevel2.boards) - 1
#     exampleLevel2.boards[lastBoardNum].players = {"exit creep": player3}
#     result = playerCanMoveTo(dest, player3, exampleLevel2, 2)
#     assert result
