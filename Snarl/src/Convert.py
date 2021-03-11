import json
from Types import *
from Util import log, intifyTuple, whichBoardInLevel
from Create import addPlayersToBoard, addEnemiesToBoard

"""
What a json room looks like: 
{ "type"   : "room",
  "origin" : (point),
  "bounds" : (boundary-data),
  "layout" : (tile-layout)
}
"""


def convertJsonPlayer(jsonPlayer: dict):
    newPlayer = Player(jsonPlayer["name"], intifyTuple(jsonPlayer["position"]))
    return newPlayer


def convertJsonEnemy(jsonEnemy: dict):
    newEnemy = Enemy(jsonEnemy["name"], intifyTuple(jsonEnemy["position"]))
    return newEnemy


def convertJsonRoom(origin: list, boundaryData: list, tileLayout: list):
    boardEnum = BoardEnum.ROOM
    dimensions = intifyTuple(tuple(boundaryData))
    upperLeftCorner = intifyTuple(tuple(origin))
    tiles = []
    doorLocations = []
    for i in range(len(tileLayout)):
        for j in range(len(tileLayout[i])):
            relX = i + upperLeftCorner[0]
            relY = j + upperLeftCorner[1]
            if tileLayout[i][j] == 0:
                temp = Tile(TileEnum.WALL, (relX, relY), False)
                tiles.append(temp)
            elif tileLayout[i][j] == 2:
                temp = Tile(TileEnum.DOOR, (relX, relY), False)
                tiles.append(temp)
                doorLocations.append((relX, relY))
            else:
                temp = Tile(TileEnum.DEFAULT, (relX, relY), False)
                tiles.append(temp)

    return Board(tiles, upperLeftCorner, dimensions, boardEnum,
                 doorLocations)


"""
What a json hallway looks like:
{ 
  "from": (point),
  "to": (point),
  "waypoints": (point-list)
}
"""


def convertJsonHallway(fromPoint: list, toPoint: list, waypoints: list):
    allWaypoints = waypoints + [toPoint]
    fromTemp = fromPoint
    tiles = []

    while len(allWaypoints) > 0:
        toTemp = allWaypoints[0]
        fromX, fromY = intifyTuple(tuple(fromTemp))
        toX, toY = intifyTuple(tuple(toTemp))
        if fromX == toX:
            toBigger = toY > fromY
            for i in range(0, abs(toY - fromY)):
                newTilePos = (fromX, fromY + i) if toBigger else (
                    fromX, fromY - i)
                newTile = Tile(TileEnum.DEFAULT, newTilePos)
                tiles.append(newTile)
        elif fromY == toY:
            toBigger = toX > fromX
            for i in range(0, abs(toX - fromX)):
                newTilePos = (fromX + i, fromY) if toBigger else (
                    fromX - i, fromY)
                newTile = Tile(TileEnum.DEFAULT, newTilePos)
                tiles.append(newTile)
        else:
            print(" YOU GAVE US A BAD LIST OF WAYPOINTS SIR")
        fromTemp = toTemp
        fromX, fromY = fromTemp
        del allWaypoints[0]

    tiles.append(Tile(TileEnum.DEFAULT, tuple(toPoint)))
    # NOTE: origin = -1,-1 for a hallway
    board = Board(tiles, intifyTuple(tuple(fromPoint)), (-1, -1),
                  BoardEnum.HALLWAY,
                  [intifyTuple(tuple(fromPoint)), intifyTuple(tuple(toPoint))])
    # for tile in board.tiles:
    #     log(str(tile.location))
    return board


"""
What a json level looks like:
{ 
  "rooms": (room-list),
  "hallways": (hall-list),
  "objects": [ { "type": "key", "position": (point) }, 
               { "type": "exit", "position": (point) } ]
}
"""


def convertJsonLevel(rooms: list, hallways: list, objects: list):
    boundsList = lambda boundaryData: [boundaryData["rows"],
                                       boundaryData["columns"]]
    roomBoards = [
        convertJsonRoom(room["origin"], boundsList(room["bounds"]),
                        room["layout"]) for room
        in rooms]
    hallwayBoards = [
        convertJsonHallway(hallway["from"], hallway["to"], hallway["waypoints"])
        for hallway in hallways]
    keyObj = list(filter(lambda obj: obj["type"] == "key", objects)).pop()
    exitObj = list(filter(lambda obj: obj["type"] == "exit", objects)).pop()
    keyLoc = intifyTuple(tuple(keyObj["position"]))
    exitLoc = intifyTuple(tuple(exitObj["position"]))
    return Level(keyLoc, exitLoc, roomBoards + hallwayBoards, False)


def convertJsonDungeon(jsonLevel: dict, jsonPlayers: list, jsonEnemies: list, jsonExitLocked: bool):
    level: Level = convertJsonLevel(jsonLevel["rooms"], jsonLevel["hallways"], jsonLevel["objects"])
    level.exitUnlocked = not jsonExitLocked

    playerNames = []
    for player in jsonPlayers:
        log("player is ", str(player))
        # make player
        newPlayer = convertJsonPlayer(player)
        playerNames.append(newPlayer.name)
        playerDict = {newPlayer.name : newPlayer}
        playerBoard = whichBoardInLevel(level, newPlayer.location)
        level.boards[playerBoard] = addPlayersToBoard(level.boards[playerBoard], playerDict)
    # Same for enemies
    enemyNames = []
    for enemy in jsonEnemies:
        newEnemy = convertJsonEnemy(enemy)
        enemyNames.append(newEnemy.name)
        enemyDict = {newEnemy.name : newEnemy}
        enemyBoard = whichBoardInLevel(level, newEnemy.location)
        level.boards[enemyBoard] = addEnemiesToBoard(level.boards[enemyBoard], enemyDict)

    game = Dungeon([level], playerNames, 0, False)
    return game


