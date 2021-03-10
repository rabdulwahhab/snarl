from Types import *
from Create import createDungeon, addPlayersToBoard
from Move import moveEntity
from Rulechecker import playerPossibleCardinalMoves, \
    destHasEnemy, destHasItem, destHasKey, destHasExit, playerCanMoveTo
from Util import logInFile

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
    currLevel: Level = game.levels[game.currLevel]
    currBoardNum = currLevel.currBoard
    currBoard: Board = currLevel.boards[currBoardNum]
    player = currBoard.players[playerName]
    numMoves = 2
    if playerCanMoveTo(destination, player, currLevel, numMoves):
        log("player can move to!")
        updatedLevel = moveEntity(currLevel, playerName, currBoardNum,
                                  destination, isPlayer=True)
        game.levels[game.currLevel] = updatedLevel
        updatedGame = interact(playerName, destination, game)
        return updatedGame
    else:
        log("player CANNOT move to")
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
    currBoard: Board = currLevel.boards[currLevel.currBoard]

    if destHasEnemy(location, currBoard):
        return interactWithEnemy(playerName, location, game)
    elif destHasKey(location, currLevel):
        return interactWithKey(playerName, location, game)
    elif destHasExit(location, currLevel):
        return interactWithExit(playerName, location, game)
    # elif destHasItem(location, currBoard):
    #     # TODO implement interactWithItem
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
    currBoard: Board = currLevel.boards[currLevel.currBoard]
    for enemyName in currBoard.enemies.keys():
        enemy: Enemy = currBoard.enemies[enemyName]
        if location == enemy.location:  # fight!
            del currBoard.players[playerName]
            break
    return game


def interactWithKey(playerName: str, location: tuple, game: Dungeon):
    # TODO what about playerName??
    level = game.levels[game.currLevel]
    if level.keyLocation == location:
        level.exitUnlocked = True
    return game


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
    currBoard: Board = currLevel.boards[currLevel.currBoard]
    allPlayers = currBoard.players.copy()
    currBoard.players = {}
    nextLevel: Level = game.levels[nextLevelNum]
    nextBoard: Board = nextLevel.boards[nextLevel.currBoard]
    nextBoard.players = allPlayers
    # FIXME place players in different locations
    newLocations = []
    while len(newLocations) < len(allPlayers):
        firstDoorLoc = nextBoard.doorLocations[0]
        newLocations += playerPossibleCardinalMoves(firstDoorLoc, 1, nextLevel,
                                                    nextLevelNum)

    for playerName in allPlayers.keys():
        player: Player = game.players[playerName]
        player.location = newLocations.pop()

    return game


def interactWithExit(playerName: str, location: tuple, game: Dungeon):
    for level in game.levels:
        if location == level.exitLocation:
            if level.exitUnlocked:
                return advanceLevel(game)
    return game


def endGame(game: Dungeon):
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
    currLevel: Level = game.levels[game.currLevel]
    currBoard: Board = currLevel.boards[currLevel.currBoard]
    updatedBoard = addPlayersToBoard(currBoard, {player.name: player})
    game.levels[game.currLevel] = updatedBoard

    return game


def startGame(level: Level):
    # starting game on first room
    room: Board = level.boards[0]
    return createDungeon(level, room.players, room.enemies)
