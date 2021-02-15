import Globals
import Util
from Types import *

# TODO Demo Level ---------------------

# Tiles
t1 = Tile(TileEnum.DOOR, (0, 0), False)
t2 = {'type': TileEnum.GRASS, 'location': (0, 1), 'hasKey': False}
t3 = {'type': TileEnum.WALL, 'location': (0, 2), 'hasKey': True}
t4 = {'type': TileEnum.DEFAULT, 'location': (1, 0), 'hasKey': False}
t5 = {'type': TileEnum.DEFAULT, 'location': (1, 1), 'hasKey': False}
t6 = {'type': TileEnum.WALL, 'location': (1, 2), 'hasKey': False}
t7 = {'type': TileEnum.DEFAULT, 'location': (2, 0), 'hasKey': False}
t8 = {'type': TileEnum.DEFAULT, 'location': (2, 1), 'hasKey': False}
t9 = {'type': TileEnum.WALL, 'location': (2, 2), 'hasKey': False}

# demoTiles = [t1, t2, t3, t4, t5, t6, t7, t8, t9]
#
# players = {}
# enemies = {}
# items = []
#
# board = {
#     'tiles':   demoTiles,
#     'type':    BoardEnum.ROOM,
#     'players': players,
#     'enemies': enemies,
#     'items':   items
# }
#
# level = {
#     'keyLocation':  (1, 0),
#     'exitLocation': (0, 0),
#     'boards':       [board],
#     'exitUnlocked': False,
#     'playerTurn':   0
# }


# ---------------------------

def createGenericRoomTiles():
    roomWidth = Globals.GAME_WIDTH
    roomHeight = Globals.GAME_HEIGHT
    roomTiles = []
    for i in range(roomWidth):
        for j in range(roomHeight):
            getsKey = True if i == 0 and j == 0 else False
            newTile = Tile(TileEnum.GRASS, (i, j), getsKey)
            roomTiles.append(newTile)
    return roomTiles


def createGenericRoom():
    boardType = BoardEnum.ROOM
    tiles = createGenericRoomTiles()
    player = Player("Saleha", (3, 3))
    enemy = Enemy("Big Monster", (2, 2))
    room = Board(tiles, boardType, {"Saleha": player}, [enemy], [])
    return room


def createGenericLevel():
    exitLocation = Util.genDoorCoords(Globals.GAME_WIDTH, Globals.GAME_HEIGHT)
    keyLocation = Util.genXRandCoords(1, {exitLocation})
    boards = [createGenericRoom()]
    level = Level(keyLocation, exitLocation, boards, False, 0)
    return level


def createGenericDungeon():
    name = "Super Generic Dungeon"
    level = createGenericLevel()
    dungeon = Dungeon(name, [level], ["Saleha"], 0, 0, False)
    return dungeon
