from Types import *
from GameManager import move
from example2 import exampleDungeon2, exampleLevel2, player1
from Util import logInFile

log = logInFile("test_GameManager.py")

"""
Cases:
- one normal, valid move of 1 space
- one normal, valid move of 2 spaces
- move into a wall
- move onto a key (interaction)
- move into an exit (interaction) (players moved)
- move into an exit (from last level)
- move into player
- move onto enemy (interaction)
- move into the void
"""


def testOneNormalMove():
    orig = player1.location
    dest = (11, 2)
    res: Dungeon = move("Saleha", dest, exampleDungeon2)
    level: Level = res.levels[res.currLevel]
    board: Board = level.boards[level.currBoard]
    updatedPlayer: Player = board.players["Saleha"]
    assert updatedPlayer.location is not orig
    assert updatedPlayer.location == dest


def testTwoNormalMove():
    orig = player1.location
    dest = (12, 2)
    res: Dungeon = move("Saleha", dest, exampleDungeon2)
    level: Level = res.levels[res.currLevel]
    board: Board = level.boards[level.currBoard]
    updatedPlayer: Player = board.players["Saleha"]
    assert updatedPlayer.location is not orig
    assert updatedPlayer.location == dest


def testMoveIntoWall():
    orig = player1.location
    log("orig", str(orig))
    dest = (11, 0)
    res: Dungeon = move("Saleha", dest, exampleDungeon2)
    level: Level = res.levels[res.currLevel]
    board: Board = level.boards[level.currBoard]
    updatedPlayer: Player = board.players["Saleha"]
    log("updated loc", str(updatedPlayer.location))
    assert updatedPlayer.location == orig
    assert updatedPlayer.location is not dest
    assert exampleDungeon2 == res


def testMoveIntoKey():
    orig = player1.location
    exampleDungeon2.levels[0].keyLocation = (11, 2)
    log("orig", str(orig))
    dest = (11, 2)
    res: Dungeon = move("Saleha", dest, exampleDungeon2)
    level: Level = res.levels[res.currLevel]
    board: Board = level.boards[level.currBoard]
    updatedPlayer: Player = board.players["Saleha"]
    log("updated loc", str(updatedPlayer.location))
    assert updatedPlayer.location is not orig
    assert updatedPlayer.location == dest
    assert level.exitUnlocked


def testMoveIntoExitAdvanceLevel():
    assert False


def testMoveIntoExitLastLevel():
    assert False


def testMoveIntoPlayer():
    # FIXME adapt/update asserts to pass
    orig = player1.location
    log("orig", str(orig))
    dest = (12, 1)
    res: Dungeon = move("Saleha", dest, exampleDungeon2)
    level: Level = res.levels[res.currLevel]
    board: Board = level.boards[level.currBoard]
    updatedPlayer: Player = board.players["Saleha"]
    log("updated loc", str(updatedPlayer.location))
    assert updatedPlayer.location is not orig
    assert updatedPlayer.location == dest


def testMoveIntoEnemy():
    orig = player1.location
    log("orig", str(orig))
    board: Board = exampleLevel2.boards[exampleLevel2.currBoard]
    enemy1 = Enemy("Green man", (11, 2))
    board.enemies = {"Green man": enemy1}
    dest = (11, 2)
    res: Dungeon = move("Saleha", dest, exampleDungeon2)
    level: Level = res.levels[res.currLevel]
    board: Board = level.boards[level.currBoard]
    assert player1 not in board.players.values()
    assert player1.name in res.players
    assert enemy1 in board.enemies.values()
    assert enemy1.location == dest



def testMoveIntoVoid():
    orig = player1.location
    log("orig", str(orig))
    dest = (101000, 450)
    res: Dungeon = move("Saleha", dest, exampleDungeon2)
    level: Level = res.levels[res.currLevel]
    board: Board = level.boards[level.currBoard]
    updatedPlayer: Player = board.players["Saleha"]
    log("updated loc", str(updatedPlayer.location))
    assert updatedPlayer.location == orig
    assert updatedPlayer.location is not dest
    assert exampleDungeon2 == res
