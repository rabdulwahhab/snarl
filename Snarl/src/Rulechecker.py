from Types import *


def playerCanMoveTo(destination: tuple, player: Player, level: Level):
    """
    Check if the destination given can be moved to by a given player
    """
    # TODO:
    #  possMoves: call playerPossibleMoves using player's location
    #  check destination's traversable, hasEnemy
    #  check if destination is in possMoves
    #  result = filter(!destHasEnemy(filter(areTraversable, surroundingLocs))
    #  return result > 0
    return True


def enemyCanMoveTo(destination: tuple, enemy: Enemy, level: Level):
    """
    Check if the destination given can be moved to by a given enemy
    """
    # Return name as playerCanMoveTo for now
    # TODO:
    #  possMoves: call playerPossibleMoves using player's location
    #  check if destination is in possMoves
    return True


def playerPossibleCardinalMoves(location: tuple, numMoves: int, level: Level):
    """
    Outputs the possible moves for a player given the number of cardinal moves
    """
    # TODO: maybe Util??
    #  ESSENTIALLY: combine traversable locations + those that do not have players/enemies
    #  result = []
    #  initialSurrounding = []
    #  potentialSurrounding = []
    #  currRoom = Find the location in level (what room or hallway?)
    #  numMovesCounter = numMoves - 1
    #  Get 4 surrounding locs (+1 in every direction)
    #    Add to potentialSurrounding, initialSurroundingi
    #  while numMoves > 0:
    #   for each in initialSurrounding:
    #     getSurroundingLocs, and add to potentialSurrounding
    #   decrement cnumMovesCounter
    #   if numMoves > 0 we may need to append initial to potential surroundings
    #  return result
    return []


def enemyPossibleCardinalMoves(location: tuple, enemy: Enemy, level: Level):
    """
    Outputs the possible moves for an enemy (given the Enemy may have different
    rules for movement)
    """
    # TODO: NO NUM MOVES, SO STANDARD + 2
    #  Call playerPossibleMoves(with numMoves = 2)
    return []


def destHasEnemy(destination: tuple, board: Board, level: Level):
    """
    Checks if moving to the destination will cause an interaction with an enemy
    """
    # TODO:
    #  ESSENTIALLY: check if board's enemies have a location equal to that of dest
    #  for each key in board.enemies:
    #    if dest == enemy.location
    #      return True
    return False


def destHasPlayer(destination: tuple, level: Level):
    """
    Checks if moving to the destination will cause an interaction with another
    player
    """
    # TODO:
    #  ESSENTIALLY: check if board's players have a location equal to that of dest
    #  for each key in board.players:
    #    if dest == player.location
    #      return True
    return False


def destHasKey(destination: tuple, level: Level):
    """
    Checks if moving to the destination will cause an interaction with a key
    """
    # TODO:
    #  ESSENTIALLY: check if board's enemies have a location equal to that of dest
    #  get key's location
    #  if dest == keyLoc
    #    return True
    return False


def destHasItem(destination: tuple, level: Level):
    """
    Checks if moving to the destination will cause an interaction with an item
    """
    # TODO:
    #  ESSENTIALLY: check if board's items have a location equal to that of dest
    #  for each item in items:
    #    if dest == item.location
    #      return True
    return False
