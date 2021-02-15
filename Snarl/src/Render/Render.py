import pygame
from Snarl.src.Enums import TileEnum
from Snarl.src.DevTools import logInFile
from Snarl.src.Util import Colors, Globals


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
    log = logInFile("Render.py", "renderLevel")

    board = level["boards"][boardNumber]
    boardTiles = board["tiles"]

    for tile in boardTiles:
        location = tile["location"]
        log(str(location))
        x, y = (
            location[0] * Globals.TILE_WIDTH, location[1] * Globals.TILE_HEIGHT)
        tileRect = pygame.Rect(x, y, Globals.TILE_WIDTH, Globals.TILE_HEIGHT)
        tileColor = getTileColor(tile)
        # can use (x, y, width, height) tuple rather than rect
        pygame.draw.rect(background, tileColor, tileRect)
