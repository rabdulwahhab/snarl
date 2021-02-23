import pygame
import Colors
import Globals
from Util import getScreenLocation, logInFile, formatInitial
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
    x, y = getScreenLocation(tile.location)  # absolute
    log = logInFile("Render.py", "renderTile")
    log("Loc: ", str(tile.location), "PixelLoc: ", str((x, y)))
    tileRect = pygame.Rect(x, y, Globals.TILE_WIDTH, Globals.TILE_HEIGHT)
    tileColor = getTileColor(tile)
    pygame.draw.rect(background, tileColor, tileRect)
    if tile.hasKey:
        radius = Globals.TILE_WIDTH / 2
        pygame.draw.circle(background, Colors.KEY, tileRect.center, radius)


def renderEnemy(background: pygame.Surface, enemy: Enemy):
    x, y = getScreenLocation(enemy.location)
    tileRect = pygame.Rect(x, y, Globals.TILE_WIDTH, Globals.TILE_HEIGHT)
    # tileColor = Colors.ENEMY
    log = logInFile("Render.py", "renderEnemy")
    log(enemy.name)
    enemyLetter = Globals.FONT.render(formatInitial(enemy.name), True,
                                      Colors.WHITE)
    # pygame.draw.rect(background, tileColor, tileRect)
    background.blit(enemyLetter, tileRect.topleft)


def renderEnemies(background: pygame.Surface, enemies):
    log = logInFile("Render.py", "renderEnemies")
    log()
    for enemy in enemies:
        renderEnemy(background, enemy)


def renderPlayer(background: pygame.Surface, player: Player):
    x, y = getScreenLocation(player.location)
    tileRect = pygame.Rect(x, y, Globals.TILE_WIDTH, Globals.TILE_HEIGHT)
    # tileColor = Colors.PLAYER
    # TODO Fonts slow down the loading
    log = logInFile("Render.py", "renderPlayer")
    log(player.name)
    playerLetter = Globals.FONT.render(formatInitial(player.name), True,
                                       Colors.BLACK)  # TODO font color
    # pygame.draw.rect(background, tileColor, tileRect)
    background.blit(playerLetter, tileRect.topleft)


def renderPlayers(background: pygame.Surface, players: dict):
    log = logInFile("Render.py", "renderPlayers")
    log()
    playerNames = players.keys()
    for name in playerNames:
        player = players[name]
        renderPlayer(background, player)


def renderItem(background: pygame.Surface, item: Item):
    x, y = getScreenLocation(item.location)
    tileRect = pygame.Rect(x, y, Globals.TILE_WIDTH, Globals.TILE_HEIGHT)
    # tileColor = Colors.GROUND
    itemLetter = Globals.FONT.render(formatInitial(item.name), True,
                                     Colors.ITEM)
    # pygame.draw.rect(background, tileColor, tileRect)
    background.blit(itemLetter, tileRect.topleft)


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
    # renderPlayers(background, board.players)
    # renderEnemies(background, board.enemies)
    # renderItems(background, board.items)


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
    # TODO render entire level (including all boards)
    for board in level.boards:
        renderBoard(background, board)


def renderDungeon(background: pygame.Surface, dungeon: Dungeon):
    log = logInFile("Render.py", "renderDungeon")
    log()
    renderLevel(background, dungeon.levels[dungeon.currLevel],
                dungeon.currBoard)
