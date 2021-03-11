import sys
import json
from Util import intifyTuple, whichBoardInLevel
from Convert import convertJsonDungeon
from Types import *
from Rulechecker import destHasPlayer, destHasKey, destHasEnemy
from enum import Enum


class MoveStatus(Enum):
    NONE = 1
    SUCCESS = 2
    EJECTED = 3
    EXITED = 4
    KEY = 5
    PLAYERINVALID = 6
    DESTINVALID = 7


def arbitraryMove(destination: tuple, game: Dungeon):
    """
    Updates the game to reflect the movement of a player if they
    can move to the given destination in the game. Returns an
    unmodified game if the player cannot move based on game rules.
    :param destination: tuple
    :param game: Dungeon
    """
    status = MoveStatus.NONE
    currLevel: Level = game.levels[game.currLevel]
    if validMoveForHarness(destination, currLevel):
        return status
    else:
        status = MoveStatus.DESTINVALID
        return status


def validMoveForHarness(destination: tuple, level: Level):
    boardNum = whichBoardInLevel(level, destination)
    if boardNum == -1:
        return False
    if destHasPlayer(destination, level.boards[boardNum]):
        return False
    for tile in level.boards[boardNum].tiles:
        if tile.location == destination:
            return tile.tileType is not TileEnum.WALL
    return False


def getSuccessStatus(destination: tuple, initGame: Dungeon):
    level: Level = initGame.levels[0]
    destBoard = whichBoardInLevel(level, destination)
    # 1. exit
    if level.exitUnlocked and level.exitLocation == destination:
        status = MoveStatus.EXITED
    # 2. ejected
    elif destHasEnemy(destination, level.boards[destBoard]):
        status = MoveStatus.EJECTED
    elif destHasKey(destination, level):
        status = MoveStatus.KEY
    # 3. Success
    else:
        status = MoveStatus.SUCCESS
    return status


def buildOutput(status: MoveStatus, playerName: str, jsonPoint: list,
                jsonDungeon: dict):
    playerIndex = -1
    for i in range(len(jsonDungeon["players"])):
        if jsonDungeon["players"][i]["name"] == playerName:
            playerIndex = i
            break
    if status == MoveStatus.PLAYERINVALID:
        # Do the player output AND RETURN
        return ["Failure", "Player ", playerName, " is not a part of the game."]
    elif status == MoveStatus.DESTINVALID:
        # Do the dest output and RETURN
        return ["Failure", "The destination position ", jsonPoint,
                " is invalid."]
    elif status == MoveStatus.KEY:
        # Create output + state and RETURN
        jsonDungeon["players"][playerIndex]["position"] = jsonPoint
        jsonDungeon["exit-locked"] = False
        return ["Success", jsonDungeon]
    elif status == MoveStatus.SUCCESS:
        # Create output + state and RETURN
        jsonDungeon["players"][playerIndex]["position"] = jsonPoint
        return ["Success", jsonDungeon]
    else:
        del jsonDungeon["players"][playerIndex]
        if status == MoveStatus.EXITED:
            # Create output + state and RETURN
            return ["Success", "Player ", playerName, " exited.", jsonDungeon]
        elif status == MoveStatus.EJECTED:
            # Create output + state and RETURN
            return ["Success", "Player ", playerName, " was ejected.",
                    jsonDungeon]


def main():
    try:
        # Read input
        inputJson = sys.stdin.read()

        # Parse json
        parsedJson = json.loads(inputJson.replace("\n", ""))
        jsonDungeon, playerName, jsonPoint = parsedJson
        jsonLevel = jsonDungeon["level"]
        jsonPlayers = jsonDungeon["players"]
        jsonEnemies = jsonDungeon["adversaries"]
        jsonExitLocked = jsonDungeon["exit-locked"]
        game = convertJsonDungeon(jsonLevel, jsonPlayers, jsonEnemies,
                                  jsonExitLocked)

        # Validate
        if playerName not in game.players:
            status = MoveStatus.PLAYERINVALID
        else:
            status = arbitraryMove(intifyTuple(jsonPoint), game)
            if status == status.NONE:
                status = getSuccessStatus(intifyTuple(jsonPoint), game)

        # Output
        output = buildOutput(status, playerName, jsonPoint, jsonDungeon)
        print(json.dumps(output))
    except json.JSONDecodeError:
        print("Malformed input.")
        sys.exit(1)
    except KeyboardInterrupt:
        print("Exiting...")
        sys.exit(0)


if __name__ == '__main__':
    main()
