from random import randint
from Snarl.src.Util import Globals
from Snarl.src.Util import utils
from Snarl.src.Enums.GamePieces import Level, Tile, Board, Dungeon, Enemy, Item, Player
from Snarl.src.Enums import BoardEnum, TileEnum

"""
tileType -> TileEnum
location -> (X, Y)

"""


def createRoomTiles():
    roomWidth = Globals.GAME_WIDTH - 1
    roomHeight = Globals.GAME_HEIGHT - 1
    roomTiles = []
    for i in roomWidth:
        for j in roomHeight:
            newTile = Tile(TileEnum.GRASS, (i, j))
            roomTiles.append(newTile)
    return roomTiles


def createGenericRoom():
    boardType = BoardEnum.ROOM
    tiles = createRoomTiles()
    room = Board(tiles, boardType, {}, [], [])
    return room


def createGenericLevel():
    exitLocation = utils.genDoorCoords()
    keyLocation = utils.genXRandCoords(1, {exitLocation})
    boards = createGenericRoom()
    level = Level(keyLocation, exitLocation, boards, False, 0)
    return level


def createDungeion():
    level= createGenericLevel()
