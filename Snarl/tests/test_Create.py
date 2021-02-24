from Create import createDungeon, addPlayersToBoard, addEnemiesToBoard, \
    addBoardToLevel
from Types import *
from example2 import enemies, players, boards, keyLoc, exitLoc, room1


def testCreateDungeon():
    level = Level(keyLoc, exitLoc, boards, False, "Saleha")
    dungeon = createDungeon(level, players,
                            enemies)

    assert len(dungeon.levels) == 1
    assert dungeon.players == ["Saleha", "Rayyan"]

    dungLevel: Level = dungeon.levels[dungeon.currLevel]
    assert dungLevel.keyLocation == keyLoc
    assert dungLevel.exitLocation == exitLoc
    assert not dungLevel.exitUnlocked
    assert dungLevel.playerTurn == "Saleha"

    dungLevelBoards = dungLevel.boards
    assert len(dungLevelBoards) == 5

    board1: Board = dungLevelBoards[dungLevel.currBoard]
    assert board1.boardType == BoardEnum.ROOM
    assert len(board1.players) == 2


def testAddPlayersToBoard():
    player1 = Player('test', (20, 20))
    updatedRoom = addPlayersToBoard(room1, {"player1": player1})
    assert len(updatedRoom.players) == 1

    updatedRoom2 = addPlayersToBoard(updatedRoom, players)
    assert len(updatedRoom2.players) == 3
    assert "Saleha" in list(updatedRoom2.players.keys())

    updatedRoom3 = addPlayersToBoard(room1, players)
    assert len(updatedRoom3.players) == 2
    assert "Rayyan" in list(updatedRoom3.players.keys())


def testAddEnemiesToBoard():
    enemy1 = Enemy('test', (20, 20))
    updatedRoom = addEnemiesToBoard(room1, {"enemy1": enemy1})
    assert len(updatedRoom.enemies) == 1

    updatedRoom2 = addEnemiesToBoard(updatedRoom, enemies)
    assert len(updatedRoom2.enemies) == 4
    assert "The Mischievous Melonhead" in list(updatedRoom2.enemies.keys())


def testAddBoardToLevel():
    level = Level(keyLoc, exitLoc, [], False, "Saleha")
    updatedLevel = addBoardToLevel(level, room1)
    assert len(updatedLevel.boards) == 1
    assert len(level.boards) == 0
    assert updatedLevel.boards[0].boardType == BoardEnum.ROOM

    updatedLevel2 = addBoardToLevel(level, boards[0])
    updatedLevel2 = addBoardToLevel(updatedLevel2, boards[1])
    updatedLevel2 = addBoardToLevel(updatedLevel2, boards[2])
    updatedLevel2 = addBoardToLevel(updatedLevel2, boards[3])
    updatedLevel2 = addBoardToLevel(updatedLevel2, boards[4])
    assert len(updatedLevel2.boards) == 5
