import pygame
import Colors
import Globals
from Util import getScreenLocation, logInFile
from Types import *


def getTileColor(tile: Tile):
    if tile.tileType == TileEnum.WALL:
        return Colors.WALL
    elif tile.tileType == TileEnum.DOOR:
        return Colors.DOOR
    elif tile.tileType == TileEnum.GRASS:
        return Colors.GRASS
    elif tile.tileType == TileEnum.STAIR:
        return Colors.STAIR
    else:
        return Colors.GROUND


def renderTile(background: pygame.Surface, tile):
    x, y = getScreenLocation(tile.location)
    tileRect = pygame.Rect(x, y, Globals.TILE_WIDTH, Globals.TILE_HEIGHT)
    tileColor = getTileColor(tile)
    pygame.draw.rect(background, tileColor, tileRect)
    if tile.hasKey:
        radius = Globals.TILE_WIDTH / 2
        pygame.draw.circle(background, Colors.KEY, tileRect.center, radius)


def renderEnemy(background: pygame.Surface, enemy: Enemy):
    x, y = getScreenLocation(enemy.location)
    tileRect = pygame.Rect(x, y, Globals.TILE_WIDTH, Globals.TILE_HEIGHT)
    tileColor = Colors.ENEMY
    # TODO fonts slow
    # font = pygame.font.SysFont('courier', 12)
    log = logInFile("Render.py", "renderEnemy")
    log(enemy.name)
    # enemyLetter = font.render(enemy.name[0], False, tileColor)
    pygame.draw.rect(background, tileColor, tileRect)
    # background.blit(enemyLetter, tileRect.center)


def renderEnemies(background: pygame.Surface, enemies):
    log = logInFile("Render.py", "renderEnemies")
    log()
    for enemy in enemies:
        renderEnemy(background, enemy)


def renderPlayer(background: pygame.Surface, player: Player):
    x, y = getScreenLocation(player.location)
    tileRect = pygame.Rect(x, y, Globals.TILE_WIDTH, Globals.TILE_HEIGHT)
    tileColor = Colors.PLAYER
    # TODO Fonts slow down the loading significantly
    # font = pygame.font.SysFont('arial', Globals.TILE_WIDTH)
    log = logInFile("Render.py", "renderPlayer")
    log(player.name)
    # playerLetter = font.render(player.name[0], True, (0, 0, 0)) # TODO font color
    pygame.draw.rect(background, tileColor, tileRect)
    # background.blit(playerLetter, tileRect.center)


def renderPlayers(background: pygame.Surface, players):
    log = logInFile("Render.py", "renderPlayers")
    log()
    playerNames = players.keys()
    for name in playerNames:
        player = players[name]
        renderPlayer(background, player)


def renderItem(background: pygame.Surface, item: Item):
    x, y = getScreenLocation(item.location)
    tileRect = pygame.Rect(x, y, Globals.TILE_WIDTH, Globals.TILE_HEIGHT)
    tileColor = Colors.GROUND
    font = pygame.font.SysFont('courier', 12)
    font.render("*", False, Colors.ITEM)
    pygame.draw.rect(background, tileColor, tileRect)


def renderItems(background: pygame.Surface, items):
    log = logInFile("Render.py", "renderItems")
    log()
    for item in items:
        if not item.hasBeenAcquired:
            renderItem(background, item)


def renderBoard(background: pygame.Surface, board: Board):
    log = logInFile("Render.py", "renderBoard")
    log()
    for tile in board.tiles:
        renderTile(background, tile)

    log(str(board.players))
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
    log()
    board = level.boards[boardNumber]
    renderBoard(background, board)


def renderDungeon(background: pygame.Surface, dungeon: Dungeon):
    log = logInFile("Render.py", "renderDungeon")
    log()
    renderLevel(background, dungeon.levels[dungeon.currLevel],
                dungeon.currBoard)
