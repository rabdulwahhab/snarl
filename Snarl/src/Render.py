import pygame
import Colors
import Globals
from Util import getScreenLocation, logInFile, formatInitial
from Types import *


def getTileColor(tileType: TileEnum):
    if tileType == TileEnum.WALL:
        return Colors.WALL
    elif tileType == TileEnum.DOOR:
        return Colors.DOOR
    elif tileType == TileEnum.GRASS:
        return Colors.GRASS
    elif tileType == TileEnum.STAIR:
        return Colors.STAIR
    else:
        return Colors.GROUND


def renderTile(background: pygame.Surface, tileType: TileEnum, row: int,
               col: int, hasKey=False, hasExit=False):
    log = logInFile("Render.py", "renderTile")
    log(str(row), str(col))
    screenX, screenY = getScreenLocation((row, col))  # absolute location
    tileRect = pygame.Rect(screenX, screenY, Globals.TILE_WIDTH,
                           Globals.TILE_HEIGHT)
    tileColor = Colors.WHITE if hasExit else getTileColor(tileType)
    pygame.draw.rect(background, tileColor, tileRect)
    if hasKey:
        radius = Globals.TILE_WIDTH / 2
        pygame.draw.circle(background, Colors.KEY, tileRect.center, radius)


def renderEnemy(background: pygame.Surface, enemy: Enemy):
    x, y = getScreenLocation(enemy.location)
    tileRect = pygame.Rect(x, y, Globals.TILE_WIDTH, Globals.TILE_HEIGHT)
    # tileColor = Colors.ENEMY
    log = logInFile("Render.py", "renderEnemy")
    log(enemy.name)
    enemyLetter = Globals.FONT.render(formatInitial(enemy.name), True,
                                      Colors.ENEMY)
    # pygame.draw.rect(background, tileColor, tileRect)
    background.blit(enemyLetter, tileRect.topleft)


def renderEnemies(background: pygame.Surface, enemies: dict):
    log = logInFile("Render.py", "renderEnemies")
    log()
    enemyNames = enemies.keys()
    for name in enemyNames:
        enemy = enemies[name]
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


def renderBoard(background: pygame.Surface, board: Board, keyLoc: tuple,
                exitLoc: tuple):
    # FIXME only Rooms should render door tiles
    log = logInFile("Render.py", "renderBoard")
    log()
    for row in board.tiles.keys():
        for col in board.tiles[row].keys():
            tile = board.tiles[row][col]
            hasKey = (row, col) == keyLoc
            hasExit = (row, col) == exitLoc
            renderTile(background, tile.tileType, row, col, hasKey, hasExit)

    log("Players in board:", str(board.players))
    renderPlayers(background, board.players)
    renderEnemies(background, board.enemies)
    # renderItems(background, board.items)


def renderLevel(background: pygame.Surface, level: Level):
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
        renderBoard(background, board, level.keyLocation, level.exitLocation)


def renderDungeon(background: pygame.Surface, dungeon: Dungeon):
    log = logInFile("Render.py", "renderDungeon")
    log()
    renderLevel(background, dungeon.levels[dungeon.currLevel])
