import socket
import sys
import json
import math
import argparse
import re

sys.path.append("../")
from Util import logInFile, getRandomRoomInLevel, genXRandCoords, \
    isDoorLocation, isTraversable, whichBoardInLevel
from Player import getVisibleTiles, getFieldOfView, getPlayer
from Types import *
from GameManager import *
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


def broadcast(msg: str, conns: dict):
    msg = json.dumps(msg)
    for conn in conns.values():
        conn.send(msg.encode('utf-8'))


def sendPlayer(playerName: str, msg: str, conns: dict):
    conn = conns[playerName]
    conn.send(msg.encode('utf-8'))


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


def getEnemiesAroundPlayer(possMoves: list, game: Dungeon):
    """
    Returns the enemies around a player in JSON format.
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
              "actors":   getEnemiesAroundPlayer(possMoves, game)}
    return output


def main():
    log = logInFile("Server.py")

    DEFAULT_LEVEL = './snarl.levels'
    CLIENTS = 4
    WAIT = 60
    OBSERVE = False
    ADDRESS = '127.0.0.1'
    PORT = 45678

    parser = argparse.ArgumentParser()  # initialize
    # this is how you add an optional argument
    parser.add_argument("--levels",
                        help="Enter the name of an input JSON Level file",
                        nargs='?',
                        const=DEFAULT_LEVEL, type=str)
    parser.add_argument("--clients",
                        help="Enter the amount of clients connecting to the game",
                        nargs='?',
                        const=CLIENTS, type=int)
    parser.add_argument("--wait",
                        nargs='?',
                        help="Enter the amount of time to wait for the next client to connect",
                        const=WAIT, type=int)
    parser.add_argument("--observe", help="Observe the game",
                        action="store_true")
    parser.add_argument("--address",
                        nargs='?',
                        help="Enter the IP address to listen for connections",
                        const=ADDRESS, type=str)
    parser.add_argument("--port",
                        nargs='?',
                        help="Enter the port number to listen on",
                        const=PORT, type=int)

    # this is called after you define your optional args
    args = parser.parse_args()

    # Global vars
    JSON_LEVELS = None
    NUM_LEVELS = 0

    # Parse options
    if args.levels:
        # global NUM_LEVELS, JSON_LEVELS, log
        log('got levels flag', args.levels)
        with open(args.levels) as file:
            wholeFile = file.read()
            portions = wholeFile.split('\n\n')
            cleaned = list(filter(lambda port: port != '', portions))
            NUM_LEVELS = int(cleaned[0])
            JSON_LEVELS = cleaned[1:]
    else:
        log("using default level")
        # global NUM_LEVELS, JSON_LEVELS, log
        with open(DEFAULT_LEVEL) as file:
            wholeFile = file.read()
            portions = wholeFile.split('\n\n')
            cleaned = list(filter(lambda port: port != '', portions))
            NUM_LEVELS = int(cleaned[0])
            JSON_LEVELS = cleaned[1:]

    if args.clients:
        # global CLIENTS, log
        if 1 <= args.clients <= 4:
            log('got clients flag', str(args.clients))
            CLIENTS = args.clients
        else:
            print("Clients must be from 1-4")
            sys.exit(1)

    if args.wait:
        # global WAIT, log
        log('got wait flag', str(args.wait))
        WAIT = args.wait

    if args.observe:
        # global OBSERVE, log
        log('got observe')
        OBSERVE = True

    if args.address:
        # global ADDRESS, log
        log("got address flag")
        if re.search("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", args.address):
            ADDRESS = args.address
        else:
            print("Invalid address given. Try again")
            sys.exit(1)

    if args.port:
        # global PORT, log
        log("got port flag")
        if 2000 <= args.port <= 65000:
            log('got port flag', str(args.port))
            PORT = args.port
        else:
            print("Invalid port number. Try again")
            sys.exit(1)

    # Ready to begin

    CONNS = {}
    SOCK = None

    try:
        SOCK = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        SOCK.settimeout(WAIT)
        SOCK.bind((ADDRESS, PORT))
        SOCK.listen(CLIENTS)

        numPlayersConnected = 0

        # Dish out connections + register sockets
        while numPlayersConnected < CLIENTS:
            try:
                log = logInFile("Server.py", "Join loop")
                log("begin loop")

                # Block waiting for new connection
                conn, client_addr = SOCK.accept()
                log("Got a connection")

                conn.send(welcomeMsg('"Alon"').encode('utf-8'))
                conn.send("Enter your name > ".encode('utf-8'))

                name = conn.recv(1024).decode('utf-8').strip()
                log("Name received", name)

                CONNS[name] = conn  # register the player's conn
                log("Connected players:", str(CONNS.keys()))

                numPlayersConnected += 1
                if numPlayersConnected < CLIENTS:
                    conn.send(
                        "Welcome {}! Please wait for {} other players to join\n".format(
                            name, CLIENTS - numPlayersConnected).encode(
                            'utf-8'))
            except UnicodeDecodeError:
                log("Received EOF (probably)")
                if name in CONNS.keys():
                    del CONNS[name]
                continue
            except socket.timeout:
                break

        # Setup game (Convert levels, populate players, populate enemies,
        # create dungeon)
        jsonGameLevels = [json.loads(rawJsonLevel) for rawJsonLevel in
                          JSON_LEVELS]
        log("got+converted {} levels".format(len(jsonGameLevels)))
        levels = [convertJsonLevel(jsonLevel["rooms"], jsonLevel["hallways"],
                                   jsonLevel["objects"]) for jsonLevel in
                  jsonGameLevels]
        playerNames = list(CONNS.keys())
        initPlayerLocs, levels[0] = populatePlayers(levels[0],
                                                    playerNames)  # init first level players

        # Create game
        GAME = Dungeon(levels, playerNames, 0, False)
        GAME = initEnemies(GAME, initPlayerLocs)

        # Broadcast initial game state
        broadcast(startLevelMsg(1, playerNames), CONNS)

        # Send initial player update msgs
        for playerName in playerNames:
            sendPlayer(playerName, playerUpdateMsg(playerName, GAME), CONNS)

        # Enter main loop
        while True:
            log("DONE CONNECTING")
            closeConns(CONNS)
            sys.exit(0)

    except FileNotFoundError:
        print("Couldn't find that level file. Try again")
        closeConns(CONNS)
        if SOCK:
            SOCK.close()
        sys.exit(1)
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


if __name__ == '__main__':
    main()
