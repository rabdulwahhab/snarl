# Demo game pieces and types

from Types import *

# Room 1 Tiles
r1tw1 = Tile(TileEnum.WALL, (0, 0), False)
r1tw2 = Tile(TileEnum.WALL, (1, 0), False)
r1tw3 = Tile(TileEnum.WALL, (2, 0), False)
r1tw4 = Tile(TileEnum.WALL, (3, 0), False)
r1tw5 = Tile(TileEnum.WALL, (4, 0), False)
r1tw6 = Tile(TileEnum.WALL, (0, 1), False)
r1tw7 = Tile(TileEnum.WALL, (0, 3), False)
r1tw8 = Tile(TileEnum.WALL, (0, 4), False)
r1tw9 = Tile(TileEnum.WALL, (1, 4), False)
r1tw10 = Tile(TileEnum.WALL, (2, 4), False)
r1tw11 = Tile(TileEnum.WALL, (3, 4), False)
r1tw12 = Tile(TileEnum.WALL, (4, 4), False)
r1tw13 = Tile(TileEnum.WALL, (0, 2), False)
r1tw14 = Tile(TileEnum.WALL, (4, 1), False)
r1tw15 = Tile(TileEnum.WALL, (4, 2), False)

r1t1 = Tile(TileEnum.DEFAULT, (3, 3), False)
r1t2 = Tile(TileEnum.DEFAULT, (1, 1), False)
r1t3 = Tile(TileEnum.DEFAULT, (1, 2), False)
r1t5 = Tile(TileEnum.GRASS, (1, 3), False)
r1t6 = Tile(TileEnum.DEFAULT, (2, 1), False)
r1t7 = Tile(TileEnum.DEFAULT, (2, 2), False)
r1t8 = Tile(TileEnum.GRASS, (2, 3), False)
r1t9 = Tile(TileEnum.GRASS, (3, 1), False)
r1t10 = Tile(TileEnum.DEFAULT, (3, 2), False)
r1t11 = Tile(TileEnum.DOOR, (4, 3), False)

room1Tiles = [r1tw1, r1tw2, r1tw3, r1tw4, r1tw5, r1tw6, r1tw7, r1tw8, r1tw9,
              r1tw10, r1tw11, r1tw12,
              r1tw13,
              r1tw14, r1tw15, r1t1, r1t2, r1t3, r1t5, r1t6, r1t7, r1t8, r1t9,
              r1t10, r1t11]

# Hallway Tiles
htw1 = Tile(TileEnum.WALL, (5, 2), False)
htw2 = Tile(TileEnum.WALL, (6, 2), False)
htw3 = Tile(TileEnum.WALL, (7, 2), False)
htw4 = Tile(TileEnum.WALL, (8, 2), False)
htw5 = Tile(TileEnum.WALL, (9, 2), False)
htw6 = Tile(TileEnum.WALL, (5, 4), False)
htw7 = Tile(TileEnum.WALL, (6, 4), False)
htw8 = Tile(TileEnum.WALL, (7, 4), False)
htw9 = Tile(TileEnum.WALL, (8, 4), False)
htw10 = Tile(TileEnum.WALL, (9, 4), False)

ht1 = Tile(TileEnum.DEFAULT, (5, 3), False)
ht2 = Tile(TileEnum.DEFAULT, (6, 3), False)
ht3 = Tile(TileEnum.DEFAULT, (7, 3), False)
ht4 = Tile(TileEnum.GRASS, (8, 3), False)
ht5 = Tile(TileEnum.DEFAULT, (9, 3), False)

hallwayTiles = [htw1, htw2, htw3, htw4, htw5, htw6, htw7, htw8, htw9, htw10,
                ht1, ht2, ht3, ht4, ht5]

# Room 2 Tiles
r2tw1 = Tile(TileEnum.WALL, (10, 0), False)
r2tw2 = Tile(TileEnum.WALL, (11, 0), False)
r2tw3 = Tile(TileEnum.WALL, (12, 0), False)
r2tw4 = Tile(TileEnum.WALL, (13, 0), False)
r2tw5 = Tile(TileEnum.WALL, (14, 0), False)
r2tw6 = Tile(TileEnum.WALL, (10, 1), False)
r2tw7 = Tile(TileEnum.WALL, (10, 3), False)
r2tw8 = Tile(TileEnum.WALL, (10, 4), False)
r2tw9 = Tile(TileEnum.WALL, (11, 4), False)
r2tw10 = Tile(TileEnum.WALL, (12, 4), False)
r2tw11 = Tile(TileEnum.WALL, (13, 4), False)
r2tw12 = Tile(TileEnum.WALL, (14, 4), False)
r2tw13 = Tile(TileEnum.WALL, (10, 2), False)
r2tw14 = Tile(TileEnum.WALL, (14, 1), False)
r2tw15 = Tile(TileEnum.WALL, (14, 2), False)
r2tw16 = Tile(TileEnum.WALL, (14, 3), False)

r2t1 = Tile(TileEnum.DEFAULT, (13, 3), False)
r2t2 = Tile(TileEnum.DEFAULT, (11, 1), False)
r2t3 = Tile(TileEnum.DEFAULT, (11, 2), False)
r2t5 = Tile(TileEnum.DEFAULT, (11, 3), False)
r2t6 = Tile(TileEnum.DEFAULT, (12, 1), False)
r2t7 = Tile(TileEnum.DEFAULT, (12, 2), False)
r2t8 = Tile(TileEnum.GRASS, (12, 3), False)
r2t9 = Tile(TileEnum.GRASS, (13, 1), False)
r2t10 = Tile(TileEnum.DEFAULT, (13, 2), True)
r2t11 = Tile(TileEnum.DOOR, (10, 3), False)

room2Tiles = [r2tw1, r2tw2, r2tw3, r2tw4, r2tw5, r2tw6, r2tw7, r2tw8, r2tw9,
              r2tw10, r2tw11, r2tw12,
              r2tw13,
              r2tw14, r2tw15, r2tw16, r2t1, r2t2, r2t3, r2t5, r2t6, r2t7, r2t8,
              r2t9,
              r2t10, r2t11]

room1 = Board(room1Tiles, (0, 0), (5, 5), BoardEnum.ROOM, [(4, 3)], {}, [], [])
hallway = Board(hallwayTiles, (5, 0), (5, 5), BoardEnum.HALLWAY, [], {}, [], [])
room2 = Board(room2Tiles, (10, 0), (5, 5), BoardEnum.ROOM, [(0, 3)], {}, [], [])

# Example level
exampleLevel = Level((13, 2), (1, 1), [room1, hallway, room2], False, 0)
