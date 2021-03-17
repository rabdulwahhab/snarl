import sys
import json
from Util import intifyTuple, whichBoardInLevel
from Types import *
from Convert import convertJsonLevel


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


def isTraversable(level: Level, currBoardIndex: int, givenPoint: tuple):
    currBoard = level.boards[currBoardIndex]
    # Check traversable
    for row in currBoard.tiles.keys():
        for col in currBoard.tiles[row].keys():
            tile = currBoard.tiles[row][col]
            if (row, col) == givenPoint:
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
