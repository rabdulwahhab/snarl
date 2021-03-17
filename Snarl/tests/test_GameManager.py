from Types import *
from GameManager import move
from example2 import exampleDungeon2, exampleLevel2, player1
from Util import logInFile, locationInBounds

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

# TODO MAKE THINGS LOOK GOOD

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


def testMoveIntoExitNotUnlocked():
    orig = player1.location
    exampleDungeon2.levels[0].exitLocation = (11, 2)
    dest = (11, 2)
    res: Dungeon = move("Saleha", dest, exampleDungeon2)
    level: Level = res.levels[res.currLevel]
    board: Board = level.boards[level.currBoard]
    updatedPlayer: Player = board.players["Saleha"]
    assert updatedPlayer.location is not orig
    assert updatedPlayer.location == dest
    assert not level.exitUnlocked
    assert res.currLevel == exampleDungeon2.currLevel


def testMoveIntoExitAdvanceLevel():
    # Given
    orig = player1.location
    exampleDungeon2.levels[0].exitLocation = (11, 2)
    exampleDungeon2.levels[0].exitUnlocked = True
    exampleDungeon2.levels.append(exampleLevel2)
    dest = (11, 2)

    # When
    res: Dungeon = move("Saleha", dest, exampleDungeon2)
    level: Level = res.levels[res.currLevel]
    board: Board = level.boards[level.currBoard]

    # Then
    assert "Saleha" not in board.players.keys()

    # first level exit has been unlocked
    assert res.levels[res.currLevel].exitUnlocked

    # Exited player has been removed from the board players
    assert len(board.players.values()) == 1


def testMoveIntoExitLastLevel():
    # Given
    orig = player1.location
    exampleDungeon2.levels[0].exitLocation = (11, 2)
    exampleDungeon2.levels[0].exitUnlocked = True
    dest = (11, 2)

    # When
    res: Dungeon = move("Saleha", dest, exampleDungeon2)
    res: Dungeon = move("Rayyan", dest, res)

    level: Level = res.levels[res.currLevel]
    board: Board = level.boards[level.currBoard]

    # Then
    # No players left in the board (all exited)
    assert len(board.players.values()) == 0

    # The game is over (game won)
    # TODO should fail until advanceLevel is implemented
    # assert res.isGameOver


def testMoveIntoPlayer():
    # Given
    orig = player1.location
    dest = (12, 1)

    # When
    res: Dungeon = move("Saleha", dest, exampleDungeon2)
    level: Level = res.levels[res.currLevel]
    board: Board = level.boards[level.currBoard]
    updatedPlayer: Player = board.players["Saleha"]

    # Then no change
    assert updatedPlayer.location is orig
    assert updatedPlayer.location is not dest
    assert res == exampleDungeon2


def testMoveIntoEnemy():
    # Given
    orig = player1.location
    log("orig", str(orig))
    board: Board = exampleLevel2.boards[exampleLevel2.currBoard]
    enemy1 = Enemy("Green man", (11, 2))
    board.enemies = {"Green man": enemy1}
    dest = (11, 2)

    # When
    res: Dungeon = move("Saleha", dest, exampleDungeon2)
    level: Level = res.levels[res.currLevel]
    board: Board = level.boards[level.currBoard]

    # Then
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
