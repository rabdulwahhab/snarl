import socket
import sys
import math
import time

from Util import isDoorLocation, isTraversable, intifyTuple, getEnemiesInLevel
from Player import getVisibleTiles, getFieldOfView, getPlayer
from Types import *
from Rulechecker import isLevelOver
from GameManager import *
from Enemy import enemyNextMove
from Messages import *
from Convert import convertJsonLevel, addPlayersToBoard, addEnemiesToBoard
from more_itertools import first_true

"""
The Snarl Server:

- dish out connections
- create new game 
- handle joins 
- start game 
- administer game
    - broadcast game 
- end game
"""

log = logInFile("Server.py")


class PlayerDisconnect(Exception):
    pass


def populatePlayers(level: Level, playerNames: list):
    numPlayers = len(playerNames)
    forbidden = [level.keyLocation, level.exitLocation]
    players = []
    playerLocs = []
    i = 0
    while i < numPlayers:  # Populate players in level
        playerName = playerNames[i]
        randBoardNum, randBoard = getRandomRoomInLevel(level)
        log("Rand board", str(randBoardNum), str(randBoard.dimensions))
        loc = genXRandCoords(1, forbidden, randBoard.origin,
                             randBoard.dimensions).pop()
        if loc not in playerLocs:
            player = Player(playerName, loc)
            players.append(player)
            level.boards[randBoardNum] = addPlayersToBoard(randBoard, {
                playerName: player})
            playerLocs.append(loc)
            i += 1
    return playerLocs, level


def populateEnemies(levelNum: int, levelEnemies: dict, game: Dungeon):
    for enemyName in levelEnemies.keys():  # Populate enemies in level
        enemyBoardNum = levelEnemies[enemyName][0]
        board: Board = game.levels[levelNum].boards[enemyBoardNum]
        game.levels[levelNum].boards[enemyBoardNum] = addEnemiesToBoard(
            board, {
                enemyName: levelEnemies[enemyName][1]})


def initEnemies(game: Dungeon, initPlayerLocs: list):
    enemies = []  # LIST of dictionaries for each level
    forbiddenLocs = initPlayerLocs

    for i in range(len(game.levels)):
        numZombies = math.floor((i + 1) / 2) + 1
        numGhosts = math.floor(((i + 1) - 1) / 2)
        forbiddenLocs += [game.levels[i].keyLocation,
                          game.levels[i].exitLocation]
        levelEnemies = {}
        enemyLocs = []
        for ghost in range(numGhosts):
            randBoardNum, randBoard = getRandomRoomInLevel(game.levels[i])
            name = "ghost" + str((ghost + 1))
            loc = genXRandCoords(1, forbiddenLocs + enemyLocs,
                                 randBoard.origin,
                                 randBoard.dimensions)
            enemyLocs.append(loc)
            newGhost = Enemy(name, loc, "ghost")
            levelEnemies[name] = (randBoardNum, newGhost)

        forbiddenLocs += [board.doorLocations for board in
                          game.levels[i].boards]
        for zombie in range(numZombies):
            randBoardNum, randBoard = getRandomRoomInLevel(game.levels[i])
            name = "zombie" + str((zombie + 1))
            loc = genXRandCoords(1, forbiddenLocs + enemyLocs,
                                 randBoard.origin,
                                 randBoard.dimensions).pop()
            enemyLocs.append(loc)
            newZombie = Enemy(name, loc)
            levelEnemies[name] = (randBoardNum, newZombie)

        enemies.append(levelEnemies)
        populateEnemies(i, levelEnemies, game)
        forbiddenLocs = []
    return game


def closeConns(conns: dict):
    for conn in conns.values():
        conn.close()


def sendPlayer(playerName: str, msg: str, conns: dict):
    conn = conns[playerName]
    conn.sendall(msg.encode('utf-8'))


def broadcast(msg: str, conns: dict):
    msg = json.dumps(msg)
    for conn in conns.values():
        conn.sendall(msg.encode('utf-8'))


def broadcastPlayerUpdates(conns: dict, game: Dungeon):
    for playerName in conns.keys():
        if getPlayer(game.levels[game.currLevel], playerName):
            msg = "--> Player Update: {}\n".format(playerName)
            msg += formatted(getPlayerUpdate(playerName, game))
            sendPlayer(playerName, msg, conns)


def broadcastLevelOver(game: Dungeon, conns: dict):
    for playerName in conns.keys():
        msg = "--> Level Over <--\n"
        msg += endLevelMsg(game)
        sendPlayer(playerName, msg, conns)


def broadcastGameOver(game: Dungeon, conns: dict):
    msg = "=== GAME OVER ===\n"
    msg += endGameMsg(game)
    broadcast(msg, conns)


def getTileType(location: tuple, game: Dungeon):
    """
    Return 0, 1, or 2 depending on what lies
    at the given location
    """
    if isDoorLocation(location, game):
        return 2
    elif isTraversable(location, game):
        return 1
    else:
        return 0


def getTileLayout(game: Dungeon, player: Player):
    """
    Returns the tile layout of around a player currently in the game.
    :params game: Dungeon
    :params player: Player
    """
    layout = [[-1, -1, -1, -1, -1],
              [-1, -1, -1, -1, -1],
              [-1, -1, -1, -1, -1],
              [-1, -1, -1, -1, -1],
              [-1, -1, -1, -1, -1]]
    pRow, pCol = player.location
    origin = (pRow - 2, pCol - 2)
    for r in range(5):
        for c in range(5):
            relLoc = (origin[0] + r, origin[1] + c)
            layout[r][c] = getTileType(relLoc, game)
    return layout


def getActorsAroundPlayer(possMoves: list, game: Dungeon):
    """
    Returns the actors around a player in JSON format.
    :params possMoves: list
    :params game: Dungeon
    """
    acc = []
    for loc in possMoves:
        level: Level = game.levels[game.currLevel]
        boardNum = whichBoardInLevel(level, loc)
        if destHasEnemy(loc, level.boards[boardNum]):
            enemy: Enemy = first_true(level.boards[boardNum].enemies.values(),
                                      pred=lambda enem: enem.location == loc)
            acc.append({
                "type":     enemy.enemyType,
                "name":     enemy.name,
                "position": loc
            })
        if destHasPlayer(loc, level.boards[boardNum]):
            player: Player = first_true(level.boards[boardNum].players.values(),
                                        pred=lambda
                                            playa: playa.location == loc)
            acc.append({
                "type":     "player",
                "name":     player.name,
                "position": loc
            })
    return acc


def getObjectsAroundPlayer(possMoves: list, game: Dungeon):
    """
    Gets the objects around a player in JSON format.
    :params possMoves: list
    :params game: Dungeon
    """
    acc = []
    for loc in possMoves:
        level: Level = game.levels[game.currLevel]
        if destHasKey(loc, level):
            acc.append({"type": "key", "position": loc})
        elif destHasExit(loc, level):
            acc.append({"type": "exit", "position": loc})
    return acc


def getPlayerUpdate(playerName: str, game: Dungeon):
    """
    PlayerUpdateType is:
    {
      "type": "player-update",
      "layout": (tile-layout), # getLayout?
      "position": (point), # getPlayer.location
      "objects": (object-list), # getLocationsAround.map(if destHasItem || desthasKey -> return object)
        [ { "type": "key", "position": [ 4, 2 ] },
               { "type": "exit", "position": [ 7, 17 ] } ]
      "actors": (actor-position-list) # potentially getLocationsAround.map(if destHasEnemy -> return enemy)
    }

    1. Finds 25 points: surrounding 24 of given point
    2. Layout based on the 25 points
    3. Will check if enemies exist on any of those 25
    4. Will check if key or exit on any of those 25
    """
    player: Player = getPlayer(game.levels[game.currLevel], playerName)
    possMoves = getFieldOfView(player.name, game.levels[game.currLevel])
    output = {"type":     "player-update",
              "layout":   getTileLayout(game, player),
              "position": [player.location[0], player.location[1]],
              "objects":  getObjectsAroundPlayer(possMoves, game),
              "actors":   getActorsAroundPlayer(possMoves, game)}
    return output


def registerPlayers(numClients: int, sock: socket.socket):
    """
    Registers numClients amount of clients to the game on the socket
    as players and returns a dict of name -> connection.
    :params numClients: int
    :params sock: socket.socket
    """
    CONNS = {}
    numPlayersConnected = 0
    # Dish out connections + register sockets
    while numPlayersConnected < numClients:
        try:
            log = logInFile("Server.py", "Join loop")
            log("begin loop")

            # Block waiting for new connection
            conn, client_addr = sock.accept()
            log("Got a connection")

            introMsg = welcomeMsg('"Alon"')
            introMsg += "\nEnter your name"
            conn.sendall(introMsg.encode('utf-8'))

            name = conn.recv(1024).decode('utf-8').strip()
            log("Name received", name)

            CONNS[name] = conn  # register the player's conn
            log("Connected players:", str(list(CONNS.keys())))

            numPlayersConnected += 1
            if numPlayersConnected < numClients:
                conn.sendall(
                    "Welcome {}! Please wait for {} other players to join\n".format(
                        name, numClients - numPlayersConnected).encode(
                        'utf-8'))
        except UnicodeDecodeError:
            log("unicode decode error")
            if name in CONNS.keys():
                del CONNS[name]
            continue
        except ConnectionResetError:
            log("conn reset error")
            if name in CONNS.keys():
                del CONNS[name]
            continue
            # raise PlayerDisconnect
        except BrokenPipeError:
            log("broken pipe error")
            if name in CONNS.keys():
                del CONNS[name]
            continue
            # raise PlayerDisconnect
    return CONNS


def setupGame(playerNames: list, jsonLevels: list):
    """
    Initializes and returns a dungeon from a list of json levels and
    player names.
    :params playerNames: list
    :params jsonLevels: list
    """
    jsonGameLevels = [json.loads(rawJsonLevel) for rawJsonLevel in
                      jsonLevels]
    log("got+converted {} levels".format(len(jsonGameLevels)))
    levels = [convertJsonLevel(jsonLevel["rooms"], jsonLevel["hallways"],
                               jsonLevel["objects"]) for jsonLevel in
              jsonGameLevels]
    # init first level players
    initPlayerLocs, levels[0] = populatePlayers(levels[0], playerNames)

    # Create game
    GAME = Dungeon(levels, playerNames, 0, False)
    GAME = initEnemies(GAME, initPlayerLocs)
    return GAME, playerNames


def executeTurn(conn: socket.socket):
    """
    Awaits a move from the given player connection and returns a
    location tuple or None if turn is skipped or connection fails.
    :params conn: socket.socket
    """
    conn.sendall("move".encode('utf-8'))
    while True:
        try:
            resp = conn.recv(4096).decode('utf-8')
            playerMove = json.loads(resp)
            conn.sendall("\nok".encode('utf-8'))
            to = intifyTuple(playerMove["to"]) if playerMove["to"] else None
            return to
        except json.JSONDecodeError:
            # FIXME getting eof tries to decode but sock disconnected
            conn.sendall("Invalid move. Try again".encode('utf-8'))
        except ConnectionResetError:
            raise PlayerDisconnect
        except BrokenPipeError:
            raise PlayerDisconnect


def start(args):
    log = logInFile("Server.py")

    # Global vars
    JSON_LEVELS = args['jsonLevels']
    NUM_LEVELS = args['numLevels']
    NUM_CLIENTS = args['numClients']
    WAIT = args['wait']
    OBSERVE = args['observe']
    ADDRESS = args['address']
    PORT = args['port']

    # Ready to begin

    CONNS = {}
    SOCK = None

    try:
        SOCK = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        SOCK.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        SOCK.settimeout(WAIT)
        SOCK.bind((ADDRESS, PORT))
        SOCK.listen(NUM_CLIENTS)

        CONNS = registerPlayers(NUM_CLIENTS, SOCK)

        # Setup game (Convert levels, populate players, populate enemies,
        # create dungeon)
        GAME, playerNames = setupGame(list(CONNS.keys()), JSON_LEVELS)

        # Broadcast initial game state
        broadcast(startLevelMsg(1, playerNames), CONNS)

        # Send initial player update msgs
        broadcastPlayerUpdates(CONNS, GAME)

        log("GAME INITIALIZED!")

        # Enter main loop
        while True:

            # Obtain the current level
            currLevel: Level = GAME.levels[GAME.currLevel]

            # Check if the level has been completed
            if isLevelOver(currLevel):
                GAME = advanceLevel(GAME)
                broadcastLevelOver(GAME, CONNS)

            # Check if game is over
            if GAME.isGameOver:
                broadcastGameOver(GAME, CONNS)
                broadcast("disconnect", CONNS)

            # Execute player turns
            for playerName in playerNames:
                try:
                    player = getPlayer(currLevel, playerName)
                    if player:
                        initLoc = player.location
                        playerTurn = GAME.levels[GAME.currLevel].playerTurn
                        MAX_TRIES = 5
                        for tries in range(MAX_TRIES):
                            time.sleep(1)
                            playerMove = executeTurn(CONNS[playerName])
                            GAME = move(playerName, playerMove, GAME)
                            playerAfter = getPlayer(currLevel, playerName)
                            moveMade = not playerAfter or playerTurn != \
                                       GAME.levels[
                                           GAME.currLevel].playerTurn
                            if moveMade:
                                break
                            # last turn and still no valid move made
                            if not moveMade:
                                if tries == (MAX_TRIES - 1):
                                    GAME = move(playerName, None, GAME)
                                else:
                                    sendPlayer(playerName,
                                               "Invalid move. Try again...",
                                               CONNS)

                        broadcastPlayerUpdates(CONNS, GAME)
                except PlayerDisconnect:
                    # TODO broadcast??
                    log("PLAYER DISCONNECTED")
                    player: Player = getPlayer(currLevel, playerName)
                    playerBoardNum = whichBoardInLevel(currLevel,
                                                       player.location)
                    GAME = removePlayer(playerName, playerBoardNum, GAME)
                    # TODO reset playerNames
                    continue

            # Execute enemy turns
            currLevel: Level = GAME.levels[GAME.currLevel]
            for enemy in getEnemiesInLevel(currLevel):
                nextMove = enemyNextMove(enemy, GAME)
                GAME = move(enemy.name, nextMove, GAME, isPlayer=False)
                broadcastPlayerUpdates(CONNS, GAME)
                # for playerName in playerNames:
                # msg = enemy.name + " moved"
                # broadcast(playerUpdateMsg(playerName, GAME, msg), CONNS)


    except json.JSONDecodeError:
        print("Malformed level file. Check your formatting")
        closeConns(CONNS)
        if SOCK:
            SOCK.close()
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nExiting...")
        closeConns(CONNS)
        if SOCK:
            SOCK.close()
        sys.exit(0)
