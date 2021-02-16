import Globals
import Util
from Types import *
from random import randint

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

def createBoards(numBoards, dimensions):
    (levelWidth, levelHeight) = dimensions


def createPlayer(playerName, location):
    return Player(playerName, location)


def createLevel(numRooms, numHallways):
    numBoards = numRooms + numHallways
    maxLevelWidth = Globals.GAME_WIDTH * numBoards
    maxLevelHeight = Globals.GAME_HEIGHT * numBoards
    minLevelWidth = Globals.GAME_WIDTH * (numBoards - 1)
    minLevelHeight = Globals.GAME_HEIGHT * (numBoards - 1)
    levelWidth = randint(minLevelWidth, maxLevelWidth)
    levelHeight = randint(minLevelHeight, maxLevelHeight)
    # TODO key excluded locations (player, wall, door, etc.)
    keyLocation = Util.genXRandCoords(1, {(0, 0)}, (levelWidth, levelHeight))
    exitLocation = Util.genXRandCoords(1, {(0, 0), keyLocation},
                                       (levelWidth, levelHeight))
    rooms = createRooms(numRooms, (levelWidth, levelHeight))
    hallways = createHallways(numHallways, (levelWidth, levelHeight))

    return Level(keyLocation, exitLocation, boards, False, 0)


def createGenericRoomTiles():
    roomWidth = Globals.GAME_WIDTH
    roomHeight = Globals.GAME_HEIGHT
    doorLocation = (roomWidth - 1, roomHeight - 1)
    roomTiles = []
    for i in range(roomWidth):
        for j in range(roomHeight):
            getsKey = True if i == 0 and j == 0 else False  # TODO remove
            tileType = TileEnum.DOOR if (i,
                                         j) == doorLocation else TileEnum.DEFAULT
            newTile = Tile(tileType, (i, j), getsKey)
            roomTiles.append(newTile)
    return roomTiles


def createGenericRoom():
    boardType = BoardEnum.ROOM
    tiles = createGenericRoomTiles()
    player = Player("Saleha", (3, 3))
    enemy = Enemy("Big Monster", (2, 2))
    item = Item("Potion", (5, 1), False)
    room = Board(tiles, boardType, [(0, 0)], {"Saleha": player}, [enemy],
                 [item])
    return room


def createGenericLevel():
    exitLocation = Util.genDoorCoords(Globals.GAME_WIDTH, Globals.GAME_HEIGHT)
    keyLocation = Util.genXRandCoords(1, {exitLocation})
    boards = [createGenericRoom()]
    level = Level(keyLocation, exitLocation, boards, False, 0)
    return level


def createDungeon(playerName, numLevels):
    """
    Creates a Dungeon with numLevels and create the Player with playerName in
    the first level.
    :param playerName: Str
    :param numLevels: Int
    :return: Dungeon
    """
    # TODO numRooms and numHallways (random gen)
    levels = [createLevel(2, 1) for i in numLevels]
    players = [createPlayer(playerName)]
    dungeon = Dungeon(levels, players, 0, 0, False)
    return dungeon
