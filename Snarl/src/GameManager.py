from Types import *
from Create import createDungeon, addPlayersToBoard, removePlayersFromBoard
from Move import moveEntity
from Rulechecker import destHasEnemy, destHasKey, destHasExit, playerCanMoveTo
from Util import whichBoardInLevel, logInFile, getPlayer, genXRandCoords, \
    getRandomRoomInLevel, getPlayersInLevel, getEnemy

log = logInFile("GameManager.py")


def move(entityName: str, destination: tuple, game: Dungeon, isPlayer=True):
    """
    Updates the game to reflect the movement of a player if they
    can move to the given destination in the game. Returns an
    unmodified game if the player cannot move based on game rules.
    :param entityName: str
    :param destination: tuple
    :param game: Dungeon
    """
    currLevel: Level = game.levels[game.currLevel]
    entity = getPlayer(currLevel, entityName) if isPlayer else getEnemy(
        currLevel, entityName)
    currBoardNum = whichBoardInLevel(currLevel, entity.location)
    newBoardNum = whichBoardInLevel(currLevel, destination)
    numMoves = 2
    if isPlayer and playerCanMoveTo(destination, entity, currLevel, numMoves):
        updatedLevel = moveEntity(currLevel, entityName, currBoardNum,
                                  newBoardNum,
                                  destination, isPlayer=True)
        if updatedLevel.playerTurn == len(game.players) - 1:
            updatedLevel.playerTurn = 0
        else:
            updatedLevel.playerTurn = updatedLevel.playerTurn + 1
        game.levels[game.currLevel] = updatedLevel
        updatedGame = interact(entityName, destination, game)
        return updatedGame
    elif not isPlayer:
        updatedLevel = moveEntity(currLevel, entityName, currBoardNum,
                                  newBoardNum, destination, isPlayer=False)
        game.levels[game.currLevel] = updatedLevel
        updatedGame = enemyInteract(game)
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


# TODO
def enemyInteract(game: Dungeon):
    return game

# TODO
def interactWithPlayer():
    return None

# TODO
def interactWithWall():
    return None
# TODO: in rulechecker add destHasWall


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


def advanceLevel(game: Dungeon):
    """
    Advances the game (Dungeon) to the next level (increments game's current
    level, moves players to a random room of next level) and returns the
    updated game. If there are no levels remaining in the game to advance
    to, ends the game.
    :param game: Dungeon
    """
    log("Advancing level")
    nextLevelNum = game.currLevel + 1
    if nextLevelNum == len(game.levels):
        return endGame(game)

    game.currLevel = nextLevelNum
    nextLevel: Level = game.levels[nextLevelNum]
    numPlayers = len(game.players)
    forbidden = [nextLevel.keyLocation, nextLevel.exitLocation]
    playerLocs = []
    i = 0
    while i < numPlayers:  # Populate players in level
        playerName = game.players[i]
        randBoardNum, randBoard = getRandomRoomInLevel(nextLevel)
        log("Rand board", str(randBoardNum), str(randBoard.dimensions))
        loc = genXRandCoords(1, forbidden, randBoard.origin,
                             randBoard.dimensions).pop()
        if loc not in playerLocs:
            player = Player(playerName, loc)
            nextLevel.boards[randBoardNum] = addPlayersToBoard(randBoard, {
                playerName: player})
            playerLocs.append(loc)
            i += 1

    return game


def interactWithExit(playerName: str, location: tuple, game: Dungeon):
    """
    Computes the resulting game state of a player acquires an exit in the
    level.
    :param playerName: str
    :param location: tuple
    :param game: Dungeon
    """
    log("Interacting with exit")
    for level in game.levels:
        if location == level.exitLocation:
            if level.exitUnlocked:
                currBoardNum = whichBoardInLevel(level, location)
                playersLeft = getPlayersInLevel(level)
                log("Players left --->", str(playersLeft))
                if len(playersLeft) == 1:  # last player
                    # FIXME return advanceLevel(game)
                    log("Last player")
                    return advanceLevel(game)
                else:
                    log("Removing player")
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
