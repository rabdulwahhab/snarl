class Dungeon:
    def __init__(self, name, levels, players, currLevel, currRoom, isGameOver):
        self.name = name
        self.levels = levels
        self.players = players
        self.currLevel = currLevel
        self.currRoom = currRoom
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
    def __init__(self, tiles, type, players, enemies, items):
        self.tiles = tiles
        self.type = type
        self.players = players
        self.enemies = enemies
        self.items = items


class Tile:
    def __init__(self, type, location):
        self.type = type
        self.location = location


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
