
# A container for currently useless code that may be useful if and when we
# get to random level generation


# GIANT TODO
# def createBoards(corners, dimensions):
#     (levelWidth, levelHeight) = dimensions
#     # todo do math to determine boundaries of each
#     rooms = createRooms(numRooms, (levelWidth, levelHeight))
#     hallways = createHallways(numHallways, (levelWidth, levelHeight))
#     boards = interleave(rooms, hallways)
#     return boards

# TODO don't need to add enemies or players
# def createLevel(numRooms):
#     numHallways = randint(0, numRooms - 1)
#     numBoards = numRooms + numHallways
#     maxLevelWidth = Globals.GAME_WIDTH * numBoards
#     maxLevelHeight = Globals.GAME_HEIGHT * numBoards
#     minLevelWidth = Globals.GAME_WIDTH * (numBoards - 1)
#     minLevelHeight = Globals.GAME_HEIGHT * (numBoards - 1)
#     levelWidth = randint(minLevelWidth, maxLevelWidth)
#     levelHeight = randint(minLevelHeight, maxLevelHeight)
#     # TODO key excluded locations (player, wall, door, etc.)
#     keyLocation = Util.genXRandCoords(1, {(0, 0)}, (levelWidth, levelHeight))
#     exitLocation = Util.genXRandCoords(1, {(0, 0), keyLocation},
#                                        (levelWidth, levelHeight))
#     boards = createBoards(numRooms, numHallways, (levelWidth, levelHeight))
#     return Level(keyLocation, exitLocation, boards, False, 0)


# def addPlayersToBoard(board: Board, players):
#     withPlayers = board.players + players
#     updatedBoard = deepcopy(board)
#     updatedBoard.players = withPlayers
#     return updatedBoard


# def createGenericRoomTiles():
#     roomWidth = Globals.GAME_WIDTH
#     roomHeight = Globals.GAME_HEIGHT
#     doorLocation = (roomWidth - 1, roomHeight - 1)
#     roomTiles = []
#     for i in range(roomWidth):
#         for j in range(roomHeight):
#             getsKey = True if i == 0 and j == 0 else False  # TODO remove
#             tileType = TileEnum.DOOR if (i,
#                                          j) == doorLocation else TileEnum.DEFAULT
#             newTile = Tile(tileType, (i, j), getsKey)
#             roomTiles.append(newTile)
#     return roomTiles


# def createGenericRoom():
#     boardType = BoardEnum.ROOM
#     tiles = createGenericRoomTiles()
#     player = Player("Saleha", (3, 3))
#     enemy = Enemy("Big Monster", (2, 2))
#     item = Item("Potion", (5, 1), False)
#     room = Board(tiles, boardType, [(0, 0)], {"Saleha": player}, [enemy],
#                  [item])
#     return room


# def createGenericLevel():
#     exitLocation = Util.genDoorCoords(Globals.GAME_WIDTH, Globals.GAME_HEIGHT)
#     keyLocation = Util.genXRandCoords(1, {exitLocation})
#     boards = [createGenericBoards()]
#     level = Level(keyLocation, exitLocation, boards, False, 0)
#     return level