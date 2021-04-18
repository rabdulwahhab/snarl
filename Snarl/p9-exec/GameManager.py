from Types import *
from Create import createDungeon, addPlayersToBoard, removePlayersFromBoard
from Move import moveEntity
from Rulechecker import destHasEnemy, destHasKey, destHasExit, destHasPlayer, \
    destHasWall, playerCanMoveTo
from Util import whichBoardInLevel, logInFile, getPlayer, genXRandCoords, \
    getRandomRoomInLevel, getPlayersInLevel, getEnemy, getAllPlayers

log = logInFile("GameManager.py")


def move(entityName: str, destination, game: Dungeon, isPlayer=True):
    """
    Updates the game to reflect the movement of a player if they
    can move to the given destination in the game or skip a turn when
    destination is None. Returns an unmodified game if the player cannot
    move based on game rules.
    :param entityName: str
    :param destination: tuple | None
    :param game: Dungeon
    """
    currLevel: Level = game.levels[game.currLevel]

    # Player move is skipped
    if destination is None:
        # only increment player turn
        updatedPlayerTurn = currLevel.playerTurn + 1
        if updatedPlayerTurn == len(game.players) - 1:
            currLevel.playerTurn = 0
        else:
            currLevel.playerTurn = updatedPlayerTurn
        return game

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
            updatedLevel.enemyTurn = updatedLevel.enemyTurn + 1
        else:
            updatedLevel.playerTurn = updatedLevel.playerTurn + 1
            updatedLevel.enemyTurn = updatedLevel.enemyTurn + 1
        game.levels[game.currLevel] = updatedLevel
        updatedGame = interact(entityName, destination, game)
        return updatedGame
    elif not isPlayer:
        updatedLevel = moveEntity(currLevel, entityName, currBoardNum,
                                  newBoardNum, destination, isPlayer=False)
        game.levels[game.currLevel] = updatedLevel
        updatedGame = enemyInteract(entityName, destination, game)
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
        return interactWithKey(playerName, location, game)
    elif destHasExit(location, currLevel):
        return interactWithExit(playerName, location, game)
    # elif destHasItem(location, currBoard):
    #     TODO implement interactWithItem
    #     return game
    else:
        return game


def ejectPlayer(playerName: str, currBoardNum: int, game: Dungeon):
    game.levels[game.currLevel].ejects.append(playerName)
    game.scores[playerName]['ejects'] += 1
    return removePlayer(playerName, currBoardNum, game)


def exitPlayer(playerName: str, currBoardNum: int, game: Dungeon):
    game.levels[game.currLevel].exits.append(playerName)
    game.scores[playerName]['exits'] += 1
    return removePlayer(playerName, currBoardNum, game)


def enemyInteract(enemyName: str, destination: tuple, game: Dungeon):
    currLevel: Level = game.levels[game.currLevel]
    currBoardNum = whichBoardInLevel(currLevel, destination)
    currBoard: Board = currLevel.boards[currBoardNum]
    if destHasPlayer(destination, currBoard):
        return interactWithPlayer(destination, game)
    elif destHasWall(destination, currLevel):
        return interactWithWall(enemyName, destination, game)
    else:
        return game


def interactWithPlayer(dest: tuple, game: Dungeon):
    currLevel: Level = game.levels[game.currLevel]
    currBoardNum = whichBoardInLevel(currLevel, dest)
    currBoard: Board = currLevel.boards[currBoardNum]
    for player in currBoard.players.values():
        if player.location == dest:
            updatedGame = removePlayer(player.name, currBoardNum, game)
            if len(getAllPlayers(currLevel)) == 0:
                updatedGame = endGame(updatedGame)
            return updatedGame
    return game


def interactWithWall(enemyName: str, destination: tuple, game: Dungeon):
    """
    Only for ghosts, teleports the enemy to a random location in the level,
    or doesn't do anything if that's not possible. Returns an updated (or not)
    game.
    """
    currLevel = game.levels[game.currLevel]
    randBoardNum, randBoard = getRandomRoomInLevel(currLevel)
    enemy = getEnemy(currLevel, enemyName)
    while True:
        loc = genXRandCoords(1, [enemy.location],
                             randBoard.origin,
                             randBoard.dimensions).pop()
        if not destHasWall(loc, currLevel) and not destHasPlayer(loc,
                                                                 randBoard):
            newDestForGhost = loc
            break
    # Move ghost to newDest, and delete from currBoard
    game = move(enemyName, newDestForGhost, game, isPlayer=False)
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
            updatedGame = ejectPlayer(playerName, currBoardNum, game)
            # if last player in level, game over
            if len(getAllPlayers(currLevel)) == 0:
                updatedGame = endGame(updatedGame)
            return updatedGame
    return game


def interactWithKey(playerName: str, location: tuple, game: Dungeon):
    """
    Computes the resulting game state of a player acquiring a key in the
    level.
    :param playerName: str
    :param location: tuple
    :param game: Dungeon
    """
    level = game.levels[game.currLevel]
    if level.keyLocation == location:
        level.exitUnlocked = True
        level.key = playerName
        game.scores[playerName]['keys'] += 1
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
    game.levels[game.currLevel].boards[currBoardNum] = updatedBoard
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
                log("Removing player")
                updatedGame = exitPlayer(playerName, currBoardNum, game)
                if len(getAllPlayers(level)) == 0:
                    updatedGame = endGame(updatedGame)
                return updatedGame

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
