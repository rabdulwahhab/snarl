import sys
import json
from Util import intifyTuple, whichBoardInLevel, logInFile
from Convert import convertJsonDungeon
from Types import  *
from Rulechecker import destHasPlayer, destHasKey, destHasExit, destHasEnemy
from enum import Enum

log = logInFile("testState.py")

"""
Cases:
- valid move
- move to an exit (locked)
- move to an exit (unlocked)
- move to player spot
- move to key
- move with unknown player
- move with dest invalid (wall or in the void)
- leap
"""

class MoveStatus(Enum):
    NONE = 1
    SUCCESS = 2
    EJECTED = 3
    EXITED = 4
    KEY = 5
    PLAYERINVALID = 6
    DESTINVALID = 7


def arbitraryMove(destination: tuple, playerName: str, game: Dungeon):
    """
    Updates the game to reflect the movement of a player if they
    can move to the given destination in the game. Returns an
    unmodified game if the player cannot move based on game rules.
    :param playerName: str
    :param destination: tuple
    :param game: Dungeon
    """
    status = MoveStatus.NONE
    currLevel: Level = game.levels[game.currLevel]
    currBoardNum = currLevel.currBoard
    currBoard: Board = currLevel.boards[currBoardNum]
    if validMoveForHarness(destination, currLevel):
        log("valid move!!")
        return status
    else:
        log("invalid move :(")
        status = MoveStatus.DESTINVALID
        return status


def validMoveForHarness(destination: tuple, level: Level):
    log("destination is -->", str(destination))
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
        # CREATE STATE where player is removed
        del jsonDungeon["players"][playerIndex]
        if status == MoveStatus.EXITED:
            # Create output + state and RETURN
            return ["Success", "Player ", playerName, " exited.", jsonDungeon]
        elif status == MoveStatus.EJECTED:
            # Create output + state and RETURN
            return ["Success", "Player ", playerName, " was ejected.",
                    jsonDungeon]


def main():
    output = {}
    try:
        # Read input
        inputJson = sys.stdin.read()

        # Parse json
        parsedJson = json.loads(inputJson.replace("\n", ""))
        jsonDungeon, playerName, jsonPoint = parsedJson
        givenPoint = intifyTuple(tuple(jsonPoint))
        jsonLevel = jsonDungeon["level"]
        jsonPlayers = jsonDungeon["players"]
        jsonEnemies = jsonDungeon["adversaries"]
        jsonExitLocked = jsonDungeon["exit-locked"]
        game = convertJsonDungeon(jsonLevel, jsonPlayers, jsonEnemies,
                                  jsonExitLocked)
        log("Game players are: ", str(game.players))
        log("Level board 0 players are", str(game.levels[0].boards[0].players))
        log("Level board 1 players are", str(game.levels[0].boards[1].players))
        # Failure: Player not in game or tile not traversable/invalid
        # Success: player ejected, player exited, normal
        if playerName not in game.players:
            status = MoveStatus.PLAYERINVALID
        else:
            log("Calling arbitrary move")
            status = arbitraryMove(intifyTuple(jsonPoint), playerName,
                                           game)
            # result = arbitraryMove(playerName, intifyTuple(jsonPoint), game)
            # status = getStatus(initGame, result)
            if status == status.NONE:
                status = getSuccessStatus(intifyTuple(jsonPoint), game)


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
