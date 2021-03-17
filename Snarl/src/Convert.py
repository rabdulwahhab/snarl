from Types import *
from Util import intifyTuple, whichBoardInLevel, logInFile
from Create import addPlayersToBoard, addEnemiesToBoard

log = logInFile("Convert.py")

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
    tiles = dict()
    doorLocations = []
    for r in range(len(tileLayout)):
        relRow = r + upperLeftCorner[0]
        tempColDict = dict()
        for c in range(len(tileLayout[r])):
            relCol = c + upperLeftCorner[1]
            if tileLayout[r][c] == 0:
                tempColDict[relCol] = Tile(TileEnum.WALL)
            elif tileLayout[r][c] == 2:
                tempColDict[relCol] = Tile(TileEnum.DOOR)
                doorLocations.append((relRow, relCol))
            else:
                tempColDict[relCol] = Tile(TileEnum.DEFAULT)
        tiles[relRow] = tempColDict

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
    tiles = dict()
    while len(allWaypoints) > 0: # loop through all waypoints
        toTemp = allWaypoints[0] # current waypoint to segment
        fromRow, fromCol = intifyTuple(tuple(fromTemp)) # hallway beginning location
        toRow, toCol = intifyTuple(tuple(toTemp)) # hallway ending location
        # tempDict here
        if fromCol == toCol: # means we have a vertical segment
            toBigger = toRow > fromRow # means we are going visually down
            for i in range(0, abs(toRow - fromRow)): # for every row going down
                newTilePos = (fromRow + i, fromCol) if toBigger else (
                    fromRow - i, fromCol) # get the next location
                row, col = newTilePos
                if row in tiles.keys(): # if this row already exists in our tile representation
                    tiles[row].update({col: Tile(TileEnum.DEFAULT)}) # add a new tile at a column on that row
                else:
                    tiles[row] = {col: Tile(TileEnum.DEFAULT)} # create a row and add a tile at this column
            # add to temp
        elif fromRow == toRow: # means we have a horizontal segment
            tempColDict = dict()
            toBigger = toCol > fromCol
            for i in range(0, abs(toCol - fromCol)):
                newTilePos = (fromRow, fromCol + i) if toBigger else (
                    fromRow, fromCol - i)
                row, col = newTilePos
                tempColDict[col] = Tile(TileEnum.DEFAULT)

            if fromRow in tiles.keys():
                tiles[fromRow].update(tempColDict)
            else:
                tiles[fromRow] = tempColDict
        else:
            print(" YOU GAVE US A BAD LIST OF WAYPOINTS SIR")

        # add to tiles dict
        fromTemp = toTemp
        del allWaypoints[0]

    lastRow, lastCol = toPoint
    if lastRow in tiles.keys():
        tiles[lastRow].update({lastCol: Tile(TileEnum.DEFAULT)})
    else:
        tiles[lastRow] = {lastCol: Tile(TileEnum.DEFAULT)}

    # NOTE: origin = -1,-1 for a hallway
    board = Board(tiles, intifyTuple(tuple(fromPoint)), (-1, -1),
                  BoardEnum.HALLWAY,
                  [intifyTuple(tuple(fromPoint)), intifyTuple(tuple(toPoint))])
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


def convertJsonDungeon(jsonLevel: dict, jsonPlayers: list, jsonEnemies: list,
                       jsonExitLocked: bool):
    level: Level = convertJsonLevel(jsonLevel["rooms"], jsonLevel["hallways"],
                                    jsonLevel["objects"])
    level.exitUnlocked = not jsonExitLocked

    playerNames = []
    for player in jsonPlayers:
        # make player
        newPlayer = convertJsonPlayer(player)
        playerNames.append(newPlayer.name)
        playerDict = {newPlayer.name: newPlayer}
        playerBoard = whichBoardInLevel(level, newPlayer.location)
        level.boards[playerBoard] = addPlayersToBoard(level.boards[playerBoard],
                                                      playerDict)
    # Same for enemies
    enemyNames = []
    for enemy in jsonEnemies:
        newEnemy = convertJsonEnemy(enemy)
        enemyNames.append(newEnemy.name)
        enemyDict = {newEnemy.name: newEnemy}
        enemyBoard = whichBoardInLevel(level, newEnemy.location)
        level.boards[enemyBoard] = addEnemiesToBoard(level.boards[enemyBoard],
                                                     enemyDict)

    game = Dungeon([level], playerNames, 0, False)
    return game
