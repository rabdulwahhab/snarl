from Types import *
from Create import createDungeon, addPlayersToBoard, removePlayersFromBoard
from Move import moveEntity
from Rulechecker import playerPossibleCardinalMoves, \
    destHasEnemy, destHasKey, destHasExit, playerCanMoveTo
from Util import whichBoardInLevel, logInFile, getPlayer


log = logInFile("GameManager.py")


def move(playerName: str, destination: tuple, game: Dungeon):
    """
    Updates the game to reflect the movement of a player if they
    can move to the given destination in the game. Returns an
    unmodified game if the player cannot move based on game rules.
    :param playerName: str
    :param destination: tuple
    :param game: Dungeon
    """
    log("Moving", playerName, "to", str(destination))
    currLevel: Level = game.levels[game.currLevel]
    player = getPlayer(currLevel, playerName)
    currBoardNum = whichBoardInLevel(currLevel, player.location)
    newBoardNum = whichBoardInLevel(currLevel, destination)
    numMoves = 2
    if playerCanMoveTo(destination, player, currLevel, numMoves):
        updatedLevel = moveEntity(currLevel, playerName, currBoardNum, newBoardNum,
                                  destination, isPlayer=True)
        game.levels[game.currLevel] = updatedLevel
        updatedGame = interact(playerName, destination, game)
        return updatedGame
    else:
        return game


def interact(playerName: str, location: tuple, game: Dungeon):
    """
    Updates the game to reflect a player's interaction with a location
    in the game.
    :param playerName: str
    :param location: tuple
    :param game: Dungeon
    """
    currLevel: Level = game.levels[game.currLevel]
    currBoardNum = whichBoardInLevel(currLevel, location)
    currBoard: Board = currLevel.boards[currBoardNum]

    if destHasEnemy(location, currBoard):
        return interactWithEnemy(playerName, location, game)
    elif destHasKey(location, currLevel):
        return interactWithKey(location, game)
    elif destHasExit(location, currLevel):
        return interactWithExit(playerName, location, game)
    # elif destHasItem(location, currBoard):
    #     TODO implement interactWithItem
    #     return game
    else:
        return game


def interactWithEnemy(playerName: str, location: tuple, game: Dungeon):
    """
    Calculates the consequence of a player interacting with an enemy
    and updates the state of the game.
    :param playerName: str
    :param location: tuple
    :param game: Dungeon
    """
    currLevel: Level = game.levels[game.currLevel]
    currBoardNum = whichBoardInLevel(currLevel, location)
    currBoard: Board = currLevel.boards[currBoardNum]
    for enemyName in currBoard.enemies.keys():
        enemy: Enemy = currBoard.enemies[enemyName]
        if location == enemy.location:  # fight!
            del currBoard.players[playerName]
            break
    return game


def interactWithKey(location: tuple, game: Dungeon):
    """
    Computes the resulting game state of a player acquiring a key in the
    level.
    :param location: tuple
    :param game: Dungeon
    """
    level = game.levels[game.currLevel]
    if level.keyLocation == location:
        level.exitUnlocked = True
    return game


def removePlayer(playerName: str, currBoardNum: int, game: Dungeon):
    """
    Removes the player from the level and returns the
    updated game.
    :param playerName: str
    :param currBoardNum: int
    :param game: Dungeon
    """
    currLevel: Level = game.levels[game.currLevel]
    currBoard: Board = currLevel.boards[currBoardNum]
    player = currBoard.players[playerName]
    updatedBoard = removePlayersFromBoard(currBoard, {playerName: player})
    currLevel.boards[currBoardNum] = updatedBoard
    return game


# TODO: look thru to make sure it still works as expected after advancePlayer adjustment
# FIXME: need to refactor for placing all players in the next level at sane locations
def advanceLevel(game: Dungeon):
    """
    Advances the game (Dungeon) to the next level (increments game's current
    level, moves players to first room of next level) and returns the
    updated game. If there are no levels remaining in the game to advance
    to, ends the game.
    :param game: Dungeon
    """
    nextLevelNum = game.currLevel + 1
    if nextLevelNum == len(game.levels):
        return endGame(game)

    game.currLevel = nextLevelNum
    currLevel: Level = game.levels[game.currLevel]
    # TODO is currBoard needed here???
    currBoard: Board = currLevel.boards[currLevel.currBoard]

    allPlayers = currBoard.players.copy()
    currBoard.players = {}
    nextLevel: Level = game.levels[nextLevelNum]
    nextBoard: Board = nextLevel.boards[nextLevel.currBoard]
    # TODO use addPlayerToBoard
    nextBoard.players = allPlayers
    # FIXME place players in different locations
    newLocations = []
    while len(newLocations) < len(allPlayers):
        firstDoorLoc = nextBoard.doorLocations[0]
        newLocations += playerPossibleCardinalMoves(firstDoorLoc, 1, nextLevel)

    for playerName in allPlayers.keys():
        player: Player = nextBoard.players[playerName]
        player.location = newLocations.pop()

    return game


def interactWithExit(playerName: str, location: tuple, game: Dungeon):
    """
    Computes the resulting game state of a player acquires an exit in the
    level.
    :param playerName: str
    :param location: tuple
    :param game: Dungeon
    """
    for level in game.levels:
        if location == level.exitLocation:
            if level.exitUnlocked:
                currBoardNum = whichBoardInLevel(level, location)
                currBoard: Board = level.boards[currBoardNum]
                if len(currBoard.players.values()) == 1:  # last player
                    # FIXME return advanceLevel(game)
                    return removePlayer(playerName, currBoardNum, game)
                else:
                    return removePlayer(playerName, currBoardNum, game)
    return game


def endGame(game: Dungeon):
    """
    Changes game to game over when the game has ended
    """
    game.isGameOver = True
    return game


def isValidPlayerName(game: Dungeon, name: str):
    """
    Determines if a name is already in use by another Player
    in the Dungeon.
    :param game: Dungeon
    :param name: Str
    """
    return name not in game.players


def addPlayer(player: Player, game: Dungeon):
    """
    Adds a new player to a game
    :param player: Player
    :param game: Dungeon
    """
    currLevel: Level = game.levels[game.currLevel]
    currBoardNum = whichBoardInLevel(currLevel, player.location)
    currBoard: Board = currLevel.boards[currBoardNum]
    updatedBoard = addPlayersToBoard(currBoard, {player.name: player})
    game.levels[game.currLevel] = updatedBoard

    return game


def startGame(level: Level):
    """
    Given a level, starts a new game at the first board in the level
    :param level: Level
    """
    room: Board = level.boards[0]
    return createDungeon(level, room.players, room.enemies)
