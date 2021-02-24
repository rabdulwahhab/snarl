from Move import moveEntity
from Create import createDungeon
from Types import *
from example2 import exampleLevel2, enemies


def testMovePlayer():
    saleha = Player("Saleha", (10, 10))
    dung = createDungeon(exampleLevel2, {saleha.name: saleha}, enemies)
    destination = (10, 12)

    level = moveEntity(dung.levels[dung.currLevel], "Saleha", 0, destination,
                       isPlayer=True)
    salehaMoved = level.boards[level.currBoard].players["Saleha"]
    assert salehaMoved.location == (10, 12)

    # room to room movement
    destination2 = (250, 100)
    prevBoard = 0
    landedBoard = 4
    assert level.currBoard == prevBoard
    level = moveEntity(dung.levels[dung.currLevel], "Saleha", 0, destination2,
                       isPlayer=True)
    assert level.currBoard == landedBoard
    assert "Saleha" in list(level.boards[landedBoard].players.keys())
    assert "Saleha" not in list(level.boards[prevBoard].players.keys())
    salehaMoved2 = level.boards[landedBoard].players["Saleha"]
    assert salehaMoved2.location == (250, 100)
