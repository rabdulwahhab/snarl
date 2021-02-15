import pygame
from Snarl.src.Enums import TileEnum
from Snarl.src.DevTools import logInFile
from Snarl.src.Util import Colors, Globals, getScreenLocation
from Snarl.src.Enums import *
from typing import Union


def getTileColor(tile: Tile):
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


def renderTile(background: pygame.Surface, tile):
    x, y = getScreenLocation(tile.location)
    tileRect = pygame.Rect(x, y, Globals.TILE_WIDTH, Globals.TILE_HEIGHT)
    tileColor = getTileColor(tile)
    pygame.draw.rect(background, tileColor, tileRect)


def renderCreature(background: pygame.Surface, creature: Union[Player, Enemy]):
    x, y = getScreenLocation(creature.location)
    tileRect = pygame.Rect(x, y, Globals.TILE_WIDTH, Globals.TILE_HEIGHT)
    tileColor = Colors.GROUND
    font = pygame.font.SysFont('courier', 14)
    font.render(creature.name[0], 1, Colors.ENEMY, tileRect)
    pygame.draw.rect(background, tileColor, tileRect)


def renderEnemies(background: pygame.Surface, enemies):
    for enemy in enemies:
        renderCreature(background, enemy)


def renderPlayers(background: pygame.Surface, players):
    playerNames = players.keys()
    for name in playerNames:
        player = players[name]
        renderCreature(background, player)


def renderItems(background: pygame.Surface, items):
    for item in items:
        if not item.hasBeenAcquired:
            renderItem(background, item)


def renderItem(background: pygame.Surface, item: Item):
    x, y = getScreenLocation(item.location)
    tileRect = pygame.Rect(x, y, Globals.TILE_WIDTH, Globals.TILE_HEIGHT)
    tileColor = Colors.GROUND
    font = pygame.font.SysFont('courier', 14)
    font.render("*", 1, Colors.ITEM, tileRect)
    pygame.draw.rect(background, tileColor, tileRect)


def renderBoard(background: pygame.Surface, board: Board):
    for tile in board.tiles:
        renderTile(background, tile)

    renderPlayers(background, board.players)
    renderEnemies(background, board.enemies)
    renderItems(background, board.items)


def renderLevel(background: pygame.Surface, level: Level, boardNumber):
    """
    Render the board in the level at the given board number onto the background.
    :param background:
    :param level:
    :param boardNumber:
    :return:
    """
    log = logInFile("Render.py", "renderLevel")
    log("")
    board = level.boards[boardNumber]
    renderBoard(background, board)


def renderDungeon(background: pygame.Surface, dungeon: Dungeon):
    renderLevel(background, dungeon.levels[dungeon.currLevel],
                dungeon.currBoard)
