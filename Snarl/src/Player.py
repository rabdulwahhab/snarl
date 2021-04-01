from Types import *
from Util import locationInLevelBounds, getPlayer, whichBoardInLevel, log
from Convert import convertJsonPlayer, convertJsonEnemy
import GameManager
from more_itertools import first_true


def receivePlayerUpdate(update: dict, playerName: str):
    """
    Receive differences in game state and apply deltas to the given game view.
    :params update: dict (player-update)
    {
      "type": "player-update",
      "layout": (tile-layout),
      "position": (point),
      "objects": (object-list),
      "actors": (actor-position-list)
    }
    """
    position = update["position"]
    tiles = convertLayoutToTiles(update["layout"], position)
    players = [convertJsonPlayer(actorJson) for actorJson in update["actors"] if
               actorJson["type"] == "player"]
    enemies = [convertJsonEnemy(actorJson) for actorJson in update["actors"]
               if actorJson["type"] != "player"]

    keyObj = first_true(update["objects"],
                        pred=lambda obj: obj["type"] == "key")
    exitObj = first_true(update["objects"],
                         pred=lambda obj: obj["type"] == "exit")

    view = PlayerView(playerName, tiles, position, keyObj, exitObj, players,
                      enemies)
    return view


def convertLayoutToTiles(jsonLayout: dict, playerLocation: tuple):
    origin = (playerLocation[0] - 2, playerLocation[1] - 2)
    tiles = {}
    for row in range(len(jsonLayout)):
        for col in range(len(jsonLayout[row])):
            relRow, relCol = (origin[0] + row, origin[1] + col)
            tempColDict = {}
            if jsonLayout[row][col] == 2:
                tempColDict[relCol] = Tile(TileEnum.DOOR)
            elif jsonLayout[row][col] == 0:
                tempColDict[relCol] = Tile(TileEnum.WALL)
            else:
                tempColDict[relCol] = Tile(TileEnum.DEFAULT)

            if relRow in tiles.keys():
                tiles[relRow].update(tempColDict)
            else:
                tiles[relRow] = tempColDict
    return tiles


def makeMove(playerName: str, location: tuple, game: Dungeon):
    """
    Dispatch the move action to the game manager.

    For development, we are applying moves directly with the GameManager and
    simply returning the game because there isn't much else to do there.

    Ideally, this will send the move to the game manager over the network and
    receive the updates later (and also render). It would return success
    or failure.
    :params playerName: str
    :params location: tuple
    :params game: Dungeon (Remove in future)
    """
    # TODO in the future won't directly call this but use
    # network module to send
    game = GameManager.move(playerName, location, game)
    return game


def startGame(level):
    GameManager.startGame(level)
    return None


def joinGame(playerName, game: Dungeon):
    GameManager.addPlayer(playerName, game)
    return True


def whereAmI(view: PlayerView):
    return view.position


def getFieldOfView(playerName: str, level: Level):
    player: Player = getPlayer(level, playerName)
    pLocRow, pLocCol = player.location
    origin = (pLocRow - 2, pLocCol - 2)
    fieldOfView = []
    for r in range(5):
        for c in range(5):
            relLoc = (origin[0] + r, origin[1] + c)
            if locationInLevelBounds(level, relLoc):
                fieldOfView.append(relLoc)
    return fieldOfView


def getVisibleTiles(player: Player, level: Level):
    pLocRow, pLocCol = player.location
    origin = (pLocRow - 2, pLocCol - 2)
    fieldOfView = {}
    for r in range(5):
        fovRow = {}
        relRow = origin[0] + r
        for c in range(5):
            relCol = origin[1] + c
            relLoc = (relRow, relCol)
            if locationInLevelBounds(level, relLoc):
                boardNum = whichBoardInLevel(level, relLoc)
                tile = level.boards[boardNum].tiles[relRow][relCol]
                fovRow[relCol] = tile
        fieldOfView.update({relRow: fovRow})
    log("Got visible tiles", str(fieldOfView))
    return fieldOfView
