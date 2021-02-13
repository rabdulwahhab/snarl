# This is a hard-coded level for demonstration purposes. Enjoy

from Snarl.src.Enums import TileEnum, BoardEnum

# Tiles
t1 = {'type': TileEnum.DOOR, 'location': (0, 0), 'hasKey': False}
t2 = {'type': TileEnum.GRASS, 'location': (0, 1), 'hasKey': False}
t3 = {'type': TileEnum.WALL, 'location': (0, 2), 'hasKey': True}
t4 = {'type': TileEnum.DEFAULT, 'location': (1, 0), 'hasKey': False}
t5 = {'type': TileEnum.DEFAULT, 'location': (1, 1), 'hasKey': False}
t6 = {'type': TileEnum.WALL, 'location': (1, 2), 'hasKey': False}
t7 = {'type': TileEnum.DEFAULT, 'location': (2, 0), 'hasKey': False}
t8 = {'type': TileEnum.DEFAULT, 'location': (2, 1), 'hasKey': False}
t9 = {'type': TileEnum.WALL, 'location': (2, 2), 'hasKey': False}


tiles = [t1, t2, t3, t4, t5, t6, t7, t8, t9]

players = {}
enemies = {}
items = []

board = {
    'tiles':   tiles,
    'type':    BoardEnum.ROOM,
    'players': players,
    'enemies': enemies,
    'items':   items
}

level = {
    'keyLocation':  (1, 0),
    'exitLocation': (0, 0),
    'boards':       [board],
    'exitUnlocked': False,
    'playerTurn':   0
}




