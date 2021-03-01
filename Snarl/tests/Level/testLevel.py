from Types import *
from Util import log, locationInBounds
from more_itertools import first_true

"""
Wishlist of Functions:
- ConvertJSONLevel (similar to convertJSONBoard)
--- Convert rooms (we have this for boards so we can use that)
--- Convert hallway (we wrote out the logic for this on the OneNote sheet)
- REACHABLE LOGIC!!!!
--- Big TODO
- What board are we on? (Level, Point) -> origin of board point is in


Once we have ocnverted to a level, out first couple outputs are easy:
- traversable: check tileType
- object: check point against key and exit locations
- type: check within boundaries of diff boards, at board index check type
--- For hallways, traverse tiles, for boards check origin + dimens for bounds
- reachable: BIG INTERESTING
--- Find which board we're in currently
--- If hallway:
----- Check doorLocations
----- Locate what board those locations are on
----- Get the origins of those boards/rooms and output
--- If room:
----- Check doorLocations
----- if room:
-------- add origin of that room
----- if hallway:
-------- Find what hallway connects to
-------- get origin of room of doorLocations of the hallway


"""


def whichBoardInLevel(level: Level, givenPoint: tuple):
    pointX = int(givenPoint[0])
    pointY = int(givenPoint[1])
    point = (pointX, pointY)
    for i in range(len(level.boards)):
        currBoard: Board = level.boards[i]
        if currBoard.boardType == BoardEnum.ROOM:
            if locationInBounds(point, currBoard.origin, currBoard.dimensions):
                return i
        else:
            hallwayTiles = currBoard.tiles
            if first_true(hallwayTiles, default=None,
                          pred=lambda tile: tile.location == point) is not None:
                return i
    return -1