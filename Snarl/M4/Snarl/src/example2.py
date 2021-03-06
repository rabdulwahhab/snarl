# Example level 2

from Create import createGenericBoardTiles, createLevel, addPlayersToBoard, \
    addEnemiesToBoard
from Types import *

keyLoc = (320, 200)
exitLoc = (360, 240)

r1orig = (10, 0)
r1dim = (90, 180)
r1doors = [(99, 52)]
room1Tiles = createGenericBoardTiles(r1dim, r1orig, r1doors)
room1 = Board(room1Tiles, r1orig, r1dim, BoardEnum.ROOM, r1doors)

r2orig = (140, 45)
r2dim = (40, 100)
r2doors = [(141, 52), (181, 72)]
room2Tiles = createGenericBoardTiles(r2dim, r2orig, r2doors)
room2 = Board(room2Tiles, r2orig, r2dim, BoardEnum.ROOM, r2doors)

r3orig = (220, 50)
r3dim = (160, 100)
r3doors = [(219, 72), exitLoc]
room3Tiles = createGenericBoardTiles(r3dim, r3orig, r3doors, keyLoc)
room3 = Board(room3Tiles, r3orig, r3dim, BoardEnum.ROOM, r3doors)

h1orig = (100, 50)
h1dim = (40, 3)
h1doors = [(99, 52), (141, 52)]
hall1Tiles = createGenericBoardTiles(h1dim, h1orig, h1doors)
hallway1 = Board(hall1Tiles, h1orig, h1dim, BoardEnum.HALLWAY, h1doors)

h2orig = (180, 70)
h2dim = (40, 3)
h2doors = [(181, 72), (219, 72)]
hall2Tiles = createGenericBoardTiles(h2dim, h2orig, h2doors)
hallway2 = Board(hall2Tiles, h2orig, h2dim, BoardEnum.HALLWAY, h2doors)

player1 = Player("Saleha", (11, 1))
player2 = Player("Rayyan", (12, 1))
enemy1 = Enemy("Green man", (221, 51))
enemy2 = Enemy("The Mischievous Melonhead", (222, 51))
enemy3 = Enemy("a hyena", (223, 51))

boards = [room1, hallway1, room2, hallway2, room3]
players = {"Saleha": player1, "Rayyan": player2}
enemies = {"Green man": enemy1, "The Mischievous Melonhead": enemy2,
           "a hyena":   enemy3}

exampleLevel2 = createLevel(keyLoc, exitLoc, boards)
