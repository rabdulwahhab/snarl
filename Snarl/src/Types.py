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
    def __init__(self, name, levels, players, currLevel, currBoard, isGameOver):
        self.name = name
        self.levels = levels
        self.players = players
        self.currLevel = currLevel
        self.currBoard = currBoard
        self.isGameOver = isGameOver


class Level:
    def __init__(self, keyLocation, exitLocation, boards, exitUnlocked,
                 playerTurn):
        self.keyLocation = keyLocation
        self.exitLocation = exitLocation
        self.boards = boards
        self.exitUnlocked = exitUnlocked
        self.playerTurn = playerTurn


class Board:
    def __init__(self, tiles, boardType, players, enemies, items):
        self.tiles = tiles
        self.boardType = boardType
        self.players = players
        self.enemies = enemies
        self.items = items


class Tile:
    def __init__(self, tileType, location, hasKey):
        self.tileType = tileType
        self.location = location
        self.hasKey = hasKey


class Player:
    def __init__(self, name, location):
        self.name = name
        self.location = location
        self.health = None
        self.movePoints = None
        self.damageOutput = None
        self.inventory = None
        self.vision = None
        self.memory = None


class Enemy:
    def __init__(self, name, location):
        self.name = name
        self.location = location
        self.health = None
        self.damageOutput = None


class Item:
    def __init__(self, name, location, hasBeenAcquired):
        self.name = name
        self.location = location
        self.hasBeenAcquired = hasBeenAcquired
        self.effect = None
