import sys
import json
from Util import intifyTuple, whichBoardInLevel
from Convert import convertJsonDungeon
from GameManager import *

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


# TODO
#  ☑︎make arbitraryMove function
#  ☑︎fix our exit thing (not ll players move on just 1 gets ejected)
#  ☑︎update main to take in state, name, point
#  ☑︎convert state to game
#    NOTE: here don't add players, add players in using addPlayersToBoard
#    yourself to place them on the right board
#  call move to update game state
#  if failure or ejection or exit => build output
#  else create new game state from game => build output
#  return output

def arbitraryMove(playerName: str, destination: tuple, game: Dungeon):
    """
    Updates the game to reflect the movement of a player if they
    can move to the given destination in the game. Returns an
    unmodified game if the player cannot move based on game rules.
    :param playerName: str
    :param destination: tuple
    :param game: Dungeon
    """
    currLevel: Level = game.levels[game.currLevel]
    currBoardNum = currLevel.currBoard
    currBoard: Board = currLevel.boards[currBoardNum]
    player = currBoard.players[playerName]
    if validMoveForHarness(destination, currLevel):
        updatedLevel = moveEntity(currLevel, playerName, currBoardNum,
                                  destination, isPlayer=True)
        game.levels[game.currLevel] = updatedLevel
        updatedGame = interact(playerName, destination, game)
        return updatedGame
    else:
        return game


def validMoveForHarness(destination: tuple, level: Level):
    boardNum = whichBoardInLevel(level, destination)
    if boardNum == -1:
        return False
    for tile in level.boards[boardNum]:
        if tile.location == destination:
            return tile.tileType is not TileEnum.WALL
    return False



def createDungeonFromInput(levels: list, players: list, enemies: list):
    return True


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
        game = convertJsonDungeon(jsonLevel, jsonPlayers, jsonEnemies, jsonExitLocked)


        print(json.dumps(output))
    except json.JSONDecodeError:
        print("Malformed input.")
        sys.exit(1)
    except KeyboardInterrupt:
        print("Exiting...")
        sys.exit(0)


if __name__ == '__main__':
    main()
