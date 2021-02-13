import pygame
from pygame.locals import *
from Snarl.src.Enums import TileEnum, Colors
from Snarl.src.DevTools import logInFile


# pygame.init() to initalize all modules. inidividiual ones can be picked

def getTileColor(tile):
    if tile["type"] == TileEnum.WALL:
        return Colors.WALL
    elif tile["type"] == TileEnum.DOOR:
        return Colors.DOOR
    elif tile["type"] == TileEnum.GRASS:
        return Colors.GRASS
    elif tile["type"] == TileEnum.STAIR:
        return Colors.STAIR
    else:
        return Colors.GROUND


def renderLevel(background: pygame.Surface, level, boardNumber):
    """
    Render the board in the level at the given board number onto the background.
    :param background:
    :param level:
    :param boardNumber:
    :return:
    """
    log = logInFile("render.py", "renderLevel")

    board = level["boards"][boardNumber]
    boardTiles = board["tiles"]

    for tile in boardTiles:
        location = tile["location"]
        log(str(location))
        x, y = (location[0] * 50, location[1] * 50)
        tileRect = pygame.Rect(x, y, 50.0, 50.0)
        tileColor = getTileColor(tile)
        pygame.draw.rect(background, tileColor, tileRect)
