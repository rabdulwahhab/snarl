import sys
import json
from Util import intifyTuple, whichBoardInLevel, locationInLevelBounds, \
    isDoorLocation, isTraversable, isPlayerInGame, getPlayer, logInFile
from Convert import convertJsonDungeon
from Types import *
import GameManager
from Rulechecker import playerCanMoveTo, destHasKey, destHasExit, destHasEnemy, \
    isCurrentLevelOver
from more_itertools import first_true
from Player import getFieldOfView

log = logInFile("testManager.py")


def anyOutOfMoves(jsonActorMoveListList: list):
    for moveList in jsonActorMoveListList:
        if len(moveList) == 0:
            return True
    return False


def getTileType(location: tuple, game: Dungeon):
    """
    Return 0, 1, or 2 depending on what lies
    at the given location
    """
    if isDoorLocation(location, game):
        return 2
    elif isTraversable(location, game):
        return 1
    else:
        return 0


def getTileLayout(game: Dungeon, player: Player):
    layout = [[-1, -1, -1, -1, -1],
              [-1, -1, -1, -1, -1],
              [-1, -1, -1, -1, -1],
              [-1, -1, -1, -1, -1],
              [-1, -1, -1, -1, -1]]
    pRow, pCol = player.location
    origin = (pRow - 2, pCol - 2)
    for r in range(5):
        for c in range(5):
            relLoc = (origin[0] + r, origin[1] + c)
            layout[r][c] = getTileType(relLoc, game)
    return layout


def getEnemiesAroundPlayer(possMoves: list, game: Dungeon):
    acc = []
    for loc in possMoves:
        level: Level = game.levels[game.currLevel]
        boardNum = whichBoardInLevel(level, loc)
        if destHasEnemy(loc, level.boards[boardNum]):
            enemy: Enemy = first_true(level.boards[boardNum].enemies.values(),
                                      pred=lambda enem: enem.location == loc)
            acc.append({
                "type":     enemy.enemyType,
                "name":     enemy.name,
                "position": loc
            })
    return acc


def getObjectsAroundPlayer(possMoves: list, game: Dungeon):
    acc = []
    for loc in possMoves:
        level: Level = game.levels[game.currLevel]
        if destHasKey(loc, level):
            acc.append({"type": "key", "position": loc})
        elif destHasExit(loc, level):
            acc.append({"type": "exit", "position": loc})
    return acc


def getPlayerUpdate(playerName: str, game: Dungeon):
    """
    PlayerUpdateType is:
    {
      "type": "player-update",
      "layout": (tile-layout), # getLayout?
      "position": (point), # getPlayer.location
      "objects": (object-list), # getLocationsAround.map(if destHasItem || desthasKey -> return object)
        [ { "type": "key", "position": [ 4, 2 ] },
               { "type": "exit", "position": [ 7, 17 ] } ]
      "actors": (actor-position-list) # potentially getLocationsAround.map(if destHasEnemy -> return enemy)
    }

    1. Finds 25 points: surrounding 24 of given point
    2.Layput based on the 25 points
    3. Will check if enemies exist on any of those 25
    4. Will check if key or exit on any of those 25

    """
    player: Player = getPlayer(game.levels[game.currLevel], playerName)
    possMoves = getFieldOfView(player, game.levels[game.currLevel])
    output = [playerName,
              {"type":     "player-update",
               "layout":   getTileLayout(game, player),
               "position": [player.location[0], player.location[1]],
               "objects":  getObjectsAroundPlayer(possMoves, game),
               "actors":   getEnemiesAroundPlayer(possMoves, game)}]
    return output


def getPlayersUpdates(game, managerTrace):
    alivePlayers = [playerName for playerName in game.players if
                    isPlayerInGame(playerName, game)]
    for playerName in alivePlayers:
        update = getPlayerUpdate(playerName, game)
        managerTrace.append(update)
    return managerTrace


def getMoveStatus(currLevel: Level, playerName: str, move: dict):
    dest = intifyTuple(move["to"])
    if destHasKey(dest, currLevel):
        return [playerName, move, "Key"]
    elif destHasExit(dest, currLevel):
        return [playerName, move, "Exit"]
    elif destHasEnemy(dest,
                      currLevel.boards[whichBoardInLevel(currLevel, dest)]):
        return [playerName, move, "Eject"]
    else:
        return [playerName, move, "OK"]


def executeTurns(game: Dungeon, maxNumTurns: int, jsonActorMoveListList: list,
                 jsonNameList: list, jsonLevel: dict):
    # Send initial player updates to all players in game
    managerTrace = getPlayersUpdates(game, [])
    i = 0
    while i < maxNumTurns:
        # 0. Exit checking
        if anyOutOfMoves(jsonActorMoveListList) or isCurrentLevelOver(game):
            break
        # 1. Run all moves in turn
        for j in range(len(
                jsonActorMoveListList)):  # execute each move for a player in a turn
            playerMoveList = jsonActorMoveListList[j]
            validMove = False

            while not validMove and len(playerMoveList) > 0:
                # do first move in playerMoveList, if valid, set flag
                move = playerMoveList[0]
                playerName = jsonNameList[j]
                if not isPlayerInGame(playerName, game):
                    break

                currLevel: Level = game.levels[game.currLevel]
                player = getPlayer(currLevel, playerName)  # pot bug??
                dest = move["to"]
                # apply
                if not dest:  # skipped turn
                    validMove = True
                    managerTrace.append(
                        [playerName, move, "OK"])  # pot bug adding??
                    managerTrace = getPlayersUpdates(game, managerTrace)
                elif playerCanMoveTo(intifyTuple(dest), player, currLevel, 2):
                    GameManager.move(playerName, intifyTuple(dest),
                                     game)  # pot bug not mutating??
                    managerTrace.append(getMoveStatus(currLevel, playerName,
                                                      move))  # pot bug wrong return types??
                    managerTrace = getPlayersUpdates(game, managerTrace)
                    validMove = True
                else:
                    managerTrace.append([playerName, move, "Invalid"])
                    validMove = False

                del playerMoveList[0]

        i += 1
    return managerTrace, game


def getPlayerEnemyJson(jsonPlayerList: list, jsonPointList: list):
    """
    Will output a tuple of actor-position-lists representing players and enemies
    """
    jsonPlayers = []
    jsonEnemies = []
    numPlayers = len(jsonPlayerList)
    for i in range(0, len(jsonPointList)):
        if i < numPlayers:
            # Create a player actor type and append to jsonPlayers
            newPlayer = {"type":     "player", "name": jsonPlayerList[i],
                         "position": jsonPointList[i]}
            jsonPlayers.append(newPlayer)
        else:
            # Create an enemy actor type and append to jsonPlayers
            enemyName = "creature" + str(i - numPlayers + 1)
            newEnemy = {"type":     "zombie", "name": enemyName,
                        "position": jsonPointList[i]}
            jsonEnemies.append(newEnemy)
    return jsonPlayers, jsonEnemies


def getFinalState(game: Dungeon, jsonLevel: dict, jsonEnemies: list):
    players = []
    for playerName in game.players:

        if isPlayerInGame(playerName, game):
            player: Player = getPlayer(game.levels[game.currLevel], playerName)
            newPlayer = {"type":     "player", "name": playerName,
                         "position": player.location}
            players.append(newPlayer)
    exitLocked = not game.levels[game.currLevel].exitUnlocked
    return {
        "type":        "state", "level": jsonLevel, "players": players,
        "adversaries": jsonEnemies, "exit-locked": exitLocked}


def main():
    try:
        # Read input
        inputJson = sys.stdin.read()

        # Parse json
        parsedJson = json.loads(inputJson.replace("\n", ""))
        jsonNameList, jsonLevel, maxNumTurns, jsonPointList, jsonActorMoveListList = parsedJson

        # For converJsonDungeon we need: jsonLevel, jsonPlayers, c jsonEnemies, amd unlockedExit boolean
        # We have json level, and set jsonExitLocked as False
        # TODO: we need to iterate through jsonNameList and jsonPointList to create json Players and jsonEnemies,
        jsonPlayers, jsonEnemies = getPlayerEnemyJson(jsonNameList,
                                                      jsonPointList)
        game = convertJsonDungeon(jsonLevel, jsonPlayers, jsonEnemies, True)

        # 1. cal a MAJOR function that does the looping, returns manager-Trace and a game
        managerTrace, finalGame = executeTurns(game, maxNumTurns,
                                               jsonActorMoveListList,
                                               jsonNameList, jsonLevel)

        # 2. Using the game returned in 1 + original json, get the state of the game
        outputState = getFinalState(finalGame, jsonLevel, jsonEnemies)

        # 3. Append both, and output, cheers.
        output = [outputState, managerTrace]

        print(json.dumps(output))
    except json.JSONDecodeError:
        print("Malformed input.")
        sys.exit(1)
    except KeyboardInterrupt:
        print("Exiting...")
        sys.exit(0)


if __name__ == '__main__':
    main()
