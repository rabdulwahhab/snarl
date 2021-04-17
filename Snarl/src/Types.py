from enum import Enum


class BoardEnum(Enum):
    ROOM = 1
    HALLWAY = 2


class TileEnum(Enum):
    DEFAULT = 1
    WALL = 2
    GRASS = 3
    DOOR = 4
    STAIR = 5


class Dungeon:
    def __init__(self,
                 levels: list,
                 players: list,
                 currLevel: int,
                 isGameOver: bool,
                 name="default"):
        self.levels = levels
        self.players = players
        self.currLevel = currLevel  # 0-indexed
        self.isGameOver = isGameOver
        self.name = name
        self.scores = {name: {'exits': 0, 'ejects': 0, 'keys': 0} for name in
                       players}


class Level:
    def __init__(self,
                 keyLocation: tuple,
                 exitLocation: tuple,
                 boards: list,
                 exitUnlocked: bool,
                 playerTurn=0,
                 enemyTurn=-1,
                 key="",
                 exits=[],
                 ejects=[]):
        self.keyLocation = keyLocation
        self.exitLocation = exitLocation
        self.boards = boards
        self.exitUnlocked = exitUnlocked
        self.playerTurn = playerTurn
        self.enemyTurn = enemyTurn
        self.currBoard = 0
        self.items = None
        self.key = key,
        self.exits = exits,
        self.ejects = ejects


class Board:
    def __init__(self, tiles: dict, origin: tuple, dimensions: tuple,
                 boardType: BoardEnum,
                 doorLocations: list, players={}, enemies={}):
        self.tiles = tiles
        self.origin = origin  # absolute location
        self.dimensions = dimensions  # (width, height)
        self.boardType = boardType
        # For hallways, indicates roomDoors it connects to
        self.doorLocations = doorLocations
        self.players = players
        self.enemies = enemies


class Tile:
    def __init__(self, tileType: TileEnum, items=[]):
        self.tileType = tileType
        self.items = items


class Player:
    def __init__(self, name: str, location: tuple):
        self.name = name
        self.location = location
        self.health = None
        self.movePoints = None
        self.damageOutput = None
        self.inventory = None
        self.vision = None
        self.memory = None


class Enemy:
    def __init__(self, name: str, location: tuple, enemyType="zombie"):
        self.name = name
        self.location = location
        self.enemyType = enemyType
        self.health = None
        self.damageOutput = None


class Item:
    def __init__(self, name: str, location: tuple, hasBeenAcquired: bool):
        self.name = name
        self.location = location
        self.hasBeenAcquired = hasBeenAcquired
        self.effect = None


class PlayerView:
    def __init__(self, name: str, tiles: dict, position: tuple, keys=[],
                 exits=[],
                 players=[], enemies=[]):
        self.name = name
        self.tiles = tiles  # 5x5 of tiles with absolute locations
        self.position = position
        self.keys = keys
        self.exits = exits
        self.players = players
        self.enemies = enemies


class ObserverView:
    def __init__(self, name: str, tiles: dict, keys=[], exits=[],
                 players=[], enemies=[], history=[]):
        self.name = name
        self.tiles = tiles  # all tiles with absolute locations
        self.keys = keys
        self.exits = exits
        self.players = players
        self.enemies = enemies
        self.history = history
