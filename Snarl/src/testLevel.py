import sys
import json
from Util import log, locationInBounds, intifyTuple
from Types import *
from more_itertools import first_true
from Convert import convertJsonLevel

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
------- Check if each doorLoc is in a hallways doorLoc. 
----------If yes, check that hallways doorLocs
----------Check those doorLocs room and get origin
----------Add origin to reachable

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


"""
- reachable: BIG INTERESTING
--- Find which board we're in currently
--- If hallway:
----- Check doorLocations
----- Locate what board those locations are on
----- Get the origins of those boards/rooms and output
--- If room:
----- Check doorLocations
------- Check if each doorLoc is in a hallways doorLoc. 
----------If yes, check that hallways doorLocs
----------Check those doorLocs room and get origin
----------Add origin to reachable
"""


def reachableRoomOrigins(level: Level, currBoardIndex: int):
    reachable = []
    givenRoom: Board = level.boards[currBoardIndex]
    if givenRoom.boardType == BoardEnum.HALLWAY:
        for connection in givenRoom.doorLocations:
            connIndex = whichBoardInLevel(level, connection)
            reachable.append(level.boards[connIndex].origin)
    else:
        for connection in givenRoom.doorLocations:
            for board in level.boards:
                if (board.boardType == BoardEnum.HALLWAY) and (
                        connection in board.doorLocations):
                    for loc in board.doorLocations:
                        if loc != connection:
                            connIndex = whichBoardInLevel(level, loc)
                            if level.boards[connIndex].origin not in reachable:
                                reachable.append(level.boards[connIndex].origin)
    return reachable







def isSelfReachableHallway(level: Level, hallwayIndex: int):
    selfIndex = 0
    board = level.boards[hallwayIndex]
    for location in board.doorLocations:
        currIndex = whichBoardInLevel(level, location)
        if currIndex == hallwayIndex:
            selfIndex += 1
    return selfIndex >= 2


def isTraversable(level: Level, currBoardIndex: int, givenPoint: tuple):
    currBoard = level.boards[currBoardIndex]
    # Check traversable
    for tile in currBoard.tiles:
        if tile.location == givenPoint:
            return tile.tileType != TileEnum.WALL
    return True


def objectOutput(objects: list, givenPoint: tuple):
    for entry in objects:
        if intifyTuple(tuple(entry['position'])) == givenPoint:
            return entry['type']
    return None


def typeOutput(level: Level, boardIndex: int):
    boardType = level.boards[boardIndex].boardType
    if boardType == BoardEnum.ROOM:
        return "room"
    elif boardType == BoardEnum.HALLWAY:
        return "hallway"
    else:
        return "void"


"""
Shape of output:
{
  "traversable": (boolean),
  "object": (maybe-object-type),
  "type": (room-or-hallway-or-void),
  "reachable": (point-list)
}
"""


def main():
    output = {}
    try:
        inputJson = sys.stdin.read()
        parsedJson = json.loads(inputJson.replace("\n", ""))
        jsonLevel, jsonPoint = parsedJson
        givenPoint = intifyTuple(tuple(jsonPoint))
        rooms = jsonLevel["rooms"]
        hallways = jsonLevel["hallways"]
        objects = jsonLevel["objects"]
        level = convertJsonLevel(rooms, hallways, objects)
        currentRoom = whichBoardInLevel(level, givenPoint)
        if currentRoom != -1:
            outputTraversable = isTraversable(level, currentRoom, givenPoint)
            outputObject = objectOutput(objects, givenPoint)
            outputType = typeOutput(level, currentRoom)
            outputReachable = reachableRoomOrigins(level, currentRoom)
        else:
            outputTraversable = False
            outputObject = None
            outputType = 'void'
            outputReachable = []
        output['traversable'] = outputTraversable
        output['object'] = outputObject
        output['type'] = outputType
        output['reachable'] = outputReachable

        print(json.dumps(output))
    except json.JSONDecodeError:
        print("Malformed input.")
        sys.exit(1)
    except KeyboardInterrupt:
        print("Exiting...")
        sys.exit(0)


if __name__ == '__main__':
    main()
