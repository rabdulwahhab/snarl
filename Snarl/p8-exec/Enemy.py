from Types import *
from Util import getLocationsAround, whichBoardInLevel, locationInBounds, \
    locationInLevelBounds, getPlayer, distanceFormula, log
from functools import reduce


def enemyPossibleMoves(enemy: Enemy, game: Dungeon):
    """
    Gets a list of the possible moves a given enemy can feasibly make.
    In essence, gets all the moves are traversable within each enemy's
    walkable distance.
    :params enemy: Enemy
    :params game: Dungeon
    """
    possibleMoves = []
    enemyBoardNum = whichBoardInLevel(game.levels[game.currLevel],
                                      enemy.location)
    enemyBoard: Board = game.levels[game.currLevel].boards[enemyBoardNum]
    if enemy.enemyType == "zombie":
        tilesAround = getLocationsAround(enemy.location)
        for loc in tilesAround:
            if locationInBounds(loc, enemyBoard.origin, enemyBoard.dimensions):
                tile = enemyBoard.tiles[loc[0]][loc[1]]
                if tile.tileType != TileEnum.WALL and tile.tileType != TileEnum.DOOR:
                    possibleMoves.append(loc)
    elif enemy.enemyType == "ghost":
        tilesAround = getLocationsAround(enemy.location)
        for loc in tilesAround:
            if locationInLevelBounds(game.levels[game.currLevel], loc):
                possibleMoves.append(loc)
    return possibleMoves


def enemyStrat(possMoves: list, playerLocs: list):
    """
    Given a list of possible enemy moves and player locations, selects a
    location from possible moves according to our enemy movement strategy.
    Strategy: Pick the move with the shortest distance to any player.
    :params possMoves: list
    :params playerLocs: list
    """
    distTemp = None
    shortestTemp = None
    allShortest = []
    for possMove in possMoves:
        for playerLoc in playerLocs:
            if playerLoc in possMoves:
                return playerLoc
            dist = distanceFormula(playerLoc, possMove)
            if distTemp is None:
                distTemp = dist
            if dist <= distTemp:
                shortestTemp = possMove
    #   allShortest.append({"possMove": possMove, "shortest": shortestTemp})
    # shortestEntry = reduce(
    #    lambda acc, entry: entry if entry["shortest"] < acc[
    #        "shortest"] else acc, allShortest)
    #return shortestEntry["possMove"]
    return shortestTemp


def getPlayersInRoomAndLevel(boardNum: int, game: Dungeon):
    """
    Returns a tuple of a list of the players alive at the given board number
    in the current level and a list of the players alive in the current level.
    :params boardNum: int
    :params game: Dungeon
    """
    board: Board = game.levels[game.currLevel].boards[boardNum]
    playersInOurRoom = []
    playersInLevel = []
    for playerName in game.players:
        player = getPlayer(game.levels[game.currLevel], playerName)
        if player:
            playersInLevel.append(player)
            if player.location[0] in board.tiles.keys():
                if player.location[1] in board.tiles[player.location[0]].keys():
                    playersInOurRoom.append(player)
    return playersInOurRoom, playersInLevel


def enemyNextMove(enemy: Enemy, game: Dungeon):
    """
    Selects the next move for a given enemy according to the predetermined
    move strategies for enemies. If no valid moves are possible,
    then returns the enemy's location.
    """
    enemyBoardNum = whichBoardInLevel(game.levels[game.currLevel],
                                      enemy.location)
    possMoves = enemyPossibleMoves(enemy, game)
    if len(possMoves) == 0:
        return enemy.location

    playersInOurRoom, playersInOurLevel = getPlayersInRoomAndLevel(
        enemyBoardNum, game)

    if len(playersInOurRoom) != 0:
        playerLocs = [player.location for player in playersInOurRoom]
        return enemyStrat(possMoves, playerLocs)
    elif len(playersInOurLevel) != 0:
        playerLocs = [player.location for player in playersInOurLevel]
        return enemyStrat(possMoves, playerLocs)
    else:  # No valid move
        log("shouldn't EVER EZVER EVER get here. green man you must MOVE")
        return enemy.location
