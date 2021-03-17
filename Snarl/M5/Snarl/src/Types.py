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
    def __init__(self, levels: list, players: list, currLevel: int,
                 isGameOver: bool):
        self.levels = levels
        self.players = players
        self.currLevel = currLevel
        self.isGameOver = isGameOver


class Level:
    def __init__(self, keyLocation: tuple, exitLocation: tuple, boards: list,
                 exitUnlocked: bool,
                 playerTurn=None):
        self.keyLocation = keyLocation
        self.exitLocation = exitLocation
        self.boards = boards
        self.exitUnlocked = exitUnlocked
        self.playerTurn = playerTurn
        self.currBoard = 0



class Board:
    def __init__(self, tiles: list, origin: tuple, dimensions: tuple,
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
        self.items = None


class Tile:
    def __init__(self, tileType: TileEnum, location: tuple, hasKey=False):
        self.tileType = tileType
        self.location = location  # not needed??
        self.hasKey = hasKey


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
    def __init__(self, name: str, location: tuple):
        self.name = name
        self.location = location
        self.health = None
        self.damageOutput = None


class Item:
    def __init__(self, name: str, location: tuple, hasBeenAcquired: bool):
        self.name = name
        self.location = location
        self.hasBeenAcquired = hasBeenAcquired
        self.effect = None
